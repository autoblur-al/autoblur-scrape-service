import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO

def show_car_viewer(car_data, parent=None):
    image_urls = car_data.get("Images", [])
    # Use Toplevel if parent is provided, else Tk for standalone
    if parent:
        viewer = tk.Toplevel(parent)
    else:
        viewer = tk.Tk()
    viewer.title("Car Report")
    viewer.configure(bg="#f5f6fa")

    # Main frame for layout
    main_frame = tk.Frame(viewer, bg="#f5f6fa")
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Info frame
    info_frame = tk.Frame(main_frame, bg="#f5f6fa")
    info_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 20))

    # Show car data with modern formatting
    row = 0
    info_font = ("Segoe UI", 14)
    label_font = ("Segoe UI", 16, "bold")
    for key in ["Car Name", "Type", "Generation", "Year", "Mileage", "Fuel Type", "Vehicle Number", "Price"]:
        value = car_data.get(key, "")
        tk.Label(info_frame, text=f"{key}: ", font=label_font, bg="#f5f6fa", anchor="w").grid(row=row, column=0, sticky="w", pady=4)
        tk.Label(info_frame, text=value, font=info_font, bg="#f5f6fa", anchor="w").grid(row=row, column=1, sticky="w", pady=4)
        row += 1

    # Image frame
    img_frame = tk.Frame(main_frame, bg="#f5f6fa")
    img_frame.grid(row=0, column=1, sticky="nsew")

    # Image navigation logic
    img_label = tk.Label(img_frame, bg="#f5f6fa")
    img_label.pack(pady=10)
    img_index = [0]
    img_cache = {}

    def show_image(idx):
        if image_urls:
            try:
                if idx in img_cache:
                    photo = img_cache[idx]
                else:
                    response = requests.get(image_urls[idx])
                    img_data = BytesIO(response.content)
                    img = Image.open(img_data)
                    img = img.resize((500, 375))
                    photo = ImageTk.PhotoImage(img)
                    img_cache[idx] = photo
                img_label.config(image=photo)
                img_label.image = photo
                img_label.config(text="")
            except Exception as e:
                img_label.config(text=f"Image load error: {e}", image="")
        else:
            img_label.config(text="No images available", image="")

    def next_image():
        if image_urls:
            img_index[0] = (img_index[0] + 1) % len(image_urls)
            show_image(img_index[0])

    def prev_image():
        if image_urls:
            img_index[0] = (img_index[0] - 1) % len(image_urls)
            show_image(img_index[0])

    # Navigation buttons frame
    nav_frame = tk.Frame(img_frame, bg="#f5f6fa")
    nav_frame.pack(pady=5)
    btn_prev = tk.Button(nav_frame, text="⟨ Previous", command=prev_image, font=("Segoe UI", 12), bg="#dfe4ea", relief="flat", padx=10, pady=5)
    btn_prev.pack(side="left", padx=10)
    btn_next = tk.Button(nav_frame, text="Next ⟩", command=next_image, font=("Segoe UI", 12), bg="#dfe4ea", relief="flat", padx=10, pady=5)
    btn_next.pack(side="left", padx=10)

    show_image(img_index[0])
    viewer.mainloop() if not parent else None
