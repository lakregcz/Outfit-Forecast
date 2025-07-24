import flet as ft
import requests
import json
import random
from datetime import datetime
from typing import Optional, List, Dict

CONFIG_FILE = "weather_outfit_config.json"
API_BASE_URL = "https://api.open-meteo.com/v1/forecast"
GEOCODING_API_URL = "https://geocoding-api.open-meteo.com/v1/search"

WEATHER_ICONS = {
    "clear": "☀️",
    "cloudy": "☁️",
    "rain": "🌧️",
    "snow": "❄️",
    "thunderstorm": "⛈️",
    "fog": "🌫️",
    "drizzle": "🌦️",
    "default": "🌈"
}

MOTIVATIONAL_QUOTES = [
    "The only way to do great work is to love what you do. - Steve Jobs",
    "Believe you can and you're halfway there. - Theodore Roosevelt",
    "Success is not final, failure is not fatal: It is the courage to continue that counts. - Winston Churchill",
    "Your time is limited, don't waste it living someone else's life. - Steve Jobs",
    "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
    "Strive not to be a success, but rather to be of value. - Albert Einstein",
    "Life is what happens when you're busy making other plans. - John Lennon",
    "The best way to predict the future is to invent it. - Alan Kay",
    "Don't watch the clock; do what it does. Keep going. - Sam Levenson",
    "The only limit to our realization of tomorrow is our doubts of today. - Franklin D. Roosevelt"
]

class WeatherApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Outfit Forecast"
        self.page.window_width = 900
        self.page.window_height = 750
        self.page.window_resizable = False
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.padding = 40
        self.page.fonts = {"Poppins": "fonts/Poppins-Regular.ttf"}
        self.page.theme = ft.Theme(font_family="Poppins")

        self.user_name: Optional[str] = None
        self.current_location: Optional[Dict] = None
        self.saved_locations: List[Dict] = []
        self.weather_data: Optional[Dict] = None

        self.load_config()
        self.setup_ui()

        # Set random quote
        self.set_random_quote()

        if self.saved_locations:
            self.show_location(self.saved_locations[-1])

    def setup_ui(self):
        self.greeting_text = ft.Text(size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800)
        self.current_time_text = ft.Text(size=16, color=ft.Colors.GREY_500)

        self.header = ft.Text("Outfit Forecast", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800)

        self.search_field = ft.TextField(
            label="Search for a city...",
            prefix_icon=ft.Icons.SEARCH,
            on_change=self.handle_search,
            autofocus=True,
            border_radius=15,
            border_color=ft.Colors.BLUE_200
        )
        self.search_results = ft.ListView(spacing=5, height=150, visible=False)

        self.weather_icon = ft.Text(size=100, text_align=ft.TextAlign.CENTER)
        self.weather_temp = ft.Text(size=48, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
        self.weather_desc = ft.Text(size=18, text_align=ft.TextAlign.CENTER)

        self.outfit_title = ft.Text("Outfit Recommendation", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800)
        self.outfit_content = ft.Column(spacing=5, scroll=ft.ScrollMode.AUTO)

        self.quote_title = ft.Text("Quote of the Day", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800)
        self.quote_content = ft.Text(size=16, italic=True, text_align=ft.TextAlign.CENTER)

        self.contact_info = ft.Text("Contact: contact@lakiup.com", size=14, color=ft.Colors.GREY_600)

        self.page.add(
            ft.Column([
                self.header,
                self.greeting_text,
                self.current_time_text,
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                self.search_field,
                self.search_results,
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                ft.Row([
                    ft.Column([
                        self.weather_icon,
                        self.weather_temp,
                        self.weather_desc
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, width=200),
                    ft.VerticalDivider(width=20, color=ft.Colors.BLUE_100),
                    ft.Column([self.outfit_title, self.outfit_content], expand=True)
                ], spacing=20),
                ft.Divider(height=30, color=ft.Colors.BLUE_100),
                self.quote_title,
                self.quote_content,
                ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                ft.Row([self.contact_info], alignment=ft.MainAxisAlignment.END)
            ], spacing=10, expand=True)
        )

        self.update_time()
        if not self.user_name:
            self.ask_user_name()

    def update_time(self):
        now = datetime.now()
        self.current_time_text.value = f"Current time: {now.strftime('%H:%M:%S')}"
        greeting = self.get_greeting()
        if self.user_name:
            self.greeting_text.value = f"{greeting}, {self.user_name}!"
        self.page.update()

    def get_greeting(self):
        hour = datetime.now().hour
        if hour < 12:
            return "Good morning"
        elif hour < 18:
            return "Good afternoon"
        else:
            return "Good evening"

    def ask_user_name(self):
        def save_name(e):
            name = name_input.value.strip()
            if name:
                self.user_name = name
                self.save_config()
                dialog.open = False
                self.page.dialog = None
                self.update_time()

        name_input = ft.TextField(label="Enter your name", autofocus=True)
        dialog = ft.AlertDialog(
            title=ft.Text("Welcome!"),
            content=name_input,
            actions=[ft.TextButton("Continue", on_click=save_name)],
            open=True
        )
        self.page.dialog = dialog
        self.page.update()

    def handle_search(self, e):
        query = self.search_field.value.strip()
        if len(query) < 3:
            self.search_results.visible = False
            self.search_results.controls.clear()
            self.page.update()
            return

        try:
            response = requests.get(GEOCODING_API_URL, params={"name": query, "count": 5, "language": "en", "format": "json"})
            response.raise_for_status()
            data = response.json()
            self.search_results.controls.clear()

            if "results" in data:
                for location in data["results"]:
                    display_name = f"{location.get('name', '')}, {location.get('admin1', '')}, {location.get('country', '')}"
                    self.search_results.controls.append(
                        ft.ListTile(
                            title=ft.Text(display_name),
                            on_click=lambda e, loc=location: self.select_location(loc),
                            dense=True
                        )
                    )
            else:
                self.search_results.controls.append(ft.ListTile(title=ft.Text("No locations found"), disabled=True))

            self.search_results.visible = True
            self.page.update()
        except requests.exceptions.RequestException:
            self.search_results.controls.clear()
            self.search_results.controls.append(ft.ListTile(title=ft.Text("Error fetching locations"), disabled=True))
            self.search_results.visible = True
            self.page.update()

    def select_location(self, location: Dict):
        self.current_location = {
            "name": f"{location.get('name', '')}, {location.get('admin1', '')}",
            "latitude": location.get("latitude"),
            "longitude": location.get("longitude")
        }
        self.search_field.value = self.current_location["name"]
        self.search_results.visible = False
        self.save_location(self.current_location)
        self.show_location(self.current_location)
        self.page.update()

    def show_location(self, location: Dict):
        self.current_location = location
        self.weather_icon.value = "⏳"
        self.weather_temp.value = ""
        self.weather_desc.value = "Loading weather data..."
        self.outfit_content.controls.clear()
        self.outfit_content.controls.append(ft.ProgressRing())
        self.page.update()

        weather_data = self.get_weather_data(location["latitude"], location["longitude"])
        if weather_data:
            self.weather_data = weather_data
            self.display_weather(weather_data)
            self.display_outfit_recommendation(weather_data)
        else:
            self.weather_icon.value = "❌"
            self.weather_desc.value = "Failed to load weather data"
            self.outfit_content.controls.clear()
            self.outfit_content.controls.append(ft.Text("Could not get weather information. Please try again."))

        self.page.update()

    def get_weather_data(self, latitude: float, longitude: float) -> Optional[Dict]:
        try:
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "current_weather": True,
                "hourly": "temperature_2m,weathercode",
                "timezone": "auto"
            }
            response = requests.get(API_BASE_URL, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            return None

    def display_weather(self, weather_data: Dict):
        current = weather_data.get("current_weather", {})
        temp = current.get("temperature", "N/A")
        code = current.get("weathercode", 0)

        self.weather_temp.value = f"{temp}°C"
        if code == 0:
            self.weather_icon.value = "☀️"; self.weather_desc.value = "Clear sky"
        elif 1 <= code <= 3:
            self.weather_icon.value = "🌤️"; self.weather_desc.value = "Partly cloudy"
        elif code in [45, 48]:
            self.weather_icon.value = "🌫️"; self.weather_desc.value = "Foggy"
        elif 51 <= code <= 67:
            self.weather_icon.value = "🌧️"; self.weather_desc.value = "Rainy"
        elif 71 <= code <= 77:
            self.weather_icon.value = "❄️"; self.weather_desc.value = "Snowy"
        elif 80 <= code <= 86:
            self.weather_icon.value = "🌦️"; self.weather_desc.value = "Rain showers"
        elif 95 <= code <= 99:
            self.weather_icon.value = "⛈️"; self.weather_desc.value = "Thunderstorm"
        else:
            self.weather_icon.value = WEATHER_ICONS["default"]; self.weather_desc.value = "Unknown weather"

    def display_outfit_recommendation(self, weather_data: Dict):
        temp = weather_data.get("current_weather", {}).get("temperature", None)
        self.outfit_content.controls.clear()

        if temp is None:
            self.outfit_content.controls.append(ft.Text("Temperature data not available"))
            return

        if temp > 25:
            items = ["🌞 Lightweight, breathable clothing", "🩳 Shorts or a skirt", "👕 T-shirt", "😎 Sunglasses", "👡 Sandals", "💧 Sunscreen"]
        elif 18 <= temp <= 25:
            items = ["🌤️ Light layers", "👚 T-shirt", "👖 Jeans", "👟 Sneakers", "🧴 Light jacket"]
        elif 10 <= temp < 18:
            items = ["🍂 Sweater", "👖 Jeans", "🧥 Light jacket", "👞 Closed shoes", "🧣 Light scarf"]
        elif 0 <= temp < 10:
            items = ["❄️ Warm sweater", "🧥 Coat", "🧤 Gloves", "🧦 Warm socks", "🥾 Boots"]
        else:
            items = ["🥶 Thermals", "🧥 Heavy coat", "🧣 Hat & scarf", "🧦 Insulated socks", "🥾 Winter boots", "🔥 Hand warmers"]

        for i in items:
            self.outfit_content.controls.append(ft.Text(i, size=16))

    def set_random_quote(self):
        self.quote_content.value = random.choice(MOTIVATIONAL_QUOTES)

    def save_location(self, location: Dict):
        for loc in self.saved_locations:
            if loc["latitude"] == location["latitude"] and loc["longitude"] == location["longitude"]:
                return
        self.saved_locations.append(location)
        self.save_config()

    def load_config(self):
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                self.saved_locations = data.get("locations", [])
                self.user_name = data.get("user_name", None)
        except (IOError, json.JSONDecodeError):
            self.saved_locations = []

    def save_config(self):
        try:
            with open(CONFIG_FILE, "w") as f:
                json.dump({
                    "locations": self.saved_locations,
                    "user_name": self.user_name
                }, f)
        except IOError:
            pass


def main(page: ft.Page):
    WeatherApp(page)

if __name__ == "__main__":
    ft.app(target=main)
