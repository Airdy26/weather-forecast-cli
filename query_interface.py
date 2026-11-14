'''
Module only for getting answers for query
Sets up user input to be used for answering
'''
import fetching_func
from collections import namedtuple
from weather_class_interface import WeatherAttribute

#--------------------------Exceptions--------------------------
class QueryInputError(Exception):
    pass

Info3 = namedtuple('Info3', ['scale', 'length', 'limit'])
Info2 = namedtuple('Info2', ['length', 'limit'])
#---------------Class for Queries-----------------
class Query():
    def __init__(self, query_list: list[str]) -> None:
        self._query_list = query_list
    
    def get_query_answers(self, forecast_list: list[dict]) -> list[str]:
        '''
        Uses list from .json file/url to answer queries.
        Returns a list of answers
        '''
        answer_list = []
        weather_obj = WeatherAttribute(forecast_list)
        for question in self._query_list:
            if question.startswith("TEMPERATURE AIR"):
                info_dict = _info_setup_temp(question)
                answer = weather_obj.get_air_temperature_ans(info_dict)
                answer_list.append(answer)
                
            elif question.startswith("TEMPERATURE FEELS"):
                info_dict = _info_setup_temp(question)
                answer = weather_obj._calc_feels_temp_ans(info_dict)
                answer_list.append(answer)
                
            elif question.startswith("HUMIDITY"):
                info_dict = _info_setup_one(question)
                answer = weather_obj.get_humidity_ans(info_dict)
                answer_list.append(answer)
                
            elif question.startswith("WIND"):
                info_dict = _info_setup_one(question)
                answer = weather_obj.get_wind_speed_ans(info_dict)
                answer_list.append(answer)
                
            elif question.startswith("PRECIPITATION"):
                info_dict = _info_setup_one(question)
                answer = weather_obj._get_percipitation_ans(info_dict)
                answer_list.append(answer)
                
        return answer_list    
#------------------------Helper Functions-----------------------------
def _info_setup_temp(question: str)-> Info3:
    '''
    Sets up query by getting scale, length, limit
    Stores them in to a list and validates
    Returns a named tuple
    '''
    info = fetching_func._extract_key_two(question)
    info_dict = _separate_info_3(info)
    if _verify_info(info_dict) == False:
        raise QueryInputError()
    return info_dict
def _info_setup_one(question: str) -> Info2:
    '''
    Sets up query bu getting length and limit from question
    Stores them in to a list and validates
    Returns a named tuple
    '''
    info = fetching_func._extract_key_one(question)
    info_dict = _separate_info_2(info)
    if _verify_info(info_dict) == False:
        raise QueryInputError()
    return info_dict
#-----------------------General helper functions------------------------
       
def _separate_info_3(user_info: str) -> Info3:
    '''
    Removes beginning command
    Separates user_info to a namedtuple Info3 with 3 elements
    info should have 3 parts (scale, length, limit)
    Returns namedtuple (scale, length, limit)
    Raises excpetion if wrong amount of info
    '''
    user_input = user_info.split(" ", 2)
    if len(user_input) == 3:
        info_namedtup = Info3(user_input[0], user_input[1], user_input[2])
    else:
        raise QueryInputError()
    
    return info_namedtup

def _separate_info_2(user_info: str) -> Info2:
    '''
    Removes beginning command
    Separates user_info to a namedtuple Info2 with 2 elements
    info should have 2 parts (length, limit)
    Returns namedtuple (length, limit)
    Raises excpetion if wrong amount of info
    '''
    user_input = user_info.split(" ", 1)
    if len(user_input) == 2:
        info_namedtup = Info2(user_input[0], user_input[1])
    else:
        raise QueryInputError()
    
    return info_namedtup
def _verify_info(info_tup: Info2|Info3) -> bool:
    '''
    Verifies if tuple of info has correct information
    Checks each element if it has appropriate format
    Tuple len is 2 or 3
    '''
    if info_tup.count == 3:
        if info_tup.scale != 'F' and info_tup != 'C':
            return False
        
    try:
        len = int(info_tup.length)
        if len < 1:
            return False
    except:
        return False
    
    if info_tup.limit != "MIN" and info_tup.limit !="MAX":
        return False
    
    return True
          

 