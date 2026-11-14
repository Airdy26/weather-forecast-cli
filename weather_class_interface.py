'''
Module of WeatherAttribute Class
This class is used to get a specific attributes from a weather info list of dictionaries. 
Mainly used in query interface to get temp, humidity, wind speed, and percipitation 
information, lists, and query answers (formatted) easily
'''
from datetime import datetime
from datetime import timezone


class WeatherAttribute():
    def __init__(self, forecast_list: list) -> None:
        '''
        Initializes all types of list to be accessed from 
        forecast list
        '''
        self._forecast_list = forecast_list
        self._temp_list = _get_temp_list(self._forecast_list)
        self._hum_list = _get_humidity_list(self._forecast_list)
        self._wind_list = _get_wind_list(self._forecast_list)
        self._prec_list = _get_prec_list(self._forecast_list)
        
    def get_temp_list(self, length: int):
        'Returns air temperature list up to given length'
        list = _limit_weather_char_dict(length, self._temp_list)
        return list
    
    def get_humidity_list(self, length: int):
        'Returns humidity list up to given length'
        list = _limit_weather_char_dict(length, self._hum_list)
        return list
    
    def get_wind_list(self, length: int):
        'Returns wind speed list up to given length' 
        list = _limit_weather_char_dict(length, self._wind_list)
        return list
    
    def get_air_temperature_ans(self, info_dict: list) -> str:
        '''
        Returns date with min or max air temperature as a string
        Answer for AIR TEMP query
        '''
        limited_temp_list = _limit_weather_char_dict(info_dict.length, self._temp_list)
        ext_temp = _get_extrema_temp_ans(info_dict, limited_temp_list, self._forecast_list)
        return ext_temp
    
    def get_raw_air_temperature(self, info_dict) -> float:
        '''
        Returns raw unrounded extrema temperature
        '''
        limited_temp_list = _limit_weather_char_dict(info_dict.length, self._temp_list)
        return _get_raw_extrema_temp(info_dict, limited_temp_list, self._forecast_list)
    
    def get_humidity_ans(self, info_dict) -> str:
        '''
        Returns date with humidity % answer as a string
        Answer for humdity query 
        '''
        limited_humidity_list = _limit_weather_char_dict(info_dict.length, self._hum_list)
        ext_humidity = _get_extrema_humidity_ans(info_dict, limited_humidity_list, self._forecast_list)
        return ext_humidity
    
    def get_raw_humidity(self, info_dict) -> float:
        limited_humidity_list = _limit_weather_char_dict(info_dict.length, self._hum_list)
        return get_raw_extrema_humidity(info_dict, limited_humidity_list, self._forecast_list)
    
    def get_wind_speed_ans(self,info_dict)-> str:
        '''
        Returns date with wind speed mp/h answer as a string
        Answer for windspeed query
        '''
        limited_wind_list = _limit_weather_char_dict(info_dict.length, self._wind_list)
        ext_wind = _get_extrema_wind_ans(info_dict, limited_wind_list, self._forecast_list)
        return ext_wind
    
    def get_raw_wind(self, info_dict) -> float:
        '''
        Returns raw unrounded extrema wind speed
        '''
        limited_wind_list = _limit_weather_char_dict(info_dict.length, self._wind_list)
        return get_raw_extrema_wind(info_dict, limited_wind_list, self._forecast_list)

    def _get_percipitation_ans(self, info_dict) -> str:
        '''
        Returns date with percipitation chance with % as a string
        Answer for precipitation query
        '''
        limited_prec_list = _limit_weather_char_dict(info_dict.length, self._prec_list)
        ext_prec = _get_extrema_percipitation_ans(info_dict, limited_prec_list, self._forecast_list)
        return ext_prec
        
        
    def _calc_feels_temp_ans(self, info_dict: list) -> tuple[int, float]:
        '''
        Calculates feel like temperature in the range of user length provided
        It also looks for extrema feels like temperature
        Returns answer to feels temp query as string
        '''
        length = int(info_dict.length)
        air_temp_list = _limit_weather_char_dict(length, self._temp_list)
        hum_list = _limit_weather_char_dict(length, self._hum_list)
        wind_list = _limit_weather_char_dict(length, self._wind_list)
        feels_list = _get_feels_list(length, air_temp_list, hum_list, wind_list)
            
        extrema_temp = max(feels_list)
        extrema_period = feels_list.index(extrema_temp)
        
        start_time = self._forecast_list["properties"]["periods"][extrema_period]["startTime"] 
        if info_dict.scale == "C":
            converted_temp = (extrema_temp - 32) * (5/9)
            extrema_temp = converted_temp
        rounded_temp = round(extrema_temp, 4)
        
        formatted_time = _convert_time(start_time)
        extrema_string = formatted_time + ' ' + str(f"{rounded_temp:.4f}")
        
        return extrema_string
        
