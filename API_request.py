'''
Module contains functions used to communicate with web APIs.
It has one for nominatim, NWS, and a function to encode urls.
Tools for web API data
'''
import urllib.parse
import urllib.request
import json
import time
from urllib.error import HTTPError, URLError

#--------------------------Exceptions--------------------------
class APIError(Exception):
    pass
class APIFormatError(Exception):
    pass

#-----------------------------Main Functions---------------------------
def get_nominatim_info(encoded_url: str) -> dict:
    '''
    Requests data from nominatim website with encoded_url. Provides header
    Request content depends on encoded_url, either for forward geocoding or reverse geocoding
    returns content of url as list 
    '''
    headers = {"User-Agent": "(https://www.ics.uci.edu/~thornton/icsh32/ProjectGuide/Project3/, aguilaas@uci.edu)"}
    file_content = None
    try:
        file_request = urllib.request.Request(encoded_url, headers = headers)
        time.sleep(1) #Just to be safe
        file_content = urllib.request.urlopen(file_request)
        content_list = file_content.read().decode(encoding = 'utf-8')
        loads = json.loads(content_list)

    except HTTPError as e:
        status = e.code
        error_code = str(status) + ' ' + encoded_url
        raise APIError(error_code)
    except URLError as e:
        status = e.reason
        if str(status).isdigit() == False:
            error_code = encoded_url
        else:
            error_code = str(status) + ' ' + encoded_url
        raise APIError(error_code)
    finally:
        if file_content != None:
            file_content.close() 
    if type(loads) != list and type(loads) != dict:
        error_code = str(file_content.code) + ' ' + encoded_url
        raise APIFormatError(error_code)
    return loads
  
def get_NWS_forecast(encoded_url: str) -> dict:
    '''
    Requests data from NWS website with encoded_url. Provides header
    Request content is a list used for hourly forecast and queries
    returns content of url as list  
    '''
    headers = { "Referer": "https://www.ics.uci.edu/~thornton/icsh32/ProjectGuide/Project3/aguilaas"}
    file_content = None
    try:
        file_request = urllib.request.Request(encoded_url, headers = headers)
        time.sleep(1)   
        file_content = urllib.request.urlopen(file_request)
        content_list = file_content.read().decode(encoding = 'utf-8')
        loads = json.loads(content_list)
    except HTTPError as e:
        status = e.code
        error_code = str(status) + ' ' + encoded_url
        raise APIError(error_code)
    except URLError as e:
        status = e.reason
        if status == None:
            error_code = encoded_url
        else:
            error_code = str(status) + ' ' + encoded_url
    finally:
        if file_content != None:
            file_content.close()        

    if type(loads) != list and type(loads) != dict:
        error_code = str(file_content.code) + ' ' +  encoded_url
        raise APIFormatError(error_code)
    return loads

def generate_url_encoded(base_url: str, query_parameters: list[tuple], format: tuple[str,str]):
    '''
    Generates new url with base url and encoded params
    Encodes url to be used by API.
    Base url should be valid and ends with ?
    '''
    query_parameters.append(format)
    encoded_query = urllib.parse.urlencode(query_parameters)
    new_url = base_url + encoded_query
    return new_url
    
    
    
