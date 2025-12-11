import requests
from requests_kerberos import HTTPKerberosAuth, OPTIONAL

# Define Kerberos authentication with mutual authentication configurations
kerberos_auth = HTTPKerberosAuth(mutual_authentication=OPTIONAL)

auth_data = {
    "username": "Basics of Information Security",
    "password": "AUT - 1403 - Requests.Kerberos"
}

# Base URL for the Flask app
BASE_URL = "http://127.0.0.1:5000"

'''
    This function will make a desired request to our Kerberos service.
    It will authenticate the request using Kerberos, send the request, and handle the response.
    
    Args:
        api_endpoint (str): The API endpoint you want to send the request to (e.g., "authenticate", "verify_ticket").
        data (dict): The data to be sent with the request. This will be passed as JSON in the request body.
        method (str): The HTTP method to use for the request. Should be either "GET" or "POST".
        
    Returns:
        dict or None: Returns the JSON response from the server if successful (status code 200),
                      or None if the request fails (non-200 status code).
'''


def make_kerberos_request(api_endpoint, data, method):
    url = f"{BASE_URL}/{api_endpoint}"
    
    if method == "POST":
        
        # here we will make out post request with kerberos_auth and needed headers and json data
        response = requests.post(url, auth=kerberos_auth, json=data)
    
    else:

        # here we will make out get request with kerberos_auth and needed headers and json data
        response = requests.get(url, auth=kerberos_auth, json=data)
    
    if response.status_code == 200:
        print(f"Successful request: {api_endpoint} ->", response.json())
        return response.json()
    else:
        print(f"Failed request: {api_endpoint} -> Status code {response.status_code}")
    
    return None


# Authenticate the user (assuming you have the token or credentials)
print("Step 1: Authenticating User...")

register_user = make_kerberos_request("register", auth_data, "POST")

if register_user:

    auth_response = make_kerberos_request("authenticate", auth_data, "GET")

    # Assuming we get back a ticket and session key from the auth API
    if auth_response:
        # TODO Extract the ticket and session_key from auth_response
        ticket = auth_response["ticket"]
        session_key = auth_response["session_key"]

        print("Step 2: Verifying Ticket...")
        # TODO provide ticket as the essential data for make_kerberos_request
        verify_ticket_data = {
            "ticket": ticket,
        }
        verify_ticket_response = make_kerberos_request("verify_ticket", verify_ticket_data, "GET")

        if verify_ticket_response:
            
            print("Step 3: Issuing Service Ticket...")
            # TODO
            issue_ticket_data = {
                "session_key": session_key,
                "service_name": "example_service"
            }
            issue_ticket_response = make_kerberos_request("issue_service_ticket", issue_ticket_data, "GET")

            if issue_ticket_response:
                
                print("Step 4: Verifying Service Ticket...")
                service_ticket = issue_ticket_response.get("service_ticket")

                # TODO
                verify_service_ticket_data = {
                    "service_ticket": service_ticket,
                }
                verify_service_ticket_response = make_kerberos_request("verify_service_ticket", verify_service_ticket_data, "GET")

                if verify_service_ticket_response:
                    print("All steps completed successfully!")
                else:
                    print("Failed to verify service ticket.")
            else:
                print("Failed to issue service ticket.")
        else:
            print("Failed to verify the ticket.")
    else:
        print("Authentication failed.")
