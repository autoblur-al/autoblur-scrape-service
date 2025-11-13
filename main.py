import tkinter as tk
from scraper import scrape_car_data
from car_viewer import show_car_viewer

root = tk.Tk()

def start_report():
    url = url_entry.get()
    if url:
        car_data = scrape_car_data(url)
        show_car_viewer(car_data, parent=root)

root.title("Car Report Generator")
root.geometry("400x150")
root.configure(bg="#f5f6fa")

frame = tk.Frame(root, bg="#f5f6fa")
frame.pack(expand=True)

label = tk.Label(frame, text="Enter Car Detail URL:", font=("Segoe UI", 14), bg="#f5f6fa")
label.pack(pady=10)


# Entry with placeholder
def set_placeholder(entry, placeholder):
    entry.insert(0, placeholder)
    entry.config(fg="#888")
    def on_focus_in(event):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg="#000")
    def on_focus_out(event):
        if not entry.get():
            entry.insert(0, placeholder)
            entry.config(fg="#888")
    entry.bind('<FocusIn>', on_focus_in)
    entry.bind('<FocusOut>', on_focus_out)

url_entry = tk.Entry(frame, font=("Segoe UI", 12), width=40)
url_entry.pack(pady=5)
set_placeholder(url_entry, "Paste car detail URL here")

btn = tk.Button(frame, text="Generate Report", font=("Segoe UI", 12), bg="#dfe4ea", relief="flat", command=start_report)
btn.pack(pady=10)

root.mainloop()