#-----------------------------Main functions----------------------------------------#

#-------------------------------List Functions--------------------------------------
def _get_temp_list(forecast_list: list) -> dict:
    '''
    Makes a dictionary with period as keys and temp as values
    Returns dictionary
    '''
    periods = forecast_list["properties"]["periods"]
    count = 0
    temp_dict = dict()
    while count != len(periods):
        characteristic = forecast_list["properties"]["periods"][count]["temperature"]
        temp_dict[count] = characteristic
        count += 1
        
    return temp_dict

def _get_humidity_list(forecast_list: list) -> dict:
    '''
    Makes a dictionary with period as keys and humidity as values
    Returns dictionary
    '''
    periods = forecast_list["properties"]["periods"]
    count = 0
    temp_dict = dict()
    while count != len(periods):
        characteristic = forecast_list["properties"]["periods"][count]["relativeHumidity"]["value"]
        temp_dict[count] = characteristic
        count += 1
        
    return temp_dict

def _get_wind_list(forecast_list: list) -> dict:
    '''
    Makes a dictionary with period as keys and wind speed as values
    Returns dictionary
    '''
    periods = forecast_list["properties"]["periods"]
    count = 0
    wind_dict = dict()
    while count != len(periods):
        characteristic = forecast_list["properties"]["periods"][count]["windSpeed"]
        speed = characteristic.split(" ", 1)
        characteristic = speed[0]
        wind_dict[count] = characteristic
        count += 1
        
    return wind_dict

def _get_prec_list(forecast_list: list) -> dict:
    '''
    Makes a dictionary with period as keys and precipitation as values
    Returns dictionary
    '''
    periods = forecast_list["properties"]["periods"]
    count = 0
    prec_dict = dict()
    while count != len(periods):
        characteristic = forecast_list["properties"]["periods"][count]["probabilityOfPrecipitation"]["value"]
        prec_dict[count] = characteristic
        count += 1
        
    return prec_dict

def _get_feels_list(length: int, air_temp_list, hum_list, wind_list) -> list:
    '''
    Returns a new "temp feels" list from calculations
    '''
    feels_list = []
    count = 0
    while count != length:
        if air_temp_list[count] >= 68:
            temp = use_heat_index(air_temp_list[count], hum_list[count])
        elif float(air_temp_list[count]) <= 50 and float(wind_list[count]) > 3:
            temp = use_wind_chill(air_temp_list[count], wind_list[count])
        else:
            temp = air_temp_list[count]
        feels_list.append(temp)
        count += 1
    return feels_list
#------------------------------Get formatted answer functions------------------------------------
def _get_extrema_temp_ans(info_list: list, weather_dict: dict ,forecast_list: list) -> str:
    '''
    Gets complete extrema temperature (with time)
    Used for air temp and feels temp
    With start time and numbers with 4 decimals
    Returns complete info as str
    '''
    period_extrema = _get_extrema_period(info_list.limit, weather_dict) 
    start_time = forecast_list["properties"]["periods"][period_extrema]["startTime"] 
    extrema_temp = forecast_list["properties"]["periods"][period_extrema]["temperature"]
    if info_list.scale == "C":
        converted_temp = (extrema_temp - 32) * (5/9)
        extrema_temp = converted_temp
    rounded_temp = round(extrema_temp, 4)
    
    formatted_time = _convert_time(start_time)
    extrema_string = formatted_time + ' ' + str(f"{rounded_temp:.4f}")
    
    return extrema_string

def _get_extrema_humidity_ans(info_list: list, weather_dict: dict ,forecast_list: list) -> str:
    '''
    Gets complete extrema humidity (with time)
    Used for humidity query
    With start time and numbers with 4 decimals and %
    Returns complete info as str
    '''
    period_extrema = _get_extrema_period(info_list.limit, weather_dict) 
    start_time = forecast_list["properties"]["periods"][period_extrema]["startTime"] 
    extrema_hum = forecast_list["properties"]["periods"][period_extrema]["relativeHumidity"]["value"]
    rounded_hum = round(extrema_hum, 4)
    
    formatted_time = _convert_time(start_time)
    extrema_string = formatted_time + ' ' + str(f"{rounded_hum:.4f}" + "%")
    
    return extrema_string

def _get_extrema_wind_ans(info_list: list, weather_dict: dict ,forecast_list: list) -> str:
    '''
    Gets complete extrema wind speed (with time)
    Used for wind query
    With start time and numbers with 4 decimals and mp/h
    Returns complete info as str
    '''
    period_extrema = _get_extrema_period(info_list.limit, weather_dict) 
    start_time = forecast_list["properties"]["periods"][period_extrema]["startTime"] 
    extrema_wind = forecast_list["properties"]["periods"][period_extrema]["windSpeed"]
    speed = extrema_wind.split(' ')
    extrema_wind = float(speed[0])
    rounded_wind = round(extrema_wind, 4)
    
    formatted_time = _convert_time(start_time)
    extrema_string = formatted_time + ' ' + str(f"{rounded_wind:.4f}" + " mp/h")
    
    return extrema_string

