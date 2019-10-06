# Cisco DNA Center API

This folder contains code examples of DNA Center API

## Following endpoints tested:

1. network-device

    <b>Request Type:</b> GET<br>
    <b>Description:</b> Get inventory of DNA Center

2. network-device-poller/cli/legit-reads

    <b>Request Type:</b> GET<br>
    <b>Description:</b> Get list of accepted read only commands

3. network-device-poller/cli/read-request

    <b>Request Type:</b> GET<br>
    <b>Description:</b> Run commands on give devices

4. interface/network-device/${device}

    <b>Request Type:</b> GET<br>
    <b>Description:</b> Get interface of device by ID

5. site-health

    <b>Request Type:</b> GET<br>
    <b>Description:</b> Get overall site information

6. auth/token

    <b>Request Type:</b> POST<br>
    <b>Request Body:</b> []<br>
    <b>Authentication:</b> Basic Auth<br>
    <b>Description:</b> Get authentication token