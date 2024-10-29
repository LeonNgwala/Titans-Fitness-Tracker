import customtkinter as ctk
from PIL import Image, ImageTk
import subprocess
import sys
import set_goals  # Add this import at the top

# Initialize the custom tkinter application
app = ctk.CTk()
# Set the window size to the full screen size
app.geometry(f"{app.winfo_screenwidth()}x{app.winfo_screenheight()}+0+0")
app.title("Fitness Tracker")

# Assume the email is passed from the previous page as a command-line argument
email = sys.argv[1]  # Retrieve email from the previous screen

# Set up the main frame (which holds both text and image)
main_frame = ctk.CTkFrame(app, corner_radius=0, fg_color="white")
main_frame.pack(fill="both", expand=True)

# Set up the grid for the main frame
main_frame.grid_columnconfigure(0, weight=1, uniform="equal")
main_frame.grid_columnconfigure(1, weight=2, uniform="equal")
main_frame.grid_rowconfigure(0, weight=1)

# Left frame for the text
left_frame = ctk.CTkFrame(main_frame, corner_radius=0, fg_color="white")
left_frame.grid(row=0, column=0, sticky="nsew", pady=100)

# Title Label
title_label = ctk.CTkLabel(left_frame, text="SET GOALS.\nLOG WORKOUTS.\nSTAY ON TRACK.",
                           font=ctk.CTkFont(size=40, weight="bold"))
title_label.pack(pady=(50, 20))

# Description Label
desc_label = ctk.CTkLabel(left_frame, text="Easily track your workouts, set training plans, and \ndiscover new workout routines to crush your goals.",
                          font=ctk.CTkFont(size=14), justify="left")
desc_label.pack(pady=(0, 20))

# Load arrow image for the button (replace with the correct path to your arrow image)
arrow_image = Image.open("img/arrow.png")  # Ensure this is the correct path
arrow_image = arrow_image.resize((20, 20))  # Resize to appropriate size for the button
arrow_image_tk = ImageTk.PhotoImage(arrow_image)

# Button to navigate to the next page (Goals page) with the arrow next to the text
start_button = ctk.CTkButton(left_frame, text="GET STARTED", command=lambda: next_page(email), 
                             font=ctk.CTkFont(size=16, weight="bold"), 
                             width=200, fg_color="black", 
                             image=arrow_image_tk, compound="right")  # Arrow positioned to the right
start_button.pack(pady=(10, 20))

# Right frame for the image and athlete name
right_frame = ctk.CTkFrame(main_frame, corner_radius=0, fg_color="white")
right_frame.grid(row=0, column=1, sticky="nsew", pady=90)

# Load the main image (replace with the correct path)
image = Image.open("img/ketani.jpg")  # Ensure this is the correct path
image = image.resize((800, 400))  # Resize image to fit the design
img = ImageTk.PhotoImage(image)

# Image Label
image_label = ctk.CTkLabel(right_frame, image=img, text="")
image_label.pack(pady=20)

# Athlete Name Label
athlete_label = ctk.CTkLabel(right_frame, text="WEINI KELATI\nPro Middle-Distance Runner", 
                             font=ctk.CTkFont(size=12), justify="right")
athlete_label.pack(pady=(0, 20))

# Function to navigate to the Goals page and pass the email
def next_page(email):
    app.destroy()  # Close the current window first
    set_goals.create_goals_window(email)  # Pass email to the next page's main function

# Run the application
app.mainloop()
