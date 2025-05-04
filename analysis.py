import tkinter as tk
from tkinter import ttk
import os
from datetime import datetime
from collections import defaultdict
import matplotlib.pylab as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
search_entry = None
graph_frame = None
canvas = None 

# Directory containing the image dataset
dataset_dir = "Analysis_data"

# Function to collect dates from image filenames
def collect_dates_from_filenames():
    dates = defaultdict(list)
    for animal_class in os.listdir(dataset_dir):
        class_dir = os.path.join(dataset_dir, animal_class)
        if os.path.isdir(class_dir):
            for filename in os.listdir(class_dir):
                # Split filename into base name and extension
                base_name, extension = os.path.splitext(filename)
                # Split base name to extract date and occurrence count
                parts = base_name.split(" (")
                date_str = parts[0]  # Extract date string
                try:
                    date = datetime.strptime(date_str, "%Y-%m-%d")
                    dates[animal_class].append(date)
                except ValueError:
                    print(f"Ignoring invalid filename format: {filename}")
    return dates

# Sample dataset (replace this with your actual dataset)
captured_dates = collect_dates_from_filenames()

# Function to plot a graph for a given animal type
def plot_graph(animal_type, root):
    global canvas
    dates = captured_dates.get(animal_type, [])
    date_counts = defaultdict(int)
    for date in dates:
        date_counts[date] += 1
    
    sorted_dates = sorted(date_counts.keys())
    counts = [date_counts[date] for date in sorted_dates]

    fig, ax = plt.subplots()
    ax.bar(range(1, len(sorted_dates) + 1), counts)
    ax.set_xlabel('Date')
    ax.set_ylabel('Number of Occurrences')
    ax.set_title(f'Occurrences of {animal_type.capitalize()}')
    ax.set_xticks(range(1, len(sorted_dates) + 1))
    ax.set_xticklabels([date.strftime("%Y-%m-%d") for date in sorted_dates], rotation=45)
    
    if canvas:  # If canvas already exists, clear it
        canvas.get_tk_widget().destroy()

    # Create a FigureCanvasTkAgg object within the analysis window
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side="bottom")

# Function to handle search button click
def search_animal():
    animal = search_entry.get().lower()
    plot_graph(animal, graph_frame)  # Provide the frame argument here


#Funtion to open new window
def open_analysis_window(root):
    # Hide the main GUI window
    root.withdraw()
    
    # Create the analysis window
    analysis_window = tk.Toplevel()
    analysis_window.title("Historical Data Analysis")

    # Maximize the analysis window
    analysis_window.attributes('-fullscreen', True)

    # Create and place widgets
    heading_label = tk.Label(analysis_window, text="Historical Data Analysis", font=('Arial', 20, 'bold'))
    heading_label.pack(pady=10)

    # Search box
    search_label = tk.Label(analysis_window, text="Search Animal Type:")
    search_label.pack(pady=5)
    global search_entry
    search_entry = tk.Entry(analysis_window)
    search_entry.pack(pady=5)

    # Search button
    search_button = ttk.Button(analysis_window, text="Search", command=search_animal)
    search_button.pack(pady=5)

    # Graph frame
    global graph_frame
    graph_frame = tk.Frame(analysis_window)
    graph_frame.pack(pady=10)

    # Function to handle back button click
    def go_back():
        # Destroy the analysis window
        search_entry.destroy()
        graph_frame.destroy()
        analysis_window.destroy()
        # Restore the main GUI window
        root.deiconify()

    back_button = ttk.Button(analysis_window, text="Back", command=go_back)
    back_button.pack(pady=5)

    analysis_window.mainloop()
