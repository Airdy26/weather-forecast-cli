'''
Main file where program is ran
Mainly has user-input functions and 
printing appropriate results/output
'''
from fetching_func import FileFormatError, MissingFileError
import fetching_interface
import query_interface

#--------------------------Exceptions--------------------------
class InvalidCommand(Exception):
    pass
class FileError(Exception):
    pass
class FileMissingError(Exception):
    pass
class APIError(Exception):
    pass
    
#------------------User prompt functions-------------------------
def get_target_location() -> fetching_interface.API_ForwardGeocode|fetching_interface.File_ForwardGeocode:
    '''
    Asks user input for target location or file path
    Returns ForwardGeocode object based on input
    '''
    target_input = input()
    if target_input.startswith("TARGET NOMINATIM"):
        target_file = fetching_interface.API_ForwardGeocode(target_input)
    elif target_input.startswith("TARGET FILE"):
        target_file = fetching_interface.File_ForwardGeocode(target_input)
        
    return target_file

def get_weather_method(loc_coord: tuple[str]) -> fetching_interface.API_WeatherForecast|fetching_interface.File_WeatherForecast:
    '''
    Asks user input for how to obtain hourly forecasts
    Returns WeatherForecast Object depending on input
    Parameter is location coordinate for API object since it 
    needs to generate the url from coords to use NWS
    '''
    weather_method = input()
    if weather_method == "WEATHER NWS":
        weather_file = fetching_interface.API_WeatherForecast(loc_coord)
    elif weather_method.startswith("WEATHER FILE"):
        weather_file = fetching_interface.File_WeatherForecast(weather_method)
    return weather_file

def get_queries() -> list:
    '''
    Asks users for queries until exit
    Returns query list
    '''
    query_list = []
    while True:
        query = input()
        if query == 'NO MORE QUERIES':
            break
        query_list.append(query)
        
    return query_list

def get_reverse_method(loc_coord: tuple[str]) -> fetching_interface.API_Reverse|fetching_interface.File_Reverse:
    '''
    Asks user input for how to obtain hourly forecasts
    Returns WeatherForecast Object depending on input
    Parameter is location coordinate for API object since it 
    needs to generate the url from coords to use NWS
    '''
    rev_method = input()
    if rev_method == "REVERSE NOMINATIM":
        rev_file = fetching_interface.API_Reverse(loc_coord)
    elif rev_method.startswith("REVERSE FILE"):
        rev_file = fetching_interface.File_Reverse(rev_method)

    return rev_file

#-------------------Functions for formatted printing?--------------------
def print_location_coordinates(coord_tup: tuple[float]) -> None:
    '''
    Takes in coordinates for target location and prints:
    TARGET <lat> <lon>
    '''
    latitude = coord_tup[0]
    longitude = coord_tup[1]
    print("TARGET " + str(latitude) +" " + str(longitude))
    
def print_forecast_location(coord_tup: tuple[float]) -> None:
    '''
    Takes in coordinates for forecast location and prints:
    FORECAST <lat> <lon>
    '''
    latitude = coord_tup[0]
    longitude = coord_tup[1]
    print("FORECAST " + str(latitude) +" " + str(longitude))
    
def _check_status_error(error_msg: str):
    error_msg = str(error_msg)
    msg = error_msg.split(" ")
    print(error_msg) 
    if msg[0] == '200':
        print('INCOMPLETE')
    elif len(msg) == 1:
        print('NETWORK')
    else:
        print('NOT 200')
#----------------------------Main Function------------------------------
def run_program():
    try:
        location_target = get_target_location() 
        loc_coord = location_target.coordinates()
        
        weather_method = get_weather_method(location_target._raw_coord())
        forecast_location = weather_method.forecast_coordinates()

        queries_list = get_queries()              
        q = query_interface.Query(queries_list)    
        
        forecast_info = weather_method._get_url_content()
        answer_list=  q.get_query_answers(forecast_info)
        
        reverse_method = get_reverse_method(weather_method.raw_coordinates())  
        closest_station = reverse_method.get_location_name() 

        #Print expected outputs
        print_location_coordinates(loc_coord) 
        print_forecast_location(forecast_location)
        print(closest_station)
        for answer in answer_list:
            print(answer)
            
    except MissingFileError as e:
        print("FAILED")
        print(e)
        print("MISSING")   
    except FileFormatError as e:
        print("FAILED")
        print(e)
        print("FORMAT") 
    except Exception as e:
        print("FAILED") 
        _check_status_error(e)
    

#--------------------Run----------------
if __name__ == '__main__':
    run_program()