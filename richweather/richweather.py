#!/usr/bin/env python
import argparse
import asyncio
import os

import grapheme
import python_weather
from termcolor import colored
import yaml


# Declare Moon Phases
phases = [phase for phase in python_weather.enums.Phase]
emojis = ["", "", "", "", "", "", "", ""]


def read_config():
    config_path = os.path.expanduser("~/.config/richweather/richweather.yaml")
    
    try:
        with open(config_path, 'r') as stream:
            return yaml.safe_load(stream)
    except FileNotFoundError:
        print(colored("Configuration file not found. Using defaults.", "yellow"))
        return {
            "default_city": "Ottawa",
            "element_order": [
                "temperature",
                "day_max",
                "day_min",
                "wind_speed",
                "weather",
                "humidity",
                "precipitation",
                "moon_phase"
            ]
        }


def moon_emoji(phase):
    """
    Returns emoji for moon phase.
    """
    return f"{phase} {emojis[phases.index(phase)]}"


def get_temp_color(temp):
    """
    Gets color for temp display
    """
    if temp <= 28:
        return "blue"
    elif 28 < temp <= 30:
       return "yellow"
    else:
        return "red"


def weather_emoji(weather):
    """
    Gets color and emoji for weather display.
    """

    if weather == python_weather.enums.Kind.CLOUDY:
        return [weather, "", "light_grey"]
    elif weather == python_weather.enums.Kind.FOG:
        return [weather, "󰖑", "light_grey"]
    elif weather == python_weather.enums.Kind.HEAVY_RAIN:
        return [weather, "", "blue"]
    elif weather == python_weather.enums.Kind.HEAVY_SHOWERS:
        return [weather, "", "blue"]
    elif weather == python_weather.enums.Kind.HEAVY_SNOW:
        return [weather, "󰖘", "blue"]
    elif weather == python_weather.enums.Kind.HEAVY_SNOW_SHOWERS:
        return [weather, "", "blue"]
    elif weather == python_weather.enums.Kind.LIGHT_RAIN:
        return [weather, "", "cyan"]
    elif weather == python_weather.enums.Kind.LIGHT_SHOWERS:
        return [weather, "", "cyan"]
    elif weather == python_weather.enums.Kind.LIGHT_SLEET:
        return [weather, "", "cyan"]
    elif weather == python_weather.enums.Kind.LIGHT_SLEET_SHOWERS:
        return [weather, "", "cyan"]
    elif weather == python_weather.enums.Kind.LIGHT_SNOW:
        return [weather, "󰖘", "cyan"]
    elif weather == python_weather.enums.Kind.LIGHT_SNOW_SHOWERS:
        return [weather, "", "cyan"]
    elif weather == python_weather.enums.Kind.PARTLY_CLOUDY:
        return [weather, "", "light_grey"]
    elif weather == python_weather.enums.Kind.SUNNY:
        return [weather, "", "yellow"]
    elif weather == python_weather.enums.Kind.THUNDERY_HEAVY_RAIN:
        return [weather, "", "cyan"]
    elif weather == python_weather.enums.Kind.THUNDERY_SHOWERS:
        return [weather, "", "cyan"]
    elif weather == python_weather.enums.Kind.THUNDERY_SNOW_SHOWERS:
        return [weather, "", "cyan"]
    elif weather == python_weather.enums.Kind.VERY_CLOUDY:
        return [weather, "", "light_grey"]
    else:
        return weather


