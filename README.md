# Weather Forecast CLI
 
A multi-module Python command-line app that takes a U.S. location and answers questions about its real-time hourly forecast. It uses the Nominatim (OpenStreetMap) API to turn a place name into coordinates, queries the National Weather Service (NWS) API for the hourly forecast, and parses the JSON responses to answer queries like "what is the highest air temperature over the next 12 hours?"
 
Every data source can come from a live API or from a saved file, which makes the program easy to test without network access.
 
## Requirements
 
- Python 3.10 or newer (the code uses `X | Y` type hints)
- An internet connection when using the live APIs
## How to run
 
The program reads its configuration from standard input, one line at a time, with no prompts. Save your input in a text file and run:
 
```
python project3.py < sample_input.txt
```
 
or run `python project3.py` and type the lines yourself.
 
### Input format
 
1. **Target location:** `TARGET NOMINATIM <place name>` or `TARGET FILE <path>`
2. **Forecast source:** `WEATHER NWS` or `WEATHER FILE <path>`
3. **Queries:** zero or more lines (see below), then `NO MORE QUERIES`
4. **Reverse geocoding:** `REVERSE NOMINATIM` or `REVERSE FILE <path>`
### Queries
 
| Query | Format |
|---|---|
| Air temperature | `TEMPERATURE AIR <F\|C> <hours> <MIN\|MAX>` |
| Feels-like temperature | `TEMPERATURE FEELS <F\|C> <hours> <MIN\|MAX>` |
| Humidity | `HUMIDITY <hours> <MIN\|MAX>` |
| Wind speed | `WIND <hours> <MIN\|MAX>` |
| Precipitation chance | `PRECIPITATION <hours> <MIN\|MAX>` |
 
`<hours>` is the number of upcoming hourly forecast periods to search. Each answer is the UTC timestamp of the minimum or maximum value, followed by the value (four decimal places).
 
## Example
 
Input (`sample_input.txt`):
 
```
TARGET NOMINATIM Bren Hall, Irvine, CA
WEATHER NWS
TEMPERATURE AIR F 12 MAX
HUMIDITY 12 MIN
NO MORE QUERIES
REVERSE NOMINATIM
```
 
Output:
 
```
TARGET 33.6432477/N 117.841865/W
FORECAST 33.65455/N 117.83292500000002/W
California Avenue, Regents Point, University Town Center, Irvine, Orange County, California, 92612, United States
2026-11-14T22:00:00Z 72.0000
2026-11-14T22:00:00Z 58.0000%
```
 
The first line is the coordinates of the target location, the second is the coordinates of the NWS forecast point, the third is the name of the place nearest the forecast point, and the rest are the query answers in the order they were entered. Output depends on live forecast data, so your numbers will differ.
 
## Error handling
 
If an API request fails or a file is missing or badly formatted, the program prints `FAILED`, followed by the cause (for example `MISSING`, `FORMAT`, or `NOT 200`) instead of the normal output.
 
## Project structure
 
| File | Purpose |
|---|---|
| `project3.py` | Entry point: reads input, runs the pipeline, prints results |
| `fetching_interface.py` | Classes for forward geocoding, forecasts, and reverse geocoding, each with an API version and a file version |
| `fetching_func.py` | Helper functions for fetching and parsing data |
| `query_interface.py` | Parses and validates query lines and produces answers |
| `weather_class_interface.py` | Extracts temperature, humidity, wind, and precipitation from the forecast JSON and computes min/max and feels-like values |
 
## Built with
 
Python, REST APIs, HTTP, JSON, [National Weather Service API](https://www.weather.gov/documentation/services-web-api), [Nominatim](https://nominatim.org/release-docs/latest/api/Overview/)
 
## Background
 
This project was based on a UCI ICS 32 course project about using web APIs and geocoding in Python. I adapted it to use weather forecast data.
 
