import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv
from db_con import fetch_incident_data


# Jira Service Management Configuration (Same as before)
JIRA_DOMAIN = os.getenv('JIRA_DOMAIN')
JIRA_EMAIL = os.getenv('JIRA_EMAIL')
JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')
SERVICE_DESK_ID = os.getenv('JIRA_SERVICE_DESK_ID')
REQUEST_TYPE_ID = os.getenv('JIRA_REQUEST_TYPE_ID')

# Jira Request Details 
PRIORITY_FIELD_ID = "customfield_10001"
REPORTER_FIELD_ID = "customfield_10002"



def build_jira_payload(incident_data):
    """Constructs the JSON payload for the Jira API (Logic is unchanged)."""
    
    request_field_values = {
        "summary": f"[PG-INC {incident_data['incident_id']}]: {incident_data['summary_text']}",
        "description": incident_data['description_detail'],
        
        # Custom Fields need specific formatting based on their Jira type
        PRIORITY_FIELD_ID: {
            "value": incident_data['priority_level']
        },
        REPORTER_FIELD_ID: {
            "accountId": incident_data['jira_reporter_account_id']
        }
    }
    
    payload = {
        "serviceDeskId": SERVICE_DESK_ID,
        "requestTypeId": REQUEST_TYPE_ID,
        "requestFieldValues": request_field_values
    }
    return payload


def create_jira_request(payload):
    """Sends the constructed payload to the Jira API."""
    
    json_payload = json.dumps(payload)
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(
            JIRA_API_URL,
            headers=headers,
            auth=(JIRA_EMAIL, JIRA_API_TOKEN), 
            data=json_payload
        )
        response.raise_for_status()
        
        jira_response_data = response.json()
        print(f"Successfully created Jira request: {jira_response_data.get('issueKey')}")
        return jira_response_data
        
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
        print(f"Response content: {response.text}")
    except requests.exceptions.RequestException as err:
        print(f"An error occurred during the API request: {err}")
    
    return None




if __name__ == "__main__":
    print(f"--- Automation Script Started at {datetime.now()} ---")
    
    # 1. Get the data from PostgreSQL
    data_record = fetch_incident_data()
    
    if data_record:
        print(f"Fetched incident ID: {data_record['incident_id']}")
        
        # 2. Build the payload
        jira_payload = build_jira_payload(data_record)
        
        # 3. Send the request
        new_request = create_jira_request(jira_payload)
        
        # NOTE: You may want to add logic here to UPDATE the 'processed' flag 
        # in your PostgreSQL database if the request was successful (new_request is not None).
    
    print("--- Automation Script Finished ---")
