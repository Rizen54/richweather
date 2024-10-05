#!/usr/bin/env python
import argparse
import python_weather
from termcolor import colored
import asyncio
import os

# Declare Moon Phases
phases = [phase for phase in python_weather.enums.Phase]
emojis = ["", "", "", "", "", "", "", ""]


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


async def weather(location="Delhi"):
    async with python_weather.Client() as client:
        # Fetch a weather forecast from a city
        weather = await client.get(location)

        # Get all the reqd info
        n = True
        for daily in weather.daily_forecasts:
            while n:
                temp = weather.temperature
                # feel = weather.feels_like

                humidity = weather.humidity
                prec = weather.precipitation
                day_max = daily.highest_temperature
                day_min = daily.lowest_temperature

                phase = daily.moon_phase
                kind = weather.kind
                n = False


        # Color the stuff and find lengths
        temp_color = get_temp_color(temp)
        temp_len = len(f" {temp}󰔄")
        temp = colored(f" {temp}󰔄", temp_color)
        day_max_len = len(f"󰸂 {day_max}󰔄")
        day_max = colored(f"󰸃 {day_max}󰔄", "red")
        day_min_len = len(f"󰸂 {day_min}󰔄")
        day_min = colored(f"󰸂 {day_min}󰔄", "blue")
        weather_show = colored(f"{weather.kind} {weather_emoji(kind)[1]}", weather_emoji(kind)[2])
        weather_len = len(f"{weather.kind} {weather_emoji(kind)[1]}")
        humidity_len = len(f" {humidity}%")
        humidity = colored(f" {humidity}%", "green")
        precep_len = len(f"  {prec}mm")
        precep = colored(f"  {prec}mm", "blue")
        wind_speed = colored(f" {weather.wind_speed}km/h", "cyan")
        wind_len = len(f" {weather.wind_speed}km/h")
        moon_phase = colored(moon_emoji(phase), "yellow")
        moon_len = len(moon_emoji(phase))


        # Bar lengths for bars and spaces
        if weather_len > moon_len:
            bar_len = weather_len
        else:
            bar_len = moon_len

        if day_min_len > wind_len:
            short_bar_len = day_min_len
        else:
            short_bar_len = wind_len


        #Finally, print the stufff
        print(f"""
  ╭{"─"*short_bar_len}──┬{"─"*bar_len}───╮
  │ {temp} {" "*(short_bar_len - temp_len)}│ {weather_show}  {" "*(bar_len - weather_len)}│
  │ {day_max} {" "*(short_bar_len - day_max_len)}│ {humidity}  {" "*(bar_len - humidity_len)}│
  │ {day_min} {" "*(short_bar_len - day_min_len)}│ {precep}  {" "*(bar_len - precep_len)}│
  │ {wind_speed} {" "*(short_bar_len - wind_len)}│ {moon_phase}  {" "*(bar_len - moon_len)}│
  ╰{"─"*short_bar_len}──┴{"─"*bar_len}───╯
        """)


def main():
    # argparse stuff
    parser = argparse.ArgumentParser(description="Get weather information for a specific location.")
    parser.add_argument("location", nargs="?", help="The desired location (optional)")

    args = parser.parse_args()

    # see https://stackoverflow.com/questions/45600579/asyncio-event-loop-is-closed-when-getting-loop
    # for more details

    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # Running the thing
    try:
        asyncio.run(weather(location=args.location))
    except python_weather.errors.Error:
        print(colored("Please enter a cityname in this format: richweather <city>", "red"))

if __name__ == "__main__":
    main()
