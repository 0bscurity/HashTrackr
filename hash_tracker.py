import hashlib
import requests
import time
import threading
from tkinter import *
from tkinter import ttk

url = ""
check_period = 1  # in seconds
stop_checking = False


def fetch_and_hash(url):
    response = requests.get(url)
    content = response.content
    content_hash = hashlib.sha256(content).hexdigest()
    return content_hash


def check_website_changes(url, output_text):
    global stop_checking
    initial_hash = fetch_and_hash(url)
    change_count = 0

    while not stop_checking:
        change_count += 1
        time.sleep(check_period)
        new_hash = fetch_and_hash(url)

        if initial_hash != new_hash:
            output_text.set(f"The website content has changed >= {change_count} time(s).")
            initial_hash = new_hash
        else:
            output_text.set("No change detected.")


def start_checking():
    global stop_checking
    url = url_entry.get()
    if not url:
        output_text.set("Please enter a URL.")
        return

    stop_checking = False
    output_text.set("Checking for changes...")
    check_thread = threading.Thread(target=check_website_changes, args=(url, output_text))
    check_thread.daemon = True
    check_thread.start()


def stop_checking_process():
    global stop_checking
    stop_checking = True
    output_text.set("Stopped checking.")


root = Tk()
root.title("HashTrackr")
root.configure(bg="#1c1c1c")

frame = Frame(root, bg="#1c1c1c")
frame.pack(padx=10, pady=10)

futuristic_font = ("Helvetica", 12, "bold")
url_label = Label(frame, text="Enter URL:", font=futuristic_font, bg="#1c1c1c", fg="#00ff00")
url_label.grid(row=0, column=0, sticky=W)

url_entry = Entry(frame, width=50, font=("Helvetica", 12))
url_entry.grid(row=0, column=1, padx=10, pady=5)

style = ttk.Style()
style.configure("TButton", font=futuristic_font, borderwidth=0)

start_button = ttk.Button(frame, text="Start Checking", command=start_checking)
start_button.grid(row=1, column=1, sticky=W, pady=5)

stop_button = ttk.Button(frame, text="Stop Checking", command=stop_checking_process)
stop_button.grid(row=1, column=1, sticky=E, pady=5)

output_text = StringVar()
output_label = Label(frame, textvariable=output_text, font=futuristic_font, bg="#1c1c1c", fg="#00ff00")
output_label.grid(row=2, column=0, columnspan=2, sticky=W, pady=5)

root.mainloop()
