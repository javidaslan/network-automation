###################################################################################
#
# This file contains code examples for DNA Center API. 
# Javid Aslanov
# 
###################################################################################

import requests
from getpass import getpass
import json
from pprint import pprint
import traceback

requests.urllib3.disable_warnings(requests.urllib3.exceptions.InsecureRequestWarning)

def getToken(ip, username, password):
    """
    Get auth token
    """
    try:
        print("Obtaining token...", end='\r')
        r = requests.post(
            "https://{ip}/dna/system/api/v1/auth/token".format(ip=ip),
            auth=(username, password),
            headers={'content-type': 'application/json'},
            verify=False
        )
        data = r.json()
        print("Obtaining token...DONE!")
        return data
    except:
        print(traceback.format_exc())
        return None


def getFromAPI(ip, endpoint, token):
    """
    Get data from given URL using token
    """
    try:
        print("GET request to API, Endpoint: {}...".format(endpoint), end='\r')
        r = requests.get(
            "https://{dna_ip}/dna/intent/api/v1/{endpoint}".format(dna_ip=dna_ip, endpoint=endpoint),
            headers={'X-Auth-Token': token}, 
            verify=False
        )
        print("GET request to API, Endpoint: {}...DONE!".format(endpoint))
        return r.json()
    except:
        print(traceback.format_exc())

def postToAPI(ip, endpoint, data, token):
    """
    Start running commands on give devices
    """
    try:
        print("POST request to API, Endpoint: {}...".format(endpoint), end='\r')
        r = requests.post(
            "https://{dna_ip}/dna/intent/api/v1/{endpoint}".format(dna_ip=dna_ip, endpoint=endpoint),
            data = data,
            headers ={'X-Auth-Token': token},
            verify=False
        )
        return r.json()
    except:
        print(traceback.format_exc())

def getDeviceInfo(dna_ip, token, devices):
    """
    By specifying endpoint you can get device specific information.
    Currently following information is available:
    
    1. Interfaces
    """
    device_info_list = [] # list of dicts
    for device in devices:
        if device['softwareType']:
            device_info_list.append({
                'id': device['id'],
                'hostname': device['hostname'],
                'managementIpAddress': device['managementIpAddress'],
                'interfaceDetails': getFromAPI(ip=dna_ip, endpoint=f"interface/network-device/{device['id']}", token=token)
            }
        )
    
    with open('DeviceInfo.json', 'w') as f:
        f.write(json.dumps(device_info_list))
    
    print('Information from all devices gathered')

def runCommands(ip, endpoint, token, devices, commands):
    """
    Run list of commands on a given device(s) and return task ID
    """
    
    r = postToAPI(
        ip=ip,
        data = {"name" : "my commands", "commands" : commands, "deviceUuids" : devices},
        endpoint=endpoint,
        token=token
    )
    return r.json()



dna_ip = '10.10.20.85' # input("IP Address of your DNA Center: ")
username = 'admin' # input("username: ")
password = 'Cisco1234!'  # getpass()
token = getToken(dna_ip, username, password).get('Token', None)
if token:
    # Get site info
    site_info = getFromAPI(ip=dna_ip, endpoint='site-health', token=token)
    with open('SiteInfo.json', 'w') as f:
        f.write(json.dumps(site_info))
    
    # get inventory list of DNA Center
    # inventory = getInventory(ip=dna_ip, token=token)
    inventory = getFromAPI(ip=dna_ip, endpoint='network-device', token=token)
    with open('inventory.json', 'w') as f:
        f.write(json.dumps(inventory['response']))
    
    # Get device specific information
    getDeviceInfo(dna_ip=dna_ip, token=token, devices=inventory['response'])

    # get list of accepted read only commands
    # commands = getFromAPI(ip=dna_ip, endpoint='network-device-poller/cli/legit-reads', token=token)
    # print(commands)
    # run commands on give devices
    # task_id = runCommands(ip=dna_ip, endpoint='network-device-poller/cli/read-request', token=token, devices=devices, commands=["show ver | inc Software, Version", "show clock"])
    # print(task_id)
    