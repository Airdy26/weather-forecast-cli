'''
Inteface for Classes used in Forward Geocode, Hourly Weather, 
Weather Queries, and Reverse Nominatim. 
'''
import fetching_func
import API_request

FORWARD_GEO_BASE_URL =  "https://nominatim.openstreetmap.org/search?"
REVERSE_GEO_BASE_URL = "https://nominatim.openstreetmap.org/reverse?"
NWS_FORECAST_BASE_URL = "https://api.weather.gov/points/"

#-----------Classes for Forward Geocode------------
class File_ForwardGeocode():
    def __init__(self, file_name: str) -> None:
        '''Sets up file name and its contents as list'''
        self._target_file_name =  fetching_func._extract_key_two(file_name)
        self._file_contents = fetching_func._open_json_file(self._target_file_name)
        
    def coordinates(self) -> tuple[str]:
        '''Returns lon and lat as tuple from file'''
        formatted_coord = get_coordinates(self._file_contents)
        return fetching_func._convert_coordinates(formatted_coord)
    
    def _raw_coord(self) -> tuple[float]:
        '''Returns raw coordinates as a tuple'''
        return get_coordinates(self._file_contents)
    
    def get_url(self):
        '''Returns file name'''
        return self._target_file_url
    
class API_ForwardGeocode():
    def __init__(self, location_desc: str) -> None:
        '''Setup to get encoded url with appropriate paramenters
        Uses API to get dictionary of location description _url_content'''
        self._target_name =  fetching_func._extract_key_two(location_desc)
        self._query_list = [('q', self._target_name)]
        self._target_file_url = API_request.generate_url_encoded(FORWARD_GEO_BASE_URL, self._query_list, ('format', 'jsonv2'))
        self._url_content = API_request.get_nominatim_info(self._target_file_url)
        
    def coordinates(self):
        '''Returns lon and lat as tuple from url, formatted'''
        formatted_coord = get_coordinates(self._url_content)
        return fetching_func._convert_coordinates(formatted_coord)
    
    def _raw_coord(self) -> tuple[float]:
        '''Returns raw coordinates as tuple'''
        return get_coordinates(self._url_content)
    
    def get_url(self):
        '''Returns url'''
        return self._target_file_url
    
#-----------Classes for Hourly Weather------------
class File_WeatherForecast():
    def __init__(self, file_name: str) -> None:
        '''Initializes weather forecast url and list'''
        self._weather_file = fetching_func._extract_key_two(file_name)
        self._file_list = fetching_func._open_json_file(self._weather_file)
        
    def forecast_coordinates(self) -> tuple[float]:
        '''
        Gets the average of coordinates for forecast coordinates
        from weather_file
        returns formatted coordinates
        '''
        formatted_coord = fetching_func._convert_coordinates(get_forecast_location(self._file_list))
        return formatted_coord
    
    def raw_coordinates(self) -> tuple[float]:
        '''Returns raw coordinates'''
        return get_forecast_location(self._file_list)
    
    def get_url(self):
        '''Returns file name'''
        return self._weather_file
    
    def _get_url_content(self):
        '''Returns content of file as dict'''
        return self._file_list
        
class API_WeatherForecast():
    def __init__(self, location_coords: tuple) -> None:
        '''
        Get url from NWS with /points/ in API
        Initialize weather_url to hourly forecast format from url
        weather_url uses /gridpoints/ for hourly forecast
        '''
        self._weather_url = _get_forecast_hourly_url_API(location_coords)
        self._file_list = fetching_func._open_json_url(self._weather_url)
        
    def forecast_coordinates(self) -> tuple[float]:
        '''
        Requests content of self._weather_url with API
        Initializes _file_list a list version of url after
        Get avg coordinate of forecast location
        Return formatted coordinates
        '''
        coords = fetching_func._convert_coordinates(get_forecast_location(self._file_list))
        return coords
    
    def raw_coordinates(self) -> tuple[float]:
        '''Returns raw coordinates from url list _file_list'''
        return get_forecast_location(self._file_list)
    
    def get_url(self):
        '''Returns url used'''
        return self._weather_file   

    def _get_url_content(self):
        '''Returns dictionary of url content'''
        return self._file_list 

#-------------------Classes for Reverse---------------------
class File_Reverse():
    def __init__(self, file_name: str) -> None:
        '''Initializes file name'''
        self.reverse_file =  fetching_func._extract_key_two(file_name)
        
    def get_location_name(self) -> str:
        '''Return display name of location from file'''
        self._file_contents = fetching_func._open_json_file(self.reverse_file)
        return coord_to_name_file(self._file_contents)
    
class API_Reverse():
    def __init__(self, coords: tuple[float]) -> None:
        '''Sets up url to be encoded with lat and lon
        saves in _target_file+url the encoded url'''
        lat, lon = coords
        self._query_list = [('lat', lat), ('lon', lon)]
        self._target_file_url = API_request.generate_url_encoded(REVERSE_GEO_BASE_URL, self._query_list, ('format', 'jsonv2'))
        
    def get_location_name(self) -> str:
        '''Calls nominatim API with _target_file_url to get file dict
        Returns display name from url dict'''
        location_dict = API_request.get_nominatim_info(self._target_file_url)
        location = coord_to_name_file(location_dict)
        return location
    
#------------------Functions---------------------#
def get_coordinates(target_file: str) -> tuple[str]:
    '''
    Gets lon and lat of location from target file/url
    Parameter must be a opened file/url
    '''
    lat = float(target_file[0]["lat"])
    lon = float(target_file[0]["lon"])
    
    return (lat, lon)

def get_forecast_location(forecast_loc_coords: list) -> tuple[float]:
    '''
    Finds average lat and lon from polygon in the forecast_loc coords list 
    Returns a tuple with new averaged coordinates not formatted
    '''
    coordinate_list = forecast_loc_coords["geometry"]["coordinates"][0]
    count = sum_lat = sum_lon = 0
    lat = []
    lon = []

    for coord_tup in coordinate_list:
    #Checks for uniqueness
        if coord_tup[0] not in lon and coord_tup[1] not in lat:
            lon.append(coord_tup[0])
            lat.append(coord_tup[1])
            sum_lon += coord_tup[0]
            sum_lat += coord_tup[1]
            count += 1

    avg_lon = sum_lon/count
    avg_lat = sum_lat/count
    return (avg_lat, avg_lon)

def coord_to_name_file(rev_dic) -> tuple[float]:
    '''
    Returns display name from reverse dictionary
    Either from local file or API url
    '''
    loc_name = rev_dic["display_name"]
    return loc_name

def _get_forecast_hourly_url_API(loc_coords: tuple[str]):
    '''
    Gets forecast hourly url from NWS with API
    Returns url
    '''
    lat, lon = loc_coords
    url = NWS_FORECAST_BASE_URL + str(lat) + ',' + str(lon)
    forecast_content = API_request.get_NWS_forecast(url)
    forecast_hourly_url = forecast_content["properties"]["forecastHourly"]
    return forecast_hourly_url
    