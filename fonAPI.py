import sys
import json
import requests
"""
    Class FonApi
    Author @jesusperiago
    Version 1
"""


class FonApi:

    __ApiUrl = 'https://fonoapi.freshpixl.com/v1/'

    def __init__(self, apikey, url=None):

        self.__ApiUrl = FonApi.__ApiUrl

        if url is not None:
            self.__ApiUrl = url

        self.__ApiKey = apikey

    def getDevice(self, device, position=None, brand=None, limit = 5):
        """
        Get device data object and return a json list
        :param device:
        :param position:
        :param brand:
        :return device list:
        """
        url = self.__ApiUrl + 'getdevice'
        postdata = {'brand': brand,
                    'device': device,
                    'position': position,
                    'limit': limit,
                    'token': self.__ApiKey}
        headers = {'content-type': 'application/json'}
        result = self.sendPostData(url, postdata, headers)
        try:
            return result.json()
        except AttributeError:
            return result


    def getLatest(self, brand = None, limit = 5):
        """
        Input: brand name if any
        Return a json list of latest devices
        """
        url = self.__ApiUrl + "getlatest"
        postdata = {
            'token': self.__ApiKey,
            'limit': limit,
            'brand': brand
        }
        headers = {'content-type': 'application/json'}
        result = self.sendPostData(url, postdata, headers)
        try: 
            print(result.json())
            return result.json()
        except AttributeError:
            return result


    def sendPostData(self, url, postdata, headers, result = None):
        """
            Send data to the server
        :param url:
        :param postdata:
        :param headers:

        :return requests.post result:
        """
        try:
            result = requests.post(url, data=json.dumps(postdata), headers=headers)
            # Consider any status other than 2xx an error
            if not result.status_code // 100 == 2:
                return "Error status page: " + str(result)
            # Try send the result text else send the error
            try:
                if result.json()['status'] == 'error':

                    if result.json()['message'] == 'Invalid Token. Generate a Token at fonoapi.freshpixl.com.':
                        return "Check __ApiKey"

                return result.json()['message']
            except:
                pass

            return result
        except requests.exceptions.RequestException as e:
            # A serious problem happened, like an SSLError or InvalidURL
            return "Connect error. Check URL"
