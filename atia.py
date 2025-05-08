import requests
from datetime import datetime
import os
from dotenv import load_dotenv
import logging
import time
import random
import tkinter as tk
from tkinter import messagebox, ttk
from threading import Thread  # For asynchronous data fetching

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(filename="weather_report.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Retry configuration
MAX_RETRIES = 3
RETRY_DELAY = 3  # Seconds

def get_random_city_suggestion():
    cities = ["New York", "London", "Tokyo", "Sydney", "Paris", "Berlin"]
    return random.choice(cities)

def get_weather(city_name, result_text, city_entry):
    retries = 0
    while retries < MAX_RETRIES:
        try:
            # Retrieve API key from environment variables
            API_Key = os.getenv('API_KEY')
            if not API_Key:
                raise EnvironmentError("API Key not found in environment variables.")
            
            # Construct the API request URL
            url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_Key}&units=metric'

            # Send the GET request
            response = requests.get(url)
            response.raise_for_status()  # Raises an error for 4xx or 5xx codes

            # Parse the JSON response into a Python dictionary
            data = response.json()

            # Log the successful API fetch
            logging.info(f"Successfully fetched weather data for {city_name.title()}.")

            # Check if the response contains the necessary data
            if 'weather' not in data or 'main' not in data or 'sys' not in data:
                raise ValueError(f"Invalid data received for city '{city_name}'. Missing key information.")

            # Extract weather details and format for display
            weather_report = f"\nWeather Report for {city_name.title()}:\n"
            weather_report += f"Weather: {data['weather'][0]['description'].title()}\n"
            weather_report += f"Temperature: {data['main']['temp']}°C\n"
            weather_report += f"Feels Like: {data['main']['feels_like']}°C\n"
            weather_report += f"Humidity: {data['main']['humidity']}%\n"
            weather_report += f"Wind Speed: {data['wind']['speed']} m/s\n"
            weather_report += f"Pressure: {data['main']['pressure']} hPa\n"
            weather_report += f"UV Index: {random.randint(1, 10)} (Simulated)\n"

            # Sunrise and sunset in human-readable format
            sunrise = datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M:%S')
            sunset = datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M:%S')
            weather_report += f"Sunrise: {sunrise}\n"
            weather_report += f"Sunset: {sunset}\n"

            # Display the weather data in the result_text widget
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, weather_report)

            # Log the weather report to a log file
            logging.info(f"Weather report generated for {city_name.title()}.\n")

            return
        except requests.exceptions.RequestException as e:
            logging.error(f"Error making request to OpenWeather API for {city_name}: {e}")
            retries += 1
            if retries < MAX_RETRIES:
                result_text.insert(tk.END, f"Retrying... ({retries}/{MAX_RETRIES})\n")
                time.sleep(RETRY_DELAY)
            else:
                result_text.insert(tk.END, "Max retries reached. Unable to fetch data.\n")
                logging.error(f"Max retries reached for {city_name}. Failed to fetch data.")
                return
        except ValueError as e:
            result_text.insert(tk.END, f"Error with the data received: {e}\n")
            logging.error(f"Data issue for {city_name}: {e}")
            return
        except EnvironmentError as e:
            result_text.insert(tk.END, f"Environment error: {e}\n")
            logging.error(f"Environment error for {city_name}: {e}")
            return
        except Exception as e:
            result_text.insert(tk.END, f"Unexpected error: {e}\n")
            logging.error(f"Unexpected error for {city_name}: {e}")
            return

def on_get_weather(city_entry, result_text):
    city_name = city_entry.get().strip()
    if not city_name:
        messagebox.showwarning("Input Error", "Please enter a city name.")
    else:
        # Start a new thread to fetch weather data asynchronously
        weather_thread = Thread(target=get_weather, args=(city_name, result_text, city_entry))
        weather_thread.start()

def on_suggest_city(city_entry):
    suggested_city = get_random_city_suggestion()
    city_entry.delete(0, tk.END)
    city_entry.insert(tk.END, suggested_city)

# Tkinter GUI setup
def create_gui():
    root = tk.Tk()
    root.title("Weather Report System")
    root.geometry("500x600")

    # City input section
    city_label = tk.Label(root, text="Enter city name:", font=("Arial", 12))
    city_label.pack(pady=10)

    city_entry = tk.Entry(root, width=30, font=("Arial", 12))
    city_entry.pack(pady=5)

    # Buttons to fetch weather and suggest city
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    get_weather_button = tk.Button(button_frame, text="Get Weather", width=20, command=lambda: on_get_weather(city_entry, result_text))
    get_weather_button.pack(side=tk.LEFT, padx=10)

    suggest_button = tk.Button(button_frame, text="Suggest City", width=20, command=lambda: on_suggest_city(city_entry))
    suggest_button.pack(side=tk.LEFT, padx=10)

    # Textbox for displaying weather data
    result_text = tk.Text(root, height=15, width=60, font=("Arial", 10), wrap=tk.WORD)
    result_text.pack(pady=10)

    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    create_gui()