async def weather(location, element_order):
    async with python_weather.Client() as client:
        # Fetch a weather forecast from a city
        weather = await client.get(location)

        # Get all the required info
        n = True
        for daily in weather.daily_forecasts:
            while n:
                temp = weather.temperature
                humidity = weather.humidity
                prec = weather.precipitation
                day_max = daily.highest_temperature
                day_min = daily.lowest_temperature
                phase = daily.moon_phase
                kind = weather.kind
                wind_speed = weather.wind_speed
                n = False

        # Color the stuff and find lengths
        temp_color = get_temp_color(temp)
        temp_len = len(f" {temp}°C")
        temp = colored(f" {temp}°C", temp_color)
        day_max_len = len(f"󰸂 {day_max}°C")
        day_max = colored(f"󰸃 {day_max}°C", "red")
        day_min_len = len(f"󰸂 {day_min}°C")
        day_min = colored(f"󰸂 {day_min}°C", "blue")
        weather_show = colored(f"{weather.kind} {weather_emoji(kind)[1]}", weather_emoji(kind)[2])
        weather_len = len(f"{weather.kind} {weather_emoji(kind)[1]}")
        humidity_len = len(f" {humidity}%")
        humidity = colored(f" {humidity}%", "green")
        precep_len = len(f"  {prec}mm")
        precep = colored(f"  {prec}mm", "blue")
        # print(wind_speed)
        wind_len = len(str(wind_speed)) + 6 #Calculating the lengths of this one is really weird for some reason because of the colors and emojis and stuff.
        wind_speed = colored(f" {wind_speed}km/h", "cyan")
        moon_phase = colored(moon_emoji(phase), "yellow")
        moon_len = len(moon_emoji(phase))
        # print(wind_len)
        
        # Bar lengths for bars and spaces
        lengths = {
            "temperature": temp_len,
            "weather": weather_len,
            "humidity": humidity_len,
            "precipitation": precep_len,
            "wind_speed": wind_len,
            "moon_phase": moon_len,
            "day_max": day_max_len,
            "day_min": day_min_len
        }
        
        # Create a dictionary with all elements
        colored_elements = {
            "temperature": temp,
            "weather": weather_show,
            "humidity": humidity,
            "precipitation": precep,
            "wind_speed": wind_speed,
            "moon_phase": moon_phase,
            "day_max": day_max,
            "day_min": day_min
        }
        
        # Calculate max values for each side based on element_order
        left_side_elements = [colored_elements[element_order[i]] for i in range(0, 4)]
        right_side_elements = [colored_elements[element_order[i]] for i in range(4, 8)]

        max_left_side = max(lengths[element_order[i]] for i in range(0, 4))
        max_right_side = max(lengths[element_order[i]] for i in range(4, 8)) 


        # print(max_right_side)
        # print(max_left_side)
        #If it works it works, please dont touch this unless you know what you are doing
        #This is really hacky and static because max_left_side and max_right side arent calculated dynamically because doing so is a big pain.
        print(f"""
  ╭─{"─"*(max_left_side)}──┬{"─"*(max_right_side)}───╮
  │ {left_side_elements[0]} {" "*((max_left_side - lengths[element_order[0]]))} │ {right_side_elements[0]} {" "*((max_right_side - lengths[element_order[4]]))} │
  │ {left_side_elements[1]} {" "*((max_left_side - lengths[element_order[1]]))} │ {right_side_elements[1]} {" "*((max_right_side - lengths[element_order[5]]))} │
  │ {left_side_elements[2]} {" "*((max_left_side - lengths[element_order[2]]))} │ {right_side_elements[2]} {" "*((max_right_side - lengths[element_order[6]]))} │
  │ {left_side_elements[3]} {" "*((max_left_side - lengths[element_order[3]]))} │ {right_side_elements[3]} {" "*((max_right_side - lengths[element_order[7]]))} │
  ╰─{"─"*(max_left_side)}──┴{"─"*(max_right_side)}───╯
        """)


def main():
    
    config = read_config()
    # argparse stuff
    parser = argparse.ArgumentParser(description="Get weather information for a specific location.")
    parser.add_argument("location", nargs="?", help="The desired location (optional)")

    args = parser.parse_args()
    
    if not args.location:
        args.location = config["default_city"]
    # see https://stackoverflow.com/questions/45600579/asyncio-event-loop-is-closed-when-getting-loop
    # for more details

    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # Running the thing
    try:
        asyncio.run(weather(args.location, config["element_order"]))
    except python_weather.errors.Error:
        print(colored("Please enter a cityname in this format: richweather <city>", "red"))


if __name__ == "__main__":
    main()
