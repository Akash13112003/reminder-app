import tkinter as tk
from tkinter import ttk
import time
import winsound
import datetime
from threading import Thread

# Define the list of activities
activities = [
    "Wake up",
    "Go to gym",
    "Breakfast",
    "Meetings",
    "Lunch",
    "Quick nap",
    "Go to library",
    "Dinner",
    "Go to sleep"
]

# Create a list to store reminders
reminders = []

# Create a variable to track the current alert thread
current_alert_thread = None

# Function to update the countdown timers
def update_timers():
    while True:
        current_time = time.strftime("%H:%M")
        for reminder in reminders:
            remaining_time = get_time_difference(current_time, reminder['time'])
            reminder['remaining_time'] = remaining_time
            if remaining_time == "00:00" and reminder['status'] == 'Active':
                reminder['status'] = "Alerted"
                play_alert_sound()
        update_reminders_list()
        time.sleep(1)

# Function to calculate the time difference
def get_time_difference(current_time, reminder_time):
    current_datetime = datetime.datetime.now().replace(hour=int(current_time[:2]), minute=int(current_time[3:5]))
    reminder_datetime = datetime.datetime.now().replace(hour=int(reminder_time[:2]), minute=int(reminder_time[3:5]))

    if current_datetime < reminder_datetime:
        time_diff = reminder_datetime - current_datetime
        minutes, seconds = divmod(time_diff.seconds, 60)
        return f"{int(minutes):02d}:{int(seconds):02d}"
    else:
        return "00:00"

# Function to play the alert sound
def play_alert_sound():
    winsound.Beep(1000, 1000)  # Play a beep sound

# Function to stop the alert sound and clear reminders
def stop_alert():
    global current_alert_thread
    if current_alert_thread:
        current_alert_thread.terminate()
    for reminder in reminders:
        if reminder['status'] == 'Alerted':
            reminder['status'] = 'Cleared'
    update_reminders_list()

# Function to set a reminder
def set_reminder():
    selected_day = day_var.get()
    selected_time = time_var.get()
    selected_activity = activity_var.get()

    reminders.append({
        'day': selected_day,
        'time': selected_time,
        'activity': selected_activity,
        'status': 'Active',
        'remaining_time': get_time_difference(time.strftime("%H:%M"), selected_time)
    })

    update_reminders_list()

# Function to update the reminders list
def update_reminders_list():
    reminders_listbox.delete(0, tk.END)
    for reminder in reminders:
        reminders_listbox.insert(tk.END, f"{reminder['activity']} ({reminder['remaining_time']} remaining) - {reminder['status']}")

# Create the main application window
root = tk.Tk()
root.title("Daily Reminder App")
root.geometry("600x400")  # Set the initial window size

# Create and place GUI components
style = ttk.Style()
style.theme_use("clam")  # Use the "clam" theme for a modern look

header_label = tk.Label(root, text="Daily Reminder App", font=("Helvetica", 16, "bold"))
header_label.pack(pady=10)

day_label = tk.Label(root, text="Select Day:")
day_label.pack()

day_var = tk.StringVar()
day_dropdown = ttk.Combobox(root, textvariable=day_var, values=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
day_dropdown.pack()

time_label = tk.Label(root, text="Select Time:")
time_label.pack()

time_var = tk.StringVar()
time_dropdown = ttk.Combobox(root, textvariable=time_var, values=["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00"])
time_dropdown.pack()

activity_label = tk.Label(root, text="Select Activity:")
activity_label.pack()

activity_var = tk.StringVar()
activity_dropdown = ttk.Combobox(root, textvariable=activity_var, values=activities)
activity_dropdown.pack()

set_reminder_button = tk.Button(root, text="Set Reminder", command=set_reminder, bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"))
set_reminder_button.pack(pady=10)

reminders_listbox = tk.Listbox(root, font=("Helvetica", 12), selectmode=tk.SINGLE)
reminders_listbox.pack(pady=10)

# Create and place the Stop button

# Start the timer update thread
timer_thread = Thread(target=update_timers)
timer_thread.daemon = True
timer_thread.start()

# Start the GUI event loop
root.mainloop()
