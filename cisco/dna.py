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

def getInventory(ip, token):
    """
    Get inventory of DNA Center and save to .json (optional)
    """
    inventory = getFromAPI(ip=dna_ip, endpoint='network-device', token=token)
    # uncomment if you want to save to .json
    with open('inventory.json', 'w') as f:
        f.write(json.dumps(inventory['response']))
    return inventory['response']

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

dna_ip = input("IP Address of your DNA Center: ")
username = input("username: ")
password = getpass()
token = getToken(dna_ip, username, password).get('Token', None)
if token:
    # get inventory list of DNA Center
    inventory = getInventory(ip=dna_ip, token=token)
    devices = [device['id'] for device in inventory if device['softwareType']] # take IDs to run commands

    # get list of accepted read only commands
    commands = getFromAPI(ip=dna_ip, endpoint='network-device-poller/cli/legit-reads', token=token)
    
    # run commands on give devices
    task_id = runCommands(ip=dna_ip, endpoint='network-device-poller/cli/read-request', token=token, devices=devices, commands=["show ver | inc Software, Version", "show clock"])
    print(task_id)
    