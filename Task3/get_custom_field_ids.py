import requests
from requests.auth import HTTPBasicAuth
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Jira configuration
JIRA_DOMAIN = os.getenv('JIRA_DOMAIN')
JIRA_EMAIL = os.getenv('JIRA_EMAIL')
JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')
SERVICE_DESK_ID = os.getenv('JIRA_SERVICE_DESK_ID')
REQUEST_TYPE_ID = os.getenv('JIRA_REQUEST_TYPE_ID')

def discover_fields():
    """Discover all fields for your Jira request type"""
    
    url = f"https://{JIRA_DOMAIN}/rest/servicedeskapi/servicedesk/{SERVICE_DESK_ID}/requesttype/{REQUEST_TYPE_ID}/field"
    
    auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
    
    try:
        print(f"🔍 Fetching fields from: {JIRA_DOMAIN}")
        print(f"   Service Desk ID: {SERVICE_DESK_ID}")
        print(f"   Request Type ID: {REQUEST_TYPE_ID}\n")
        
        response = requests.get(url, auth=auth)
        response.raise_for_status()
        
        fields = response.json()['requestTypeFields']
        
        print('='*80)
        print('JIRA FIELD MAPPING GUIDE')
        print('='*80)
        
        # Required fields
        required_fields = [f for f in fields if f.get('required')]
        if required_fields:
            for field in required_fields:
                print(f"\n '{field['name']}'")
                print(f"   Field ID: {field['fieldId']}")
                print(f"   Type: {field.get('jiraSchema', {}).get('type', 'unknown')}")
                
                if field.get('validValues'):
                    print(f"   Options:")
                    for opt in field['validValues'][:5]:
                        print(f"      - {opt['value']}")
                    if len(field['validValues']) > 5:
                        print(f"      ... and {len(field['validValues']) - 5} more")
        
        # Optional fields
        optional_fields = [f for f in fields if not f.get('required')]
        if optional_fields:
            for field in optional_fields:
                print(f"\n '{field['name']}'")
                print(f"   Field ID: {field['fieldId']}")
                print(f"   Type: {field.get('jiraSchema', {}).get('type', 'unknown')}")
                
                if field.get('validValues'):
                    print(f"   Options:")
                    for opt in field['validValues'][:5]:
                        print(f"      - {opt['value']}")
                    if len(field['validValues']) > 5:
                        print(f"      ... and {len(field['validValues']) - 5} more")
        
        print('\n' + '='*80)
        print('\n✅ SUCCESS! Now update your map_database_to_jira_fields() function')
        print('   with these field IDs.')
        print('\n  Match the field names above with your database columns:')
        print('   - newusername/samplename → Name field')
        print('   - job → Job title field')
        print('   - phonenumber → Phone field')
        print('   - emailaddress → Email field')
        print('   - departmentname → Department field')
        print('   - costcenter → Cost center field')
        print('   - telephonelinesandinstallations → Telephone lines field')
        print('   - handsetsandheadsets → Handsets field')
        print('   - timeframe → Time frame field')
        print('   - dateneededby → Date needed by field')
        print('='*80)
        
        # Save to file for reference
        with open('jira_fields.json', 'w') as f:
            json.dump(fields, f, indent=2)
        print('\n Full field details saved to: jira_fields.json')
        
        return fields
        
    except requests.exceptions.RequestException as e:
        print(f"Error discovering fields: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Status Code: {e.response.status_code}")
            print(f"Response: {e.response.text}")
        raise

if __name__ == "__main__":
    # Check if .env variables are loaded
    if not all([JIRA_DOMAIN, JIRA_EMAIL, JIRA_API_TOKEN, SERVICE_DESK_ID, REQUEST_TYPE_ID]):
        print("Error: Missing required environment variables in .env file")
    else:
        discover_fields()