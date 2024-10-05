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
                "moon_phase",
                "day_max",
                "day_min"
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

        # Color the elements and calculate lengths
        temp_color = get_temp_color(temp)
        temp_len = len(f" {temp}󰔀")
        temp = colored(f" {temp}󰔀", temp_color)
        
        day_max_len = len(f"󰸂 {day_max}󰔀")
        day_max = colored(f"󰸃 {day_max}󰔀", "red")
        
        day_min_len = len(f"󰸂 {day_min}󰔀")
        day_min = colored(f"󰸂 {day_min}󰔀", "blue")
        
        weather_show = colored(f"{weather_data.kind} {weather_emoji(kind)[1]}", weather_emoji(kind)[2])
        weather_len = len(f"{weather_data.kind} {weather_emoji(kind)[1]}")
        
        humidity_len = len(f" {humidity}%")
        humidity = colored(f" {humidity}%", "green")
        
        precep_len = len(f"  {prec}mm")
        precep = colored(f"  {prec}mm", "blue")
        
        wind_speed = colored(f" {wind_speed}km/h", "cyan")
        wind_len = len(f" {wind_speed}km/h")
        
        moon_phase = colored(moon_emoji(phase), "yellow")
        moon_len = len(moon_emoji(phase))
        
        max_length = max(
            temp_len,
            day_max_len,
            day_min_len,
            weather_len,
            humidity_len,
            precep_len,
            wind_len,
            moon_len
        )
        bar_len = max_length + 2
        short_bar_len = max(day_min_len, wind_len)

        # Create a dictionary with all elements
        elements = {
            "temperature": temp,
            "weather": weather_show,
            "humidity": humidity,
            "precipitation": precep,
            "wind_speed": wind_speed,
            "moon_phase": moon_phase,
            "day_max": day_max,
            "day_min": day_min
        }

        # Print the weather info
        print(f"""
        ╭{"─"*short_bar_len}──┬{"─"*bar_len}───╮
        │ {elements[element_order[0]]} {" "*(short_bar_len - len(elements[element_order[0]]))}│ {elements[element_order[1]]}  {" "*(bar_len - len(elements[element_order[1]]))}│
        │ {elements[element_order[2]]} {" "*(short_bar_len - len(elements[element_order[2]]))}│ {elements[element_order[3]]}  {" "*(bar_len - len(elements[element_order[3]]))}│
        │ {elements[element_order[4]]} {" "*(short_bar_len - len(elements[element_order[4]]))}│ {elements[element_order[5]]}  {" "*(bar_len - len(elements[element_order[5]]))}│
        │ {elements[element_order[6]]} {" "*(short_bar_len - len(elements[element_order[6]]))}│ {elements[element_order[7]]}  {" "*(bar_len - len(elements[element_order[7]]))}│
        ╰{"─"*short_bar_len}──┴{"─"*bar_len}───╯
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