def _get_extrema_percipitation_ans(info_list: list, weather_dict: dict ,forecast_list: list) -> str:
    '''
    Gets complete extrema precipitation chance (with time)
    Used for precipitation query
    With start time and numbers with 4 decimals and %
    Returns complete info as str
    '''
    period_extrema = _get_extrema_period(info_list.limit, weather_dict) 
    start_time = forecast_list["properties"]["periods"][period_extrema]["startTime"] 
    extrema_prec = forecast_list["properties"]["periods"][period_extrema]["probabilityOfPrecipitation"]["value"]
    rounded_prec = round(extrema_prec, 4)
    
    formatted_time = _convert_time(start_time)
    extrema_string = formatted_time + ' ' + str(f"{rounded_prec:.4f}" + "%")
    
    return extrema_string
#----------------------------Functions for raw float values----------------------------------
def _get_raw_extrema_temp(info_list: list, weather_dict: dict ,forecast_list: list) -> float:
    '''
    Gets min or max temp non-rounded
    Returns float
    '''
    period_extrema = _get_extrema_period(info_list.limit, weather_dict) 
    extrema_temp = forecast_list["properties"]["periods"][period_extrema]["temperature"]
    if info_list.scale == "C":
        converted_temp = (extrema_temp - 32) * (5/9)
        extrema_temp = converted_temp
    return extrema_temp

def get_raw_extrema_humidity(info_list: list, hum_dict: dict ,forecast_list: list) -> float:
    '''
    Gets min or max of humidity raw
    Returns float
    '''
    period_extrema = _get_extrema_period(info_list.limit, hum_dict)
    extrema_humidity = forecast_list["properties"]["periods"][period_extrema]["relativeHumidity"]["value"]
    return extrema_humidity

def get_raw_extrema_precipitation(info_list: list, prec_dict: dict ,forecast_list: list) -> float:
    '''
    Gets min or max of precipitation raw
    Returns float
    '''
    period_extrema = _get_extrema_period(info_list.limit, prec_dict)
    extrema_prec = forecast_list["properties"]["periods"][period_extrema]["probabilityOfPrecipitation"]["value"]
    return extrema_prec
def get_raw_extrema_wind(info_list: list, wind_dict: dict ,forecast_list: list) -> float:
    '''
    Gets min or max of wind speed raw
    Returns float
    '''
    period_extrema = _get_extrema_period(info_list.limit, wind_dict)
    extrema_wind = forecast_list["properties"]["periods"][period_extrema]["windSpeed"]
    return extrema_wind
#-------------------------Helper Functions---------------------------------------
def _get_extrema_period(extrema: str, weather_dict: dict) -> int: 
    '''
    Gets the period with the min or max description
    (temp, humidity, wind, etc)
    Returns int
    '''
    period = 0
    if extrema == "MAX":
        period = max(weather_dict, key=weather_dict.get)
    elif extrema == "MIN":
        period = min(weather_dict, key=weather_dict.get)
    return period

def _limit_weather_char_dict(length: int, characteristic_dict: dict) -> dict:
    '''
    Used to cut original characteristic dict into length that user requested
    Returns new reduced dictionary
    '''
    length = int(length)
    new_dict = dict(list(characteristic_dict.items())[:length])
    return new_dict
    
def _convert_time(original_time: str) -> str:
    '''
    Converts time to UTC time zone in ISO 8601 format 
    Uses time from file/url startTime
    ''' 
    offset_time = datetime.fromisoformat(original_time)
    utc_time = offset_time.astimezone(timezone.utc)
    formatted_time = utc_time.isoformat().replace("+00:00", "Z")
    
    return formatted_time

def use_heat_index(air_temp: float, humidity: float) -> int:
    '''
    Computes feels like temerature with heat index method
    Returns unrounded float 
    '''
    sum = 0
    addends = [-42.379, (2.04901523 * air_temp), (10.14333127 * humidity), (-0.22475541 * air_temp * humidity),
               (-0.00683783 * (air_temp*air_temp)), (-0.05481717 * (humidity*humidity)), (0.00122874 * (air_temp*air_temp) * humidity),
               (0.00085282 * air_temp *(humidity*humidity)), (-0.00000199 * (air_temp*air_temp) * (humidity*humidity))] 
    
    for elem in addends:
        sum += elem
    return sum

def use_wind_chill(air_temp: float, wind: float):
    '''
    Computes feels like temperature with wind chill method
    Returns unrounded float
    '''
    sum = 0
    addends = [(35.74), (0.6215 * air_temp), (-35.75 * (wind ** 0.16)), (0.4275 * air_temp * (wind ** 0.16))]
    
    for elem in addends:
        sum  += elem
