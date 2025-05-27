import tkinter as tk
import requests

class WeatherApp:
    def __init__(self, root, api_key):
        self.root = root
        self.api_key = api_key

        # Set up UI
        self.root.title("Weather Forecast")
        self.root.geometry("400x400")
        self.root.resizable(False, False)
        self.root.columnconfigure((1, 2, 3), weight=1, uniform="a")

        # Variables
        self.city_country_code = tk.StringVar()
        self.forecast = tk.StringVar()

        # Widgets
        label = tk.Label(self.root, text="Enter your city and country code")
        entry = tk.Entry(self.root, justify="center", textvariable=self.city_country_code)
        entry.insert(0, "Athens, gr")

        submit_btn = tk.Button(
            self.root,
            text="Submit",
            command=self.submit_city
        )

        forecast_label = tk.Label(self.root, textvariable=self.forecast, justify="left")

        # Layout
        label.grid(row=0, column=1, columnspan=2, ipadx=60)
        entry.grid(row=1, column=1, columnspan=2, sticky="ns")
        submit_btn.grid(row=2, column=1, columnspan=2)
        forecast_label.grid(row=3, column=1, columnspan=2)

    def submit_city(self):
        """
        Handles the user input: parses and validates the city/country input.
        """
        raw_input = self.city_country_code.get()
        parts = [p.strip().lower() for p in raw_input.split(",")]

        if len(parts) != 2:
            self.forecast.set("⚠️ Please enter in format: City, CountryCode")
            return

        city, country_code = parts
        self.get_weather(city, country_code)

    def get_weather(self, city, country_code):
        """
        Fetches weather data from OpenWeatherMap API and updates the forecast string.
        """
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&appid={self.api_key}"
        try:
            response = requests.get(url)
            data = response.json()

            # Extract weather details
            weather = data["weather"][0]["main"]
            description = data["weather"][0]["description"]
            temp_f = round(data["main"]["temp"] * (9 / 5) - 459.67)
            temp_c = round((temp_f - 32) * 5 / 9)
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]

            # Update forecast text
            forecast_msg = (
                f"Current weather: {weather} - {description}\n"
                f"Temp: {temp_f}°F / {temp_c}°C\n"
                f"Humidity: {humidity}%\n"
                f"Wind Speed: {wind_speed} km/h"
            )
            self.forecast.set(forecast_msg)

        except requests.RequestException as e:
            self.forecast.set(f"❌ Failed to fetch weather.\n{e}")
        except KeyError:
            self.forecast.set("❌ Unexpected response from API.")


if __name__ == "__main__":
    # Replace with your actual API key
    API_KEY = "your_api_key_here"

    root = tk.Tk()
    app = WeatherApp(root, API_KEY)
    root.mainloop()
