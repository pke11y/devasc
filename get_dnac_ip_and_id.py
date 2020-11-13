import requests

def get_dnac_token():
    """ HTTP POST to get DNA Center API Token
    """    

    url = "https://sandboxdnac.cisco.com/dna/system/api/v1/auth/token/"

    payload = {}
    headers = {
    'Authorization': 'Basic ZGV2bmV0dXNlcjpDaXNjbzEyMyE='
    }

    response = requests.post(url, headers=headers, data=payload, verify=False)
    return response.json()

def display_id_and_ip(api_token):
    """[summary]
    """

    url = "https://sandboxdnac.cisco.com/dna/intent/api/v1/network-device"

    payload = {}
    headers = {'X-Auth-Token': api_token}

    response = requests.get(url, headers=headers, verify=False)
    for device in response.json()['response']:
        print(f"ID: {device['id']} IP: {device['managementIpAddress']}")

if __name__ == "__main__":
    token = get_dnac_token()
    print(token['Token'])
    display_id_and_ip(token['Token'])
