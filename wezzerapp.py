import requests
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

API_KEY = "6d1cb46b004b32d05ba6bd6c91af16de"

def get_current_weather(city_name): # 1 tab
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temperature = data['main']['temp']
        wind_speed = data['wind']['speed']
        humidity = data['main']['humidity']
        weather_info = f"Laikapstākļi {city_name}:\nTemperatūra: {temperature}°C\nVēja ātrums: {wind_speed} m/s\nGaisa mitrums: {humidity}%"
        result_label_current.config(text=weather_info)
        return temperature
    else:
        result_label_current.config(text="Pilsēta netika atrasta.")
        return None

def get_weather_forecast(city_name):  # 2 Tab
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        dates = [datetime.strptime(item['dt_txt'], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H")  for item in data['list'][:10]]
        temperatures = [item['main']['temp'] for item in data['list'][:10]]

        fig, ax = plt.subplots(figsize=(20, 10))
        ax.plot(dates, temperatures, marker='o')
        ax.set_title(f"{city_name} - 3 dienu temperatūras prognoze")
        ax.set_xlabel("Laiks")
        ax.set_ylabel("Temperatūra (°C)")
        plt.xticks(rotation=30)

        for widget in frame_forecast.winfo_children():
            if isinstance(widget, FigureCanvasTkAgg):
                widget.get_tk_widget().destroy()
        canvas = FigureCanvasTkAgg(fig, master=frame_forecast)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)
    else:
        result_label_forecast.config(text="Pilsēta netika atrasta vai prognoze nav pieejama.")
        return None

def compare_cities(city1, city2):
    temp1 = get_current_weather(city1)
    temp2 = get_current_weather(city2)
    if temp1 is not None and temp2 is not None:
        cities = [city1, city2]
        temperatures = [temp1, temp2]

        fig, ax = plt.subplots()
        ax.bar(cities, temperatures, color=['blue', 'orange'])
        ax.set_title("Temperatūras salīdzinājums")
        ax.set_xlabel("Pilsēta")
        ax.set_ylabel("Temperatūra (°C)")

        for widget in frame_compare.winfo_children():
            if isinstance(widget, FigureCanvasTkAgg):
                widget.get_tk_widget().destroy()
        canvas = FigureCanvasTkAgg(fig, master=frame_compare)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)
    else:
        result_label_compare.config(text="Pilsēta netika atrasta vienā vai abās pilsētās.")

def show_current_weather():
    city = entry_city.get()
    if city:
        get_current_weather(city)

def show_weather_forecast():
    city = entry_city_forecast.get()
    if city:
        get_weather_forecast(city)

def show_compare_cities():
    city1 = entry_city1.get()
    city2 = entry_city2.get()
    if city1 and city2:
        compare_cities(city1, city2)


root = tk.Tk()
root.title("Wezzer app")
root.geometry("500x600")
root.configure(bg='lightgreen')

notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)

frame_current = ttk.Frame(notebook, width=500, height=300)
frame_current.pack(fill='both', expand=True)
entry_city = tk.Entry(frame_current, width=30)
entry_city.pack(pady=10)
btn_current_weather = tk.Button(frame_current, text="Pašreizējie laikapstākļi", command=show_current_weather)
btn_current_weather.pack(pady=5)
result_label_current = tk.Label(frame_current, text="", font=("Arial", 12), wraplength=400)
result_label_current.pack(pady=10)

frame_forecast = ttk.Frame(notebook, width=500, height=300)
frame_forecast.pack(fill='both', expand=True)
entry_city_forecast = tk.Entry(frame_forecast, width=30)
entry_city_forecast.pack(pady=10)
btn_weather_forecast = tk.Button(frame_forecast, text="3 dienu prognoze", command=show_weather_forecast)
btn_weather_forecast.pack(pady=5)
result_label_forecast = tk.Label(frame_forecast, text="", font=("Arial", 12), wraplength=400)
result_label_forecast.pack(pady=10)

frame_compare = ttk.Frame(notebook, width=500, height=300)
frame_compare.pack(fill='both', expand=True)
entry_city1 = tk.Entry(frame_compare, width=30)
entry_city1.pack(pady=10)
entry_city2 = tk.Entry(frame_compare, width=30)
entry_city2.pack(pady=10)
btn_compare_cities = tk.Button(frame_compare, text="Salīdzināt divas pilsētas", command=show_compare_cities)
btn_compare_cities.pack(pady=5)
result_label_compare = tk.Label(frame_compare, text="", font=("Arial", 12), wraplength=400)
result_label_compare.pack(pady=10)

notebook.add(frame_current, text="Pašreizējie laikapstākļi")
notebook.add(frame_forecast, text="3 dienu prognoze")
notebook.add(frame_compare, text="Pilsētu salīdzinājums")

exit_button = tk.Button(root, text="Iziet", command=root.destroy)
exit_button.pack(pady=20)

root.mainloop()
