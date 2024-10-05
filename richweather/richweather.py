#!/usr/bin/env python
import argparse
import python_weather
from termcolor import colored
import asyncio
import os

# Declare Moon Phases
phases = [phase for phase in python_weather.enums.Phase]
emojis = ["", "", "", "", "", "", "", ""]
def read_config():
    config_path = os.path.expanduser("~/.config/richweather.yaml")
    
    try:
        with open(config_path, 'r') as stream:
            return yaml.safe_load(stream)
    except FileNotFoundError:
        print(colored("Configuration file not found. Using defaults.", "yellow"))
        return {
            "default_city": "Ottawa",
            "element_order": [
                "temperature",
                "weather",
                "humidity",
                "precipitation",
                "wind_speed",
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
        weather_data = await client.get(location)

        # Get all the required info
        n = True
        for daily in weather_data.daily_forecasts:
            while n:
                temp = weather_data.temperature
                humidity = weather_data.humidity
                prec = weather_data.precipitation
                day_max = daily.highest_temperature
                day_min = daily.lowest_temperature
                phase = daily.moon_phase
                kind = weather_data.kind
                wind_speed = weather_data.wind_speed
                n = False

        # Create a dictionary with all elements
        elements = {
            "temperature": f" {temp}󰔄",
            "weather": f"{weather_data.kind} {weather_emoji(kind)[1]}",
            "humidity": f" {humidity}%",
            "precipitation": f"  {prec}mm",
            "wind_speed": f" {wind_speed}km/h",
            "moon_phase": moon_emoji(phase)
        }

        # Color the elements
        colored_elements = {}
        for elem, value in elements.items():
            if elem == "temperature":
                color = get_temp_color(temp)
            elif elem == "weather":
                color = weather_emoji(kind)[2]
            elif elem == "humidity":
                color = "green"
            elif elem == "precipitation":
                color = "blue"
            elif elem == "wind_speed":
                color = "cyan"
            elif elem == "moon_phase":
                color = "yellow"
            colored_elements[elem] = colored(value, color)

        # Determine bar lengths
        max_len = max(len(colored_elements[elem]) for elem in element_order)
        short_bar_len = len(f"{colored_elements['temperature']} {' '*(max_len - len(colored_elements['temperature']))}")

        # Print the weather info
        print(f"""
  ╭{"─"*short_bar_len}──┬{"─"*max_len}───╮
  │ {colored_elements[element_order[0]]} {" "*(short_bar_len - len(colored_elements[element_order[0]]))}│ {colored_elements[element_order[1]]}  {" "*(max_len - len(colored_elements[element_order[1]]))}│
  │ {colored_elements[element_order[2]]} {" "*(short_bar_len - len(colored_elements[element_order[2]]))}│ {colored_elements[element_order[3]]}  {" "*(max_len - len(colored_elements[element_order[3]]))}│
  │ {colored_elements[element_order[4]]} {" "*(short_bar_len - len(colored_elements[element_order[4]]))}│ {colored_elements[element_order[5]]}  {" "*(max_len - len(colored_elements[element_order[5]]))}│
  ╰{"─"*short_bar_len}──┴{"─"*max_len}───╯
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
