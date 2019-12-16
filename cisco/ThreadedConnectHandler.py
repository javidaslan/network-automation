import threading
import traceback
import json
from queue import Queue
from netmiko.ssh_autodetect import SSHDetect
from netmiko.ssh_dispatcher import ConnectHandler
from netmiko import NetMikoTimeoutException, NetMikoAuthenticationException
from datetime import datetime

class ThreadedConnectHandler():
    
    _global_delay_factor = None
    
    def __init__(self, username, password, deviceList, commandList, global_delay_factor=None, threadCount=None, exportToJSON=False):
        """
        ThreadedConnectHandler class constructor
        """
        self._deviceCount = len(deviceList)
        self._threadCount = threadCount if threadCount else min(50, self._deviceCount) # number of threads
        self._deviceQueue = self._listToQueue(deviceList)
        self._outputQueue = Queue()
        self._threadList = [None] * self._threadCount
        self._username = username
        self._password = password
        self._commandList = commandList
        self.exportToJSON = exportToJSON
        if global_delay_factor:
            self._global_delay_factor = global_delay_factor
    
    def _show_progress(self, current_step, list_len):
        """
        Show progress bar
        """
        message = "Progress..."
        progress = current_step/list_len * 100
        progress_bar = "{0} {1:.2f} % ".format(message, progress)

        if progress == 100:
            print(' '*len(progress_bar), end='\r')
            print(progress_bar)
        else:
            print(progress_bar, end='\r')
    
    def _detect(self, device):
        net_connect = {'device_type': 'autodetect', 'host': device, 'username': self._username, 'password': self._password}
        if self._global_delay_factor:
            net_connect['global_delay_factor'] = self._global_delay_factor
        detecter = SSHDetect(**net_connect)
        device_type = detecter.autodetect()
        detecter.connection.disconnect()
        return device_type
    
    def _listToQueue(self, deviceList):
        """
        Queue will be used here to provide shared data synchronization among threads
        """
        tempQueue = Queue()
        for device in deviceList:
            tempQueue.put(device)
        return tempQueue

    def _queueToList(self, queueObject):
        """
        Convert queue object to list
        """
        listObject = []
        while not queueObject.empty():
            listObject.append(queueObject.get_nowait())
        return listObject

    def _handleThread(self):
        while not self._deviceQueue.empty():
            try:
                results = []
                device = self._deviceQueue.get_nowait()
                # print('Handling ' + device)
                device_type = self._detect(device)
                if device_type:
                    net_connect = {'device_type': device_type, 'host': device, 'username': self._username, 'password': self._password}
                    if self._global_delay_factor:
                        net_connect['global_delay_factor'] = self._global_delay_factor
                    connection = ConnectHandler(**net_connect)
                    for command in self._commandList:
                        output = connection.send_command(command)
                        results.append((command, output))
                    connection.disconnect()
                    self._outputQueue.put({'device': device, 'results': results, 'connected': True})
                else:
                    self._outputQueue.put({'device': device, 'results': None, 'connected': False})
            except Exception as e:
                self._outputQueue.put({'device': device, 'results': None, 'connected': False})
            finally:
                self._show_progress(self._outputQueue.qsize(), self._deviceCount)
    
    def _launchThreads(self):
        """
        Initiate and start threads
        """
        try:
            for i in range(self._threadCount):
                self._threadList[i] = threading.Thread(target=self._handleThread)
                self._threadList[i].start()
            for i in range(self._threadCount):
                self._threadList[i].join()
            return self._queueToList(self._outputQueue)
        except:
            print(traceback.format_exc())
            return None
    
    def resultsToJSON(self, resultsList, filename=None):
        """
        Optionally user can export results to JSON
        """
        filename = filename if filename else 'results.json'
        if filename[-5:] != '.json':
            filename = filename + '.json'
        try:
            with open(filename, 'w') as f:
                f.write(json.dumps(resultsList))
        except:
            print(traceback.format_exc())
                
    def start(self):
        """
        This functions starts the whole process
        """
        results = self._launchThreads()
        if self.exportToJSON:
            self.resultsToJSON(results)
        return results
            

