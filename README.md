# Outfit Forecast

[![Preview](https://lakiup.com/wp-content/uploads/2025/07/OutfitForecast.png)](https://lakiup.com)

Outfit Forecast is a desktop weather app built with [Flet](https://flet.dev/) that provides real-time weather information and personalized outfit recommendations based on the current temperature of any searched city. It also displays motivational quotes to brighten your day!

---

## Features

* **Search cities worldwide** with auto-suggestions powered by Open-Meteo's Geocoding API.
* **Current weather display** including temperature and weather conditions with intuitive icons.
* **Outfit recommendations** tailored to the temperature.
* **Motivational quote of the day** for inspiration.
* **Save favorite locations** locally for quick access.
* Friendly UI with dark mode and a modern font (Poppins).
* Configurations are saved locally in `weather_outfit_config.json`.
* Responsive UI components with loading indicators and error handling.

---

## Screenshots

![App Preview](https://lakiup.com/wp-content/uploads/2025/07/OutfitForecast.png)

---

## Installation & Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/lakregcz/Outfit-Forecast.git
   cd Outfit-Forecast
   ```

2. **Install dependencies:**

   Make sure you have Python 3.7+ installed.

   ```bash
   pip install flet requests
   ```

3. **Run the app:**

   ```bash
   python "Outfit Forecast.py"
   ```

---

## Usage

* On first launch, enter your name to personalize greetings.
* Use the search bar to find your city.
* Select a location from the search results to fetch weather and outfit recommendations.
* The app saves your last selected locations for convenience.

---

## APIs Used

* **Open-Meteo Weather API** for current weather and hourly data
  [https://open-meteo.com/](https://open-meteo.com/)

* **Open-Meteo Geocoding API** for city search and location lookup
  [https://geocoding-api.open-meteo.com/](https://geocoding-api.open-meteo.com/)

---

## Configuration

* The app saves user name and saved locations in `weather_outfit_config.json` in the working directory.
* Fonts folder should contain `Poppins-Regular.ttf` for the app font (included or download separately).

---

## About

Developed by **lakregcz**
Website: [lakiup.com](https://lakiup.com)
Contact: [contact@lakiup.com](mailto:contact@lakiup.com)

---

## License

This project is open source under the [MIT License](LICENSE).

---

## Contribution

Feel free to open issues or submit pull requests to improve the app!


