import argparse
import python_weather
from termcolor import colored
import asyncio
import os

phases = [phase for phase in python_weather.enums.Phase]
emojis = ["", "", "", "", "", "", "", ""]

def moon_emoji(phase):
    return f"{phase} {emojis[phases.index(phase)]}"

def weather_emoji(weather):
    if weather == python_weather.enums.Kind.CLOUDY:
        return f"{weather} "
    elif weather == python_weather.enums.Kind.FOG:
        return f"{weather} 󰖑"
    elif weather == python_weather.enums.Kind.HEAVY_RAIN:
        return f"{weather} "
    elif weather == python_weather.enums.Kind.HEAVY_SHOWERS:
        return f"{weather} "
    elif weather == python_weather.enums.Kind.HEAVY_SNOW:
        return f"{weather} 󰖘"
    elif weather == python_weather.enums.Kind.HEAVY_SNOW_SHOWERS:
        return f"{weather} "
    elif weather == python_weather.enums.Kind.LIGHT_RAIN:
        return f"{weather} "
    elif weather == python_weather.enums.Kind.LIGHT_SHOWERS:
        return f"{weather} "
    elif weather == python_weather.enums.Kind.LIGHT_SLEET:
        return f"{weather} "
    elif weather == python_weather.enums.Kind.LIGHT_SLEET_SHOWERS:
        return f"{weather} "
    elif weather == python_weather.enums.Kind.LIGHT_SNOW:
        return f"{weather} 󰖘"
    elif weather == python_weather.enums.Kind.LIGHT_SNOW_SHOWERS:
        return f"{weather} "
    elif weather == python_weather.enums.Kind.PARTLY_CLOUDY:
        return f"{weather} "
    elif weather == python_weather.enums.Kind.SUNNY:
        return f"{weather} "
    elif weather == python_weather.enums.Kind.THUNDERY_HEAVY_RAIN:
        return f"{weather} "
    elif weather == python_weather.enums.Kind.THUNDERY_SHOWERS:
        return f"{weather} "
    elif weather == python_weather.enums.Kind.THUNDERY_SNOW_SHOWERS:
        return f"{weather} "
    elif weather == python_weather.enums.Kind.VERY_CLOUDY:
        return f"{weather} "
    else:
        return weather


async def weather(location="Delhi"):
    async with python_weather.Client() as client:
        # fetch a weather forecast from a city
        weather = await client.get(location)

        n = True
        for daily in weather.daily_forecasts:
            while n:
                temp = weather.temperature
                feel = weather.feels_like

                humidity = weather.humidity
                prec = weather.precipitation
                day_max = daily.highest_temperature
                day_min = daily.lowest_temperature

                phase = daily.moon_phase
                kind = weather.kind
                n = False

        print(f"""{colored("[Orca]:", "red")} {colored("Here's today's forecast sir:", "green")}

{colored(f"Temperature: {temp}󰔄 Feels like {feel}󰔄", "yellow")}
{colored(f"Day max:      {day_max}󰔄", "red")}
{colored(f"Day min:      {day_min}󰔄", "blue")}

{colored(f"Humidity:     {humidity}%", "green")}
{colored(f"Precipitaion: {prec}mm", "blue")}

{colored(f"Moon:     {moon_emoji(phase)}", "yellow")}
{colored(f"Weather:  {weather_emoji(kind)}", "blue")}
""")


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Get weather information for a specific location.")
    parser.add_argument("location", nargs="?", help="The desired location (optional)")
    args = parser.parse_args()

    # see https://stackoverflow.com/questions/45600579/asyncio-event-loop-is-closed-when-getting-loop
    # for more details

    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(weather(location=args.location))
