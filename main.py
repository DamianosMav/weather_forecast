import tkinter as tk
import requests

API_KEY = "your_api_key_here"


def Submit(data):
    city_country_code = data.split(",")
    cleaned_data = []

    for city_country in city_country_code:
        cleaned_data.append(city_country.strip())

    if len(cleaned_data) != 2:
        print("Please enter a valid city and country code")
        return
    
    city, country_code = cleaned_data[0].lower(), cleaned_data[1].lower()

    get_weather(city, country_code)

def get_weather(city, country_code):
    result = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&appid={API_KEY}")

    if result:
        json = result.json()
        weather = json["weather"][0]["main"]
        weather_description = json["weather"][0]["description"]
        temperature_f = round(json["main"]["temp"] * (9/5) - 459.67)
        temperature_c = round((temperature_f - 32) / (9/5))
        humidity = json["main"]["humidity"]
        wind_speed = json["wind"]["speed"]

        forecast_text = (
                            f"Current weather: {weather} - {weather_description}\n"
                            f"Temperature in Fahrenheit: {temperature_f}°F\n"
                            f"Temperature in Celsius: {temperature_c}°C\n"
                            f"Current humidity: {humidity}%\n"
                            f"Current wind speed: {wind_speed} km/h"
                        )
        forecast.set(forecast_text)

    

app = tk.Tk(screenName=None, baseName=None, useTk=1)
app.title("Weather Forecast")
app.geometry("400x400")
app.resizable(False, False)

app.columnconfigure((1,2,3), weight=1, uniform="a")

city_country_code = tk.StringVar()
forecast = tk.StringVar()

label = tk.Label(app, text="Enter the name of you city and country code")
label_forecast = tk.Label(app, textvariable=forecast, justify="left")
entry = tk.Entry(app, justify="center", textvariable= city_country_code)

entry.insert(0, "Athens, gr")

btn = tk.Button(app, text="Submit", command=lambda:Submit(city_country_code.get()))


label.grid(row=0, column=1, columnspan=2, ipadx=60)
entry.grid(row=1, column=1,columnspan=2, sticky="ns")
btn.grid(row=2,column=1, columnspan=2)
label_forecast.grid(row=3, column=1, columnspan=2)

app.mainloop()