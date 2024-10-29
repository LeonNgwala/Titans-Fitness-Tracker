import customtkinter as ctk
from PIL import Image, ImageTk  # Ensure ImageTk is imported
import os
import datetime
import tkinter.messagebox as messagebox
from tkcalendar import Calendar
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys
import random
import json

# Import the exercises data
# from exercises import exercises

# Initialize customtkinter
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Global variables
root = None
main_content_frame = None
recent_workouts_textbox = None
progress_label = None
profile_label = None
nav_buttons = []
notification_var = None

# Function to read user data from the text file
def load_user_data(email):
    user_data = {
        "workouts": [],
        "measurements": {}
    }
    
    # Load workout data
    try:
        with open("FitnessTrackerData.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                data = line.strip().split(',')
                if data[0] == email:
                    user_data["workouts"].append(','.join(data[1:]))
    except FileNotFoundError:
        print("No workout data found")

    # Load measurements data
    try:
        with open("measurements.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                data = line.strip().split(',')
                if data[0] == email:
                    user_data["measurements"] = {
                        "height": data[1],
                        "weight": data[2],
                        "age": data[3],
                        "gender": data[4],
                        "goal": data[5] if len(data) > 5 else "Not specified"
                    }
                    break
    except FileNotFoundError:
        print("No measurements data found")

    return user_data

# Function to load and display recent workouts
def load_recent_workouts(email):
    user_data = load_user_data(email)
    workouts = user_data.get("workouts", [])
    recent_workouts_textbox.delete("1.0", ctk.END)  # Clear textbox before loading new data
    if workouts:
        for workout in workouts:
            recent_workouts_textbox.insert(ctk.END, f"{workout}\n")
    else:
        recent_workouts_textbox.insert(ctk.END, "No recent workouts recorded.")

# Function to create the dashboard
def create_dashboard(email, user_name):
    global root, main_content_frame, recent_workouts_textbox, progress_label, profile_label
    root = ctk.CTk()
    root.title("Titan Fitness Tracker/Dashboard")

    # Set the window to open in full screen immediately
    # root.attributes('-fullscreen', True)
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")

    # Set custom logo in the title bar
    try:
        new_logo_image = Image.open("icons/new_logo.png")
        new_logo_image = new_logo_image.resize((32, 32), Image.ANTIALIAS)
        new_logo_photo = ImageTk.PhotoImage(new_logo_image)
        root.iconphoto(False, new_logo_photo)
    except Exception as e:
        print(f"Error loading logo: {e}")

    # Load the icon for the welcome label
    try:
        welcome_icon = ctk.CTkImage(light_image=Image.open("icons/welcome_icon.png"), size=(20, 20))
    except Exception:
        welcome_icon = None

    welcome_label = ctk.CTkLabel(
        root, 
        text=f"Welcome, {user_name}!", 
        font=("Helvetica", 16), 
        image=welcome_icon,
        compound="left"
    )
    welcome_label.pack(pady=20)

    # Frame for side navigation
    side_nav_frame = ctk.CTkFrame(root, width=200, corner_radius=0)
    side_nav_frame.pack(side="left", fill="y")

    # Header Frame (User Profile)
    profile_frame = ctk.CTkFrame(side_nav_frame, height=150, corner_radius=0)
    profile_frame.pack(fill="x")

    try:
        profile_picture_icon = ctk.CTkImage(light_image=Image.open("icons/logo2.png"), size=(80, 80))
    except Exception:
        profile_picture_icon = None

    profile_picture = ctk.CTkLabel(profile_frame, image=profile_picture_icon, text="", width=80, height=80)
    profile_picture.pack(pady=10)

    profile_label = ctk.CTkLabel(profile_frame, text=email, font=ctk.CTkFont(size=16, weight="bold"))
    profile_label.pack(pady=5)

    global nav_buttons
    nav_buttons = []

    def create_button(text, command, icon=None):
        button = ctk.CTkButton(
            side_nav_frame, text=text, font=ctk.CTkFont(size=14),
            command=lambda: [command(), set_active(button)],  # Ensure command is wrapped in a lambda
            image=icon, compound="left", corner_radius=10
        )
        button.pack(pady=10, padx=10, fill="x", expand=True)
        button.bind("<Enter>", lambda event: on_hover(button, True))
        button.bind("<Leave>", lambda event: on_hover(button, False))
        nav_buttons.append(button)
        return button

    # Load icons
    try:
        logout_icon = ctk.CTkImage(light_image=Image.open("icons/logout.png"), size=(20, 20))
        workout_icon = ctk.CTkImage(light_image=Image.open("icons/workout.png"), size=(20, 20))
        progress_icon = ctk.CTkImage(light_image=Image.open("icons/progress.png"), size=(20, 20))
        history_icon = ctk.CTkImage(light_image=Image.open("icons/history.png"), size=(20, 20))
        lessons_icon = ctk.CTkImage(light_image=Image.open("icons/workout.png"), size=(20, 20))
        settings_icon = ctk.CTkImage(light_image=Image.open("icons/settings.png"), size=(20, 20))
    except Exception:
        logout_icon = workout_icon = progress_icon = history_icon = lessons_icon = settings_icon = None

    # Create buttons in the desired order
    create_button("Log Workout", lambda: log_workout(email), icon=workout_icon)
    create_button("Progress", lambda: show_progress_line_graph(email), icon=progress_icon)
    create_button("Recent Workouts", lambda: show_recent_workouts(email), icon=history_icon)
    create_button("Workout Lessons", show_lessons, icon=lessons_icon)
    create_button("Settings", show_settings, icon=settings_icon)

    # Pack the logout button at the bottom
    logout_button = ctk.CTkButton(
        side_nav_frame, text="Logout", font=ctk.CTkFont(size=14),
        command=logout, image=logout_icon, compound="left", corner_radius=10
    )
    logout_button.pack(pady=10, padx=10, fill="x", expand=True, side="bottom")

    main_content_frame = ctk.CTkFrame(root)
    main_content_frame.pack(side="right", fill="both", expand=True)

    # --- Progress Section --- 
    progress_frame = ctk.CTkFrame(main_content_frame, corner_radius=10)
    progress_frame.pack(pady=20, padx=20, fill="both", expand=True)

    progress_label = ctk.CTkLabel(progress_frame, text="Workout Progress", font=ctk.CTkFont(size=20, weight="bold"))
    progress_label.pack(pady=20)

    recent_workouts_textbox = ctk.CTkTextbox(progress_frame, height=300, width=500, state="normal", corner_radius=5)
    recent_workouts_textbox.pack(pady=10)

    load_recent_workouts(email)
    show_progress_line_graph(email)

    root.mainloop()

def show_recent_workouts(email):
    # Clear the current content
    for widget in main_content_frame.winfo_children():
        widget.destroy()

    recent_workouts_frame = ctk.CTkFrame(main_content_frame, fg_color="white", corner_radius=10)
    recent_workouts_frame.pack(pady=20, padx=20, fill="both", expand=True)

    ctk.CTkLabel(recent_workouts_frame, text="All Workouts", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)

    # Create a frame to display all workouts in a visually appealing format
    workouts_display_frame = ctk.CTkFrame(recent_workouts_frame, fg_color="lightgrey", corner_radius=5)
    workouts_display_frame.pack(pady=10, padx=10, fill="both", expand=True)

    # Load user data
    user_data = load_user_data(email)
    workouts = user_data.get("workouts", [])

    # Debugging output
    print(f"Loaded workouts for {email}: {workouts}")

    # Function to generate a color for each unique date
    def get_color_for_date(date):
        # Simple hash function to generate a color from a date string
        return f"#{hash(date) & 0xFFFFFF:06x}"

    if workouts:
        for workout in workouts:
            workout_details = workout.split(',')
            if len(workout_details) < 3:
                continue  # Skip malformed entries

            exercise, date, duration = workout_details[:3]
            workout_text = f"Exercise: {exercise}, Date: {date}, Duration: {duration} mins"
            color = get_color_for_date(date)  # Get a color for the date

            workout_label = ctk.CTkLabel(
                workouts_display_frame, 
                text=workout_text, 
                font=ctk.CTkFont(size=14),
                text_color=color  # Set the text color
            )
            workout_label.pack(pady=5, padx=5, anchor='w')
    else:
        ctk.CTkLabel(workouts_display_frame, text="No workouts recorded.", font=ctk.CTkFont(size=14)).pack(pady=10)

def logout():
    # Ask for confirmation before logging out
    if messagebox.askyesno("Confirm Logout", "Are you sure you want to log out?"):
        root.destroy()  # Close the current dashboard window
        import Login  # Import and run the Login module directly
        Login.main()  # Assuming Login.py has a main() function

def log_workout(email):
    # Clear the current content
    for widget in main_content_frame.winfo_children():
        widget.destroy()

    # Create a frame for logging workouts
    log_workout_frame = ctk.CTkFrame(main_content_frame, fg_color="white", corner_radius=10)
    log_workout_frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Exercise type dropdown
    exercise_label = ctk.CTkLabel(log_workout_frame, text="Select Exercise Type:")
    exercise_label.pack(pady=5)
    exercise_var = tk.StringVar(value="Plank")  # Changed default value
    exercise_dropdown = ctk.CTkOptionMenu(
        log_workout_frame, 
        variable=exercise_var, 
        values=[
            "Plank", "Squat", "Lunge", "Wall sit", "Arm circles", "Push-up",
            "Step up", "Shoulder bridge", "Tuck jump", "Mountain climber",
            "Stair climb with bicep curl", "Deadlifts", "Leg press", "Pull up", "Bench press"
        ]
    )
    exercise_dropdown.pack(pady=5)

    # Calendar for selecting date
    date_label = ctk.CTkLabel(log_workout_frame, text="Select Workout Date:")
    date_label.pack(pady=5)
    calendar = Calendar(log_workout_frame, selectmode='day')
    calendar.pack(pady=5)

    # Duration input
    duration_label = ctk.CTkLabel(log_workout_frame, text="Enter Duration (minutes):")
    duration_label.pack(pady=5)
    duration_entry = ctk.CTkEntry(log_workout_frame)
    duration_entry.pack(pady=5)

    def calculate_and_save():
        exercise_type = exercise_var.get()
        workout_date = calendar.get_date()
        duration = int(duration_entry.get())

        # Placeholder calculations
        calories_burnt = duration * 5  # Example: 5 calories per minute
        weight_loss = duration * 0.01  # Example: 0.01 kg per minute
        strength = duration * 0.1  # Example: strength increases by 0.1 units per minute
        stamina = duration / 10  # Example: stamina increases with duration

        # Save to file
        with open("FitnessTrackerData.txt", "a") as file:
            file.write(f"{email},{exercise_type},{workout_date},{duration},{calories_burnt},{weight_loss},{strength},{stamina}\n")

        messagebox.showinfo("Workout Logged", "Your workout has been logged successfully!")

    # Log button
    log_button = ctk.CTkButton(log_workout_frame, text="Log Workout", command=calculate_and_save)
    log_button.pack(pady=20)

def show_progress_line_graph(email):
    # Clear the current content
    for widget in main_content_frame.winfo_children():
        widget.destroy()

    progress_frame = ctk.CTkFrame(main_content_frame, fg_color="white", corner_radius=10)
    progress_frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Load user data
    user_data = load_user_data(email)
    workouts = user_data.get("workouts", [])

    # Prepare data for plotting
    exercise_types = []
    calories = []

    for workout in workouts:
        workout_details = workout.split(',')
        
        # Skip malformed entries
        if len(workout_details) < 5:  # We need at least 5 elements to get calories
            continue

        exercise_type = workout_details[0]
        try:
            calories_burnt = float(workout_details[4])  # Calories is the fifth item
        except (ValueError, IndexError):
            continue

        if exercise_type in exercise_types:
            index = exercise_types.index(exercise_type)
            calories[index] += calories_burnt
        else:
            exercise_types.append(exercise_type)
            calories.append(calories_burnt)

    # Create a bar graph
    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(exercise_types, calories, color=['#4CAF50', '#2196F3', '#FFC107'], edgecolor='black', linewidth=1.5)

    # Customize the graph
    ax.set_title("Calories Burned by Exercise Type", fontsize=16, fontweight='bold')
    ax.set_xlabel("Exercise Type", fontsize=12)
    ax.set_ylabel("Total Calories Burned", fontsize=12)
    ax.set_facecolor('#f0f0f0')
    ax.grid(False)

    # Set rounded edges for bars
    for bar in bars:
        bar.set_linewidth(0)
        bar.set_capstyle('round')

    # Embed the graph
    canvas = FigureCanvasTkAgg(fig, master=progress_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=10, fill='both', expand=True)

def show_lessons():
    print("Starting show_lessons function")  # Debug print 1
    
    # Clear the current content in the main content frame
    for widget in main_content_frame.winfo_children():
        widget.destroy()
    print("Cleared main content frame")  # Debug print 2

    # Set a background color
    inspiring_color = "#D3D3D3"

    # Create main container frame
    lessons_container = ctk.CTkFrame(main_content_frame, fg_color=inspiring_color)
    lessons_container.pack(fill="both", expand=True, padx=10, pady=10)
    print("Created lessons container")  # Debug print 3

    # Configure the grid
    lessons_container.grid_rowconfigure(0, weight=1)
    lessons_container.grid_rowconfigure(1, weight=8)
    lessons_container.grid_columnconfigure(0, weight=1)
    lessons_container.grid_columnconfigure(1, weight=3)

    # Header section
    header_frame = ctk.CTkFrame(lessons_container, height=100, fg_color=inspiring_color)
    header_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

    header_label = ctk.CTkLabel(header_frame, text="Workout Lessons", 
                               font=ctk.CTkFont(size=30, weight="bold"), 
                               text_color="black")
    header_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")

    # Sidebar for exercise list
    sidebar_frame = ctk.CTkFrame(lessons_container, width=350, fg_color=inspiring_color)
    sidebar_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
    sidebar_frame.grid_rowconfigure(1, weight=1)

    # Scrollable area for exercises
    scroll_canvas = ctk.CTkCanvas(sidebar_frame, bg=inspiring_color, bd=0, highlightthickness=0)
    scroll_canvas.grid(row=1, column=0, sticky="nsew")

    scrollbar = ctk.CTkScrollbar(sidebar_frame, command=scroll_canvas.yview)
    scrollbar.grid(row=1, column=1, sticky="ns")
    scroll_canvas.configure(yscrollcommand=scrollbar.set)

    # Create scrollable frame
    scrollable_frame = ctk.CTkFrame(scroll_canvas, fg_color=inspiring_color)
    scroll_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    scrollable_frame.bind("<Configure>", lambda e: scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all")))

    # Exercise list title
    exercise_list_label = ctk.CTkLabel(scrollable_frame, text="Exercises", 
                                     font=ctk.CTkFont(size=22, weight="bold"), 
                                     text_color="black")
    exercise_list_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    # Main content frame for exercise details
    content_frame = ctk.CTkFrame(lessons_container, fg_color=inspiring_color)
    content_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

    # Quote label
    quote_label = ctk.CTkLabel(content_frame, text="", 
                              font=ctk.CTkFont(size=24, weight="bold"), 
                              text_color="black")
    quote_label.grid(row=0, column=0, pady=20, sticky="n")

    # List of motivational quotes
    quotes = [
        "Stay Strong!",
        "Believe in Yourself!",
        "Push Your Limits!",
        "Keep Moving Forward!",
        "Success is Earned, Not Given!",
        "Focus on the Goal!",
        "You Are Your Only Limit!",
        "Make Every Workout Count!",
        "Dream Big, Lift Big!",
        "The Only Bad Workout is the One You Didn't Do!"
    ]

    # Function to update the quote
    def update_quote():
        quote = random.choice(quotes)
        quote_label.configure(text=quote)
        main_content_frame.after(5000, update_quote)

    # Function to display exercise details
    def display_exercise(exercise_name, image_file, instructions):
        for widget in content_frame.winfo_children():
            widget.destroy()

        try:
            image_path = os.path.join(image_directory, image_file)
            if not os.path.exists(image_path):
                print(f"Exercise image not found: {image_path}")
                return
            
            img = Image.open(image_path)
            img = img.resize((400, 300), Image.LANCZOS)
            img = ImageTk.PhotoImage(img)

            image_label = ctk.CTkLabel(content_frame, image=img, text="")
            image_label.image = img
            image_label.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

            instructions_label = ctk.CTkLabel(content_frame, 
                                           text=f"{exercise_name}\n\n{instructions}", 
                                           font=ctk.CTkFont(size=18), 
                                           justify="left")
            instructions_label.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")

        except Exception as e:
            print(f"Error loading image {image_file}: {e}")

    # Load exercises
    current_directory = os.path.dirname(os.path.abspath(__file__))
    image_directory = os.path.join(current_directory, "img")
    print(f"Image directory path: {image_directory}")  # Debug print 4
    print(f"Directory exists: {os.path.exists(image_directory)}")  # Debug print 5

    exercises = [
        ("Barbell Bench Press", "barbell bench press.jpg", 
         "1. Lie on a flat bench with your feet on the floor and hold the barbell with both hands.\n"
         "2. Lower the barbell to your chest while keeping your elbows at a 45-degree angle.\n"
         "3. Push the barbell back up until your arms are fully extended."),

        ("Deadlift", "deadlift.jpg", 
         "1. Stand with feet shoulder-width apart, bend your knees, and lift the barbell.\n"
         "2. Keep your back straight and lift with your legs, not your back.\n"
         "3. Lower the barbell back down with control."),

        ("Push Ups", "push ups.jpg", 
         "1. Start in a plank position, bend your elbows to lower your chest to the floor.\n"
         "2. Keep your body in a straight line from head to heels.\n"
         "3. Push back up to the starting position."),

        ("Dumbbell Workout", "with-dumbbells.jpg", 
         "1. Hold dumbbells in each hand and perform shoulder presses or other exercises.\n"
         "2. Keep your core engaged to maintain stability.\n"
         "3. Vary your exercises for a full-body workout."),

        ("Burpees", "burpees.jpg", 
         "1. Begin in a standing position, drop into a squat, jump back into a plank.\n"
         "2. Perform a push-up while in the plank position.\n"
         "3. Jump your feet back to your hands and leap into the air."),

        ("Jumping Rope", "jumping rope.jpg", 
         "1. Hold the handles of the jump rope and swing it over your head.\n"
         "2. Jump with both feet as the rope comes down.\n"
         "3. Keep a steady rhythm and try to increase your speed."),

        ("Plank", "Plank.jpg", 
         "1. Position your body in a straight line from head to heels.\n"
         "2. Keep your elbows directly under your shoulders.\n"
         "3. Engage your core and hold the position."),

        ("Russian Twists", "Russian Twists.jpg", 
         "1. Sit on the ground, lean back slightly, and rotate your torso.\n"
         "2. Hold a weight or your hands together as you twist.\n"
         "3. Keep your feet off the ground for an added challenge."),

        ("Arm Circles", "Arm circles.jpg", 
         "1. Stand with feet shoulder-width apart and rotate your arms in circles.\n"
         "2. Perform both small and large circles.\n"
         "3. Reverse the direction after 30 seconds."),

        ("Bench Mark", "bench mark.jpg", 
         "1. Lie on a flat bench with your feet flat on the ground, holding weights in your hands.\n"
         "2. Lower the weights to your chest slowly.\n"
         "3. Press the weights back up until your arms are straight."),
    ]

    for index, (exercise, image_file, instructions) in enumerate(exercises):
        try:
            image_path = os.path.join(image_directory, image_file)
            print(f"Trying to load image: {image_path}")  # Debug print 6
            print(f"Image file exists: {os.path.exists(image_path)}")  # Debug print 7

            if not os.path.exists(image_path):
                print(f"Exercise image not found: {image_path}")
                continue

            img = Image.open(image_path)
            print(f"Successfully opened image for {exercise}")  # Debug print 8
            img = img.resize((200, 200), Image.LANCZOS)
            img = ImageTk.PhotoImage(img)

            label = ctk.CTkLabel(scrollable_frame, image=img, text=exercise, 
                               compound="left", padx=10, pady=5)
            label.image = img  # Keep a reference!
            label.grid(row=index + 1, column=0, padx=10, pady=5, sticky="w")
            print(f"Created label for {exercise}")  # Debug print 9

            label.bind("<Button-1>", 
                      lambda e, ex=exercise, img=image_file, ins=instructions: 
                      display_exercise(ex, img, ins))

        except Exception as e:
            print(f"Error loading image {image_file}: {str(e)}")  # More detailed error message

    # Start updating quotes
    update_quote()

def show_settings():
    # Clear the current content
    for widget in main_content_frame.winfo_children():
        widget.destroy()

    # Create a frame for settings
    settings_frame = ctk.CTkFrame(main_content_frame, fg_color="white", corner_radius=10)
    settings_frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Settings title
    ctk.CTkLabel(settings_frame, text="Settings", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)

    # Theme settings
    theme_frame = ctk.CTkFrame(settings_frame)
    theme_frame.pack(pady=10, padx=20, fill="x")

    ctk.CTkLabel(theme_frame, text="App Theme:", font=ctk.CTkFont(size=16)).pack(side="left", padx=(0, 10))
    theme_var = ctk.StringVar(value=ctk.get_appearance_mode())
    theme_dropdown = ctk.CTkOptionMenu(theme_frame, values=["Light", "Dark", "System"], 
                                       variable=theme_var, command=change_theme)
    theme_dropdown.pack(side="left")

    # Remove color mode selection
    # ctk.CTkLabel(theme_frame, text="Color Mode:", font=ctk.CTkFont(size=16)).pack(side="left", padx=(20, 10))
    # color_mode_var = ctk.StringVar(value=ctk.get_default_color_theme())
    # color_mode_dropdown = ctk.CTkOptionMenu(theme_frame, values=["blue", "green", "dark-blue"], 
    #                                         variable=color_mode_var, command=change_color_mode)
    # color_mode_dropdown.pack(side="left")

    # Font size settings
    font_frame = ctk.CTkFrame(settings_frame)
    font_frame.pack(pady=10, padx=20, fill="x")

    ctk.CTkLabel(font_frame, text="Font Size:", font=ctk.CTkFont(size=16)).pack(side="left", padx=(0, 10))
    font_size_var = ctk.StringVar(value="Medium")
    font_size_dropdown = ctk.CTkOptionMenu(font_frame, values=["Small", "Medium", "Large"], 
                                           variable=font_size_var, command=change_font_size)
    font_size_dropdown.pack(side="left")

    # Notification settings
    notification_frame = ctk.CTkFrame(settings_frame)
    notification_frame.pack(pady=10, padx=20, fill="x")

    ctk.CTkLabel(notification_frame, text="Notifications:", font=ctk.CTkFont(size=16)).pack(side="left", padx=(0, 10))
    notification_var = ctk.BooleanVar(value=True)
    notification_switch = ctk.CTkSwitch(notification_frame, text="Enable", variable=notification_var, 
                                        command=toggle_notifications)
    notification_switch.pack(side="left")

    # Reminder settings
    reminder_frame = ctk.CTkFrame(settings_frame)
    reminder_frame.pack(pady=10, padx=20, fill="x")

    ctk.CTkLabel(reminder_frame, text="Workout Reminders:", font=ctk.CTkFont(size=16)).pack(side="left", padx=(0, 10))
    reminder_var = ctk.BooleanVar(value=False)
    reminder_switch = ctk.CTkSwitch(reminder_frame, text="Enable", variable=reminder_var, 
                                    command=toggle_reminders)
    reminder_switch.pack(side="left")

    # Save button
    save_button = ctk.CTkButton(settings_frame, text="Save Settings", command=save_settings)
    save_button.pack(pady=20)

def change_theme(new_theme):
    ctk.set_appearance_mode(new_theme)
    # You might want to update some UI elements here to reflect the new theme

def change_font_size(new_size):
    # This is a placeholder. You'd need to implement the logic to change font sizes throughout the app.
    print(f"Font size changed to: {new_size}")

def toggle_notifications():
    # This is a placeholder. You'd need to implement the logic for enabling/disabling notifications.
    enabled = notification_var.get()
    print(f"Notifications {'enabled' if enabled else 'disabled'}")

def toggle_reminders():
    enabled = reminder_var.get()
    print(f"Workout reminders {'enabled' if enabled else 'disabled'}")
    if enabled:
        # Show options for setting reminder frequency, time, etc.
        show_reminder_options()

def save_settings():
    settings = {
        "theme": theme_var.get(),
        # Remove color mode from settings
        # "color_mode": color_mode_var.get(),
        "font_size": font_size_var.get(),
        "notifications": notification_var.get(),
        "reminders": reminder_var.get(),
    }
    
    try:
        with open("user_settings.json", "w") as f:
            json.dump(settings, f)
        messagebox.showinfo("Settings Saved", "Your settings have been saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save settings: {e}")

def on_hover(button, enter):
    button.configure(fg_color="blue" if enter else "black")

def set_active(button):
    for b in nav_buttons:
        b.configure(fg_color="black")
    button.configure(fg_color="blue")

# Entry point for the app
if __name__ == "__main__":
    if len(sys.argv) > 1:
        email = sys.argv[1]  # Get the email from command-line arguments
        
        # Load user data including measurements
        user_data = load_user_data(email)
        
        # Try to get the user's name from the login data
        try:
            with open("users.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    data = line.strip().split(',')
                    if data[0] == email:
                        user_name = data[2]  # Assuming format is: email,password,name
                        break
                else:
                    user_name = "User"  # Fallback if name not found
        except FileNotFoundError:
            user_name = "User"
    else:
        email = "default@example.com"  # Fallback email if none is provided
        user_name = "User"  # Fallback name if none is provided

    create_dashboard(email, user_name)
