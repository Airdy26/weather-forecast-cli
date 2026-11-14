'''
General functions that are most used everywhere
Opening files, opening urls, and extracting info from input strings
'''
from pathlib import Path
import json
import urllib.request

class FileFormatError(Exception):
    pass
class MissingFileError(Exception):
    pass

def _open_json_file(file_name: str) -> dict|list:
    '''
    Opens a json file, loads it to json_file and returns its
    contents as a list or dictionary
    '''
    _check_valid_file(file_name)
    path = Path(file_name)
    file = open(path, 'r')
    json_file = json.load(file)
    if  type(json_file) != list and type(json_file) != dict:
         raise FileFormatError(str(path.resolve()))
    return json_file

def _check_valid_file(file_name:str) -> None:
    '''Checks if file is .json and if it exists.
    If not, raises exception. Otherwise, does nothing'''
    path = Path(file_name)
    if file_name.endswith(".json") == False:
        raise FileFormatError(str(path.resolve()))
    try:
        file = open(path, 'r')
    except:
        raise MissingFileError(str(path.resolve()))
    
def _open_json_url(url_name: str ) -> dict|list:
    '''
    Opens are reads a url from API, returns its 
    contents as list or dict
    '''
    file = urllib.request.urlopen(url_name)
    file_info = file.read()
    json_file = json.loads(file_info)
    return json_file
def _convert_coordinates(coord: tuple[float]) -> tuple[str]:
    '''
    Param = tuple(lat,lon)
    Converts raw coordinates to proper format (doesnt have to be rounded off to 4)
    Has 4 decimal points and letter at end rather than pos or neg
    '''
    lat, lon = coord
    #For Latitude
    if 0 <= lat and lat <= 90:     #positive 0-90
        new_lat = str(lat) + '/N'
    elif 0 > lat and lat >= -90:    #negative -1 to -90
        new_lat = str(abs(lat)) + '/S'
    #For longitude
    if 0 <= lon and lon <= 180:     #positive 0-180
        new_lon = str(lon) + '/E'
    elif 0 > lon and lon >= -180:    #negative -1 to -180
        new_lon = str(abs(lon)) + '/W'
    
    return new_lat,new_lon

def _extract_key_two(user_input: str) -> str:
    input_list = user_input.split(' ', 2)
    return input_list[2]

def _extract_key_one(user_input: str) -> str:
    input_list = user_input.split(' ', 1)
    return input_list[1]

