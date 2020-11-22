import requests
import sys
import json

DNAC = "sandboxdnac.cisco.com"
DNAC_USER = "devnetuser"
DNAC_PASSWORD = "Cisco123!"
DNAC_PORT = 80

def get_auth_token(controller=DNAC, username=DNAC_USER, password=DNAC_PASSWORD):
    """ Authenticates with controller and returns a token to be used in subsequent API invocations
    """

    login_url = f"https://{controller}/dna/system/api/v1/auth/token"
    result = requests.post(url=login_url, auth=requests.auth.HTTPBasicAuth(username, password), verify=False)
    result.raise_for_status()

    token = result.json()["Token"]
    return {
        "token": token
    }

def create_url(path, controller=DNAC):
    """ Helper function to create a DNAC API endpoint URL
    """

    return "https://%s/api/v1/%s" % (controller, path)

def ip_to_id(ip):
    """Get a device-id using an IP address

    Args:
        ip (string): IP address x.x.x.x

    Returns:
        [string]: device_id
    """    
    return get_url(f"network-device/ip-address/{ip}")['response']['id']

def get_modules(id):
    """Get all modules for a device using a device-id

    Args:
        id (string): device-id

    Returns:
        [type]: modules
    """    
    return get_url(f"network-device/module?deviceId={id}")

def get_url(url):

    url = create_url(path=url)
    print(url)
    token = get_auth_token()
    headers = {'X-auth-token' : token['token']}
    try:
        response = requests.get(url, headers=headers, verify=False)
    except requests.exceptions.RequestException as cerror:
        print("Error processing request", cerror)
        sys.exit(1)

    return response.json()

def print_info(modules):
    print("{0:30}{1:15}{2:25}{3:5}".format("Module Name","Serial Number","Part Number","Is Field Replaceable?"))
    for module in modules['response']:
        print("{moduleName:30}{serialNumber:15}{partNumber:25}{moduleType:5}".format(moduleName=module['name'],
                                                           serialNumber=module['serialNumber'],
                                                           partNumber=module['partNumber'],
                                                           moduleType=module['isFieldReplaceable']))


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

def get_device_ids(api_token, controller=DNAC):
    """[summary]
    """

    url = f"https://{controller}/dna/intent/api/v1/network-device"

    payload = {}
    headers = {'X-Auth-Token': api_token}

    response = requests.get(url, headers=headers, verify=False)
    return [device['id'] for device in response.json()['response']]

if __name__ == "__main__":
    token = get_dnac_token()
    #display_id_and_ip(token['Token'])
    device_id_list = get_device_ids(token['Token'])

    for dev_id in device_id_list:
        modules = get_modules(dev_id)
        print_info(modules)