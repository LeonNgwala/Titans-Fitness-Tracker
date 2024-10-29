import customtkinter as ctk
from PIL import Image, ImageTk
import tkinter.messagebox as tkmb
import sys
import os
import re
import hashlib
import random
import string
import json
import datetime
from tkcalendar import Calendar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import logging

class FitnessApp:
    def __init__(self):
        self.setup_logging()
        self.current_user = None
        self.current_screen = None
        self.setup_data_files()
        self.show_splash()

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def setup_data_files(self):
        # Ensure required data files exist
        required_files = ["FitnessTrackerData.txt", "users.txt"]
        for file in required_files:
            if not os.path.exists(file):
                with open(file, "w") as f:
                    pass

    def show_splash(self):
        self.root = ctk.CTk()
        self.splash = SplashScreen(self.root, self.show_login)
        self.root.mainloop()

    def show_login(self):
        if self.current_screen:
            self.current_screen.destroy()
        self.current_screen = LoginScreen(self.root, self.on_login_success, self.show_register)

    def show_register(self):
        if self.current_screen:
            self.current_screen.destroy()
        self.current_screen = RegisterScreen(self.root, self.on_register_success)

    def on_login_success(self, user_data):
        self.current_user = user_data
        self.show_welcome()

    def on_register_success(self, user_data):
        self.current_user = user_data
        self.show_welcome()

    def show_welcome(self):
        if self.current_screen:
            self.current_screen.destroy()
        self.current_screen = WelcomeScreen(self.root, self.current_user, self.show_goals)

    def show_goals(self):
        if self.current_screen:
            self.current_screen.destroy()
        self.current_screen = SetGoalsScreen(self.root, self.current_user, self.show_measurements)

    def show_measurements(self):
        if self.current_screen:
            self.current_screen.destroy()
        self.current_screen = MeasurementsScreen(self.root, self.current_user, self.show_dashboard)

    def show_dashboard(self):
        if self.current_screen:
            self.current_screen.destroy()
        self.current_screen = DashboardScreen(self.root, self.current_user, self.show_login)

class SplashScreen:
    def __init__(self, master, callback):
        self.master = master
        self.callback = callback
        
        # Configure the window
        self.master.geometry(f"{self.master.winfo_screenwidth()}x{self.master.winfo_screenheight()}")
        self.master.title("Welcome to Titans Fitness Club")
        self.master.attributes('-fullscreen', True)
        self.master.configure(fg_color="white")

        # Create center frame
        self.center_frame = ctk.CTkFrame(self.master, fg_color="transparent")
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Load logo
        try:
            logo_image = Image.open("icons/logo.jpg")
            logo_image.thumbnail((600, 400))
            self.logo_photo = ctk.CTkImage(light_image=logo_image, dark_image=logo_image)
            self.logo_label = ctk.CTkLabel(self.center_frame, image=self.logo_photo, text="")
            self.logo_label.pack(pady=(0, 20))
        except Exception as e:
            logging.error(f"Error loading logo: {e}")

        # Add labels and progress bar
        self.title_label = ctk.CTkLabel(
            self.center_frame,
            text="Titans Fitness",
            font=("Helvetica", 40, "bold"),
            text_color="black"
        )
        self.title_label.pack(pady=(0, 20))

        self.message_label = ctk.CTkLabel(
            self.center_frame,
            text="",
            font=("Helvetica", 16),
            text_color="black"
        )
        self.message_label.pack(pady=(0, 20))

        self.progress_bar = ctk.CTkProgressBar(
            self.center_frame,
            width=300,
            fg_color="white",
            progress_color="black"
        )
        self.progress_bar.pack(pady=(0, 20))
        self.progress_bar.set(0)

        # Version label
        self.version_label = ctk.CTkLabel(
            self.master,
            text="Version 1.0",
            font=("Helvetica", 12),
            text_color="black"
        )
        self.version_label.place(relx=0.95, rely=0.98, anchor="se")

        # Start loading animation
        self.load_animation()

    def load_animation(self, step=0):
        fitness_messages = [
            "Stay fit, stay healthy!",
            "Push your limits!",
            "Every workout counts!",
            "Stronger every day!",
            "Your only limit is you!",
            "Believe in yourself!",
            "Commit to be fit!",
            "Fitness is a journey, not a destination.",
            "Consistency is key!",
            "Make every rep count!"
        ]

        if step < 100:
            self.progress_bar.set((step + 1) / 100)
            self.message_label.configure(text=random.choice(fitness_messages))
            self.master.after(30, self.load_animation, step + 1)
        else:
            self.master.after(500, self.finish_splash)

    def finish_splash(self):
        # Clear splash screen contents
        for widget in self.master.winfo_children():
            widget.destroy()
        # Call the callback to show login screen
        self.callback()

class LoginScreen:
    def __init__(self, master, login_callback, register_callback):
        self.master = master
        self.login_callback = login_callback
        self.register_callback = register_callback

        # Create main frame
        self.main_frame = ctk.CTkFrame(master, fg_color="dark gray")
        self.main_frame.pack(expand=True, fill="both")

        # Title
        self.label = ctk.CTkLabel(
            self.main_frame,
            text="Login",
            font=("Helvetica", 24, "bold"),
            text_color="black"
        )
        self.label.pack(pady=20)

        # Email entry
        self.username_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Username (email)",
            width=300
        )
        self.username_entry.pack(pady=12)

        # Password entry
        self.password_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Password",
            show="*",
            width=300
        )
        self.password_entry.pack(pady=12)

        # Login button
        self.login_button = ctk.CTkButton(
            self.main_frame,
            text="Login",
            command=self.login,
            width=300,
            fg_color="black",
            text_color="white"
        )
        self.login_button.pack(pady=12)

        # Forgot password label
        self.forgot_password_label = ctk.CTkLabel(
            self.main_frame,
            text="Forgot Password?",
            cursor="hand2",
            text_color="white"
        )
        self.forgot_password_label.pack(pady=12)
        self.forgot_password_label.bind("<Button-1>", self.forgot_password)

        # Register label
        self.register_label = ctk.CTkLabel(
            self.main_frame,
            text="Don't have an account? Register here",
            cursor="hand2",
            text_color="white"
        )
        self.register_label.pack(pady=12)
        self.register_label.bind("<Button-1>", lambda e: self.register_callback())

    def login(self):
        email = self.username_entry.get()
        password = self.password_entry.get()

        if self.validate_login(email, password):
            user_data = self.get_user_data(email)
            self.login_callback(user_data)
        else:
            tkmb.showerror("Login Failed", "Invalid email or password")

    def validate_login(self, email, password):
        try:
            with open("FitnessTrackerData.txt", "r") as file:
                for line in file:
                    if f"Email: {email}" in line and f"Password: {hashlib.sha256(password.encode()).hexdigest()}" in line:
                        return True
        except FileNotFoundError:
            logging.error("FitnessTrackerData.txt not found")
        return False

    def get_user_data(self, email):
        try:
            with open("FitnessTrackerData.txt", "r") as file:
                for line in file:
                    if f"Email: {email}" in line:
                        parts = line.strip().split(", ")
                        return {
                            'name': parts[0].split(": ")[1],
                            'email': email
                        }
        except FileNotFoundError:
            logging.error("FitnessTrackerData.txt not found")
        return None

    def forgot_password(self, event=None):
        email = self.username_entry.get().strip()
        if not email:
            tkmb.showerror("Error", "Please enter your email address")
            return
        
        if self.email_exists(email):
            # In a real application, you would implement password reset functionality here
            tkmb.showinfo("Password Reset", 
                         "Password reset instructions have been sent to your email.")
        else:
            tkmb.showerror("Error", "Email not found in our records.")

    def email_exists(self, email):
        try:
            with open("FitnessTrackerData.txt", "r") as file:
                return any(f"Email: {email}" in line for line in file)
        except FileNotFoundError:
            return False

    def destroy(self):
        self.main_frame.destroy()

class RegisterScreen:
    def __init__(self, master, register_callback):
        self.master = master
        self.register_callback = register_callback

        # Create main frame
        self.frame = ctk.CTkFrame(master, corner_radius=15, fg_color="#f0f0f0")
        self.frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Title
        self.label_reg = ctk.CTkLabel(
            self.frame,
            text="Register",
            font=("Helvetica", 24, "bold"),
            text_color="#333333"
        )
        self.label_reg.pack(pady=20)

        # Entry fields
        self.name_entry = ctk.CTkEntry(
            self.frame,
            placeholder_text="Full Name",
            width=300,
            fg_color="#ffffff"
        )
        self.name_entry.pack(pady=12)

        self.email_entry = ctk.CTkEntry(
            self.frame,
            placeholder_text="Email",
            width=300,
            fg_color="#ffffff"
        )
        self.email_entry.pack(pady=12)

        # Password frame with visibility toggle
        self.pass_frame = ctk.CTkFrame(self.frame, fg_color="#f0f0f0")
        self.pass_frame.pack(pady=12, fill="x", padx=20)

        self.pass_entry = ctk.CTkEntry(
            self.pass_frame,
            placeholder_text="Password",
            show="*",
            width=150,
            fg_color="#ffffff"
        )
        self.pass_entry.pack(side="left", fill="x", expand=True)

        self.pass_visibility_icon = ctk.CTkButton(
            self.pass_frame,
            text="👁",
            width=40,
            command=lambda: self.toggle_password_visibility(self.pass_entry)
        )
        self.pass_visibility_icon.pack(side="right", padx=(5, 0))

        # Confirm password frame
        self.confirm_pass_frame = ctk.CTkFrame(self.frame, fg_color="#f0f0f0")
        self.confirm_pass_frame.pack(pady=12, fill="x", padx=20)

        self.confirm_pass_entry = ctk.CTkEntry(
            self.confirm_pass_frame,
            placeholder_text="Confirm Password",
            show="*",
            width=150,
            fg_color="#ffffff"
        )
        self.confirm_pass_entry.pack(side="left", fill="x", expand=True)

        # Password strength indicator
        self.password_strength = ctk.CTkProgressBar(self.frame, width=300)
        self.password_strength.pack(pady=5)
        self.password_strength.set(0)

        # Terms and conditions checkbox
        self.terms_var = ctk.BooleanVar()
        self.terms_checkbox = ctk.CTkCheckBox(
            self.frame,
            text="I agree to the Terms and Conditions",
            variable=self.terms_var
        )
        self.terms_checkbox.pack(pady=5)

        # Register button
        self.register_button = ctk.CTkButton(
            self.frame,
            text="Register",
            command=self.register,
            width=200,
            fg_color="#333333",
            text_color="#ffffff"
        )
        self.register_button.pack(pady=20)

        # Bind password strength checker
        self.pass_entry.bind("<KeyRelease>", self.update_password_strength)

    def toggle_password_visibility(self, entry):
        if entry.cget('show') == '*':
            entry.configure(show='')
        else:
            entry.configure(show='*')

    def update_password_strength(self, event=None):
        password = self.pass_entry.get()
        strength = 0
        
        if not password:
            self.password_strength.set(0)
            self.password_strength.configure(progress_color="white")
            return

        if re.search(r"[a-z]", password): strength += 0.25
        if re.search(r"[A-Z]", password): strength += 0.25
        if re.search(r"\d", password): strength += 0.25
        if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password): strength += 0.25

        self.password_strength.set(strength)
        
        if strength < 0.5:
            self.password_strength.configure(progress_color="red")
        elif strength < 0.75:
            self.password_strength.configure(progress_color="yellow")
        else:
            self.password_strength.configure(progress_color="green")

    def register(self):
        # Get values from entries
        full_name = self.name_entry.get()
        email = self.email_entry.get()
        password = self.pass_entry.get()
        confirm_password = self.confirm_pass_entry.get()

        # Validate inputs
        if not self.validate_registration(full_name, email, password, confirm_password):
            return

        # Save user data
        self.save_user_data(full_name, email, password)
        
        # Call callback with user data
        self.register_callback({
            'name': full_name,
            'email': email
        })

    def validate_registration(self, full_name, email, password, confirm_password):
        if not full_name:
            tkmb.showerror("Error", "Please enter your full name")
            return False

        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            tkmb.showerror("Error", "Please enter a valid email address")
            return False

        if len(password) < 8:
            tkmb.showerror("Error", "Password must be at least 8 characters long")
            return False

        if password != confirm_password:
            tkmb.showerror("Error", "Passwords do not match")
            return False

        if not self.terms_var.get():
            tkmb.showerror("Error", "Please accept the terms and conditions")
            return False

        return True

    def save_user_data(self, full_name, email, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        with open("FitnessTrackerData.txt", "a") as file:
            file.write(f"Full Name: {full_name}, Email: {email}, Password: {hashed_password}\n")

    def destroy(self):
        self.frame.destroy()

class WelcomeScreen:
    def __init__(self, master, user_data, next_callback):
        self.master = master
        self.user_data = user_data
        self.next_callback = next_callback

        # Create main frame
        self.main_frame = ctk.CTkFrame(master, corner_radius=0, fg_color="white")
        self.main_frame.pack(fill="both", expand=True)

        # Configure grid
        self.main_frame.grid_columnconfigure(0, weight=1, uniform="equal")
        self.main_frame.grid_columnconfigure(1, weight=2, uniform="equal")
        self.main_frame.grid_rowconfigure(0, weight=1)

        # Create left and right frames
        self.setup_left_frame()
        self.setup_right_frame()

    def setup_left_frame(self):
        # Left frame for text content
        left_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color="white")
        left_frame.grid(row=0, column=0, sticky="nsew", pady=100)

        # Title
        title_label = ctk.CTkLabel(
            left_frame,
            text="SET GOALS.\nLOG WORKOUTS.\nSTAY ON TRACK.",
            font=ctk.CTkFont(size=40, weight="bold")
        )
        title_label.pack(pady=(50, 20))

        # Description
        desc_label = ctk.CTkLabel(
            left_frame,
            text="Easily track your workouts, set training plans,\nand discover new workout routines to crush your goals.",
            font=ctk.CTkFont(size=14),
            justify="left"
        )
        desc_label.pack(pady=(0, 20))

        # Get Started button with arrow
        try:
            arrow_image = Image.open("img/arrow.png")
            arrow_image = arrow_image.resize((20, 20))
            self.arrow_image_tk = ImageTk.PhotoImage(arrow_image)
            
            start_button = ctk.CTkButton(
                left_frame,
                text="GET STARTED",
                command=self.next_callback,
                font=ctk.CTkFont(size=16, weight="bold"),
                width=200,
                fg_color="black",
                image=self.arrow_image_tk,
                compound="right"
            )
            start_button.pack(pady=(10, 20))
        except Exception as e:
            logging.error(f"Error loading arrow image: {e}")
            # Fallback button without arrow
            start_button = ctk.CTkButton(
                left_frame,
                text="GET STARTED",
                command=self.next_callback,
                font=ctk.CTkFont(size=16, weight="bold"),
                width=200,
                fg_color="black"
            )
            start_button.pack(pady=(10, 20))

    def setup_right_frame(self):
        # Right frame for image
        right_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color="white")
        right_frame.grid(row=0, column=1, sticky="nsew", pady=90)

        try:
            # Load and display main image
            image = Image.open("img/ketani.jpg")
            image = image.resize((800, 400))
            self.img = ImageTk.PhotoImage(image)
            
            image_label = ctk.CTkLabel(right_frame, image=self.img, text="")
            image_label.pack(pady=20)

            # Athlete name label
            athlete_label = ctk.CTkLabel(
                right_frame,
                text="WEINI KELATI\nPro Middle-Distance Runner",
                font=ctk.CTkFont(size=12),
                justify="right"
            )
            athlete_label.pack(pady=(0, 20))
        except Exception as e:
            logging.error(f"Error loading main image: {e}")
            # Fallback text if image fails to load
            error_label = ctk.CTkLabel(
                right_frame,
                text="Image not available",
                font=ctk.CTkFont(size=16)
            )
            error_label.pack(pady=20)

    def destroy(self):
        self.main_frame.destroy()

class SetGoalsScreen:
    def __init__(self, master, user_data, next_callback):
        self.master = master
        self.user_data = user_data
        self.next_callback = next_callback
        self.selected_fitness_goal = None
        self.selected_focus_areas = []
        self.checkboxes = {}

        # Create main frame
        self.main_frame = ctk.CTkFrame(master, corner_radius=10, fg_color="white")
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.create_main_menu()

    def create_main_menu(self):
        # Clear existing widgets
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Back button
        try:
            back_image = Image.open("img/icons-back.png").resize((30, 30), Image.LANCZOS)
            self.back_icon = ctk.CTkImage(back_image, size=(30, 30))
            back_button = ctk.CTkButton(
                self.main_frame,
                image=self.back_icon,
                text="",
                command=self.go_back,
                width=40
            )
            back_button.pack(side="top", anchor="nw", padx=10, pady=(10, 0))
        except Exception as e:
            logging.error(f"Error loading back icon: {e}")

        # Title
        self.label = ctk.CTkLabel(
            self.main_frame,
            text="Select Your Fitness Goal",
            font=("Arial", 30),
            fg_color="white"
        )
        self.label.pack(pady=40)

        # Goal buttons
        goals = ["Weight Loss", "Muscle Gain", "Body Shape", "Cardio"]
        for goal in goals:
            button = ctk.CTkButton(
                self.main_frame,
                text=goal,
                font=("Arial", 28),
                command=lambda g=goal: self.show_focus_areas(g)
            )
            button.pack(pady=10)

    def show_focus_areas(self, goal):
        self.selected_fitness_goal = goal
        
        # Clear existing widgets
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Back button
        try:
            back_image = Image.open("img/icons-back.png").resize((30, 30), Image.LANCZOS)
            self.back_icon = ctk.CTkImage(back_image, size=(30, 30))
            back_button = ctk.CTkButton(
                self.main_frame,
                image=self.back_icon,
                text="",
                command=self.create_main_menu,
                width=40
            )
            back_button.pack(side="top", anchor="nw", padx=10, pady=(10, 0))
        except Exception as e:
            logging.error(f"Error loading back icon: {e}")

        # Title
        self.label = ctk.CTkLabel(
            self.main_frame,
            text=f"Select Focus Areas for {goal}",
            font=("Arial", 30),
            fg_color="white"
        )
        self.label.pack(pady=40)

        # Focus area checkboxes
        focus_areas = ['Legs', 'Back', 'Shoulders', 'Arms', 'Abs', 'Butt', 'Chest', 'Full Body']
        for area in focus_areas:
            var = ctk.BooleanVar()
            checkbox = ctk.CTkCheckBox(
                self.main_frame,
                text=area,
                font=("Arial", 25),
                variable=var,
                command=lambda a=area, v=var: self.update_selection(a, v)
            )
            checkbox.pack(pady=10)
            self.checkboxes[area] = var

        # Continue button
        continue_button = ctk.CTkButton(
            self.main_frame,
            text="Continue",
            font=("Arial", 25),
            command=self.continue_to_next_page
        )
        continue_button.pack(pady=30)

    def update_selection(self, area, var):
        if var.get():
            if area not in self.selected_focus_areas:
                self.selected_focus_areas.append(area)
        else:
            if area in self.selected_focus_areas:
                self.selected_focus_areas.remove(area)

    def continue_to_next_page(self):
        if not self.selected_focus_areas:
            tkmb.showwarning("Warning", "Please select at least one focus area")
            return

        # Save goals and focus areas to user data
        self.user_data['fitness_goal'] = self.selected_fitness_goal
        self.user_data['focus_areas'] = self.selected_focus_areas

        # Save to file
        with open("FitnessTrackerData.txt", "a") as file:
            file.write(
                f"Email: {self.user_data['email']}, "
                f"Fitness Goal: {self.selected_fitness_goal}, "
                f"Focus Areas: {', '.join(self.selected_focus_areas)}\n"
            )

        # Proceed to next screen
        self.next_callback()

    def go_back(self):
        # Implementation depends on your navigation needs
        pass

    def destroy(self):
        self.main_frame.destroy()

class MeasurementsScreen:
    def __init__(self, master, user_data, next_callback):
        self.master = master
        self.user_data = user_data
        self.next_callback = next_callback
        self.email = user_data['email']

        # Configure the window
        self.master.title("Titans Fitness Club - Measurements")
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(master, fg_color="#d9dadd")
        self.main_frame.pack(fill="both", expand=True)

        # Load icons
        self.load_icons()
        
        # Create UI elements
        self.create_widgets()

    def load_icons(self):
        try:
            # Load back icon
            self.logo_image = Image.open("./img/back-icon.png").resize((50, 50))
            self.logo_image_tk = ImageTk.PhotoImage(self.logo_image)
            
            # Load gender icons
            self.male_icon = ImageTk.PhotoImage(Image.open("./img/male.png").resize((40, 40)))
            self.female_icon = ImageTk.PhotoImage(Image.open("./img/female.png").resize((40, 40)))
            
            # Load measurement icons
            self.weight_icon = ImageTk.PhotoImage(Image.open("./img/weight.png").resize((20, 20)))
            self.height_icon = ImageTk.PhotoImage(Image.open("./img/height.png").resize((20, 20)))
            self.age_icon = ImageTk.PhotoImage(Image.open("./img/age.png").resize((20, 20)))
            
            logging.info("All icons loaded successfully")
        except Exception as e:
            logging.error(f"Error loading icons: {e}")
            self.logo_image_tk = self.male_icon = self.female_icon = None
            self.weight_icon = self.height_icon = self.age_icon = None

    def create_widgets(self):
        # Create shadow frame
        shadow_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="#fbfcf8",
            width=600,
            height=600,
            border_color="#fffdd0"
        )
        shadow_frame.place(relx=0.5, rely=0.5, anchor="center", x=5, y=5)

        # Create content frame
        content_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="#d9dadd",
            width=800,
            height=590
        )
        content_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        title_label = ctk.CTkLabel(
            content_frame,
            text="Measurements",
            font=("Helvetica", 24)
        )
        title_label.pack(pady=30)

        # Gender selection
        self.create_gender_selection(content_frame)

        # Measurements entries
        self.create_measurement_entries(content_frame)

        # Continue button
        continue_button = ctk.CTkButton(
            content_frame,
            text="Continue",
            command=self.calculate_bmi,
            corner_radius=10
        )
        continue_button.pack(pady=20)

    def create_gender_selection(self, parent):
        gender_label = ctk.CTkLabel(
            parent,
            text="Select your gender",
            text_color="#2c4fd1",
            font=("Helvetica", 14)
        )
        gender_label.pack(pady=10)

        self.gender_var = ctk.StringVar(value="Male")
        
        # Male button
        self.male_button = ctk.CTkButton(
            parent,
            text="Male",
            image=self.male_icon,
            compound="left",
            fg_color="white",
            text_color="black",
            command=lambda: self.select_gender("Male")
        )
        self.male_button.pack(pady=5)

        # Female button
        self.female_button = ctk.CTkButton(
            parent,
            text="Female",
            image=self.female_icon,
            compound="left",
            fg_color="white",
            text_color="black",
            command=lambda: self.select_gender("Female")
        )
        self.female_button.pack(pady=5)

    def create_measurement_entries(self, parent):
        # Weight entry
        weight_label = ctk.CTkLabel(
            parent,
            text=" Weight",
            image=self.weight_icon,
            compound="left",
            text_color="#2c4fd1",
            font=("Helvetica", 14)
        )
        weight_label.pack(pady=10)
        
        self.weight_entry = ctk.CTkEntry(
            parent,
            placeholder_text="Weight in kg",
            corner_radius=10,
            width=300
        )
        self.weight_entry.pack(pady=10)

        # Height entry
        height_label = ctk.CTkLabel(
            parent,
            text=" Height",
            image=self.height_icon,
            compound="left",
            text_color="#2c4fd1",
            font=("Helvetica", 14)
        )
        height_label.pack(pady=10)
        
        self.height_entry = ctk.CTkEntry(
            parent,
            placeholder_text="Height in meters",
            corner_radius=10,
            width=300
        )
        self.height_entry.pack(pady=10)

        # Age entry
        age_label = ctk.CTkLabel(
            parent,
            text=" Age",
            image=self.age_icon,
            compound="left",
            text_color="#2c4fd1",
            font=("Helvetica", 14)
        )
        age_label.pack(pady=10)
        
        self.age_entry = ctk.CTkEntry(
            parent,
            placeholder_text="Age",
            corner_radius=10,
            width=300
        )
        self.age_entry.pack(pady=10)

    def select_gender(self, gender):
        self.gender_var.set(gender)
        if gender == "Male":
            self.male_button.configure(fg_color="#a5c6ff")
            self.female_button.configure(fg_color="white")
        else:
            self.female_button.configure(fg_color="#ffb3c6")
            self.male_button.configure(fg_color="white")

    def calculate_bmi(self):
        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())
            age = int(self.age_entry.get())
            gender = self.gender_var.get()

            if height <= 0:
                raise ValueError("Height must be greater than 0")

            # Calculate BMI
            bmi = weight / (height ** 2)

            # Determine BMI category
            if bmi < 18.5:
                category = "Underweight"
            elif 18.5 <= bmi < 25:
                category = "Normal weight"
            elif 25 <= bmi < 30:
                category = "Overweight"
            else:
                category = "Obesity"

            # Save measurements data
            self.save_measurements(weight, height, bmi, category, gender, age)

            # Show result
            tkmb.showinfo("BMI Result", f"Your BMI is {bmi:.2f} ({category})")

            # Update user data
            self.user_data.update({
                'weight': weight,
                'height': height,
                'bmi': bmi,
                'gender': gender,
                'age': age
            })

            # Proceed to next screen
            self.next_callback()

        except ValueError as e:
            tkmb.showerror("Input Error", f"Invalid input: {e}")

    def save_measurements(self, weight, height, bmi, category, gender, age):
        with open("FitnessTrackerData.txt", "a") as file:
            file.write(
                f"Email: {self.email}, "
                f"Weight: {weight} kg, "
                f"Height: {height} m, "
                f"BMI: {bmi:.2f}, "
                f"Category: {category}, "
                f"Gender: {gender}, "
                f"Age: {age} |\n"
            )

    def destroy(self):
        self.main_frame.destroy()

class DashboardScreen:
    def __init__(self, master, user_data, logout_callback):
        self.master = master
        self.user_data = user_data
        self.logout_callback = logout_callback
        
        # Initialize variables
        self.nav_buttons = []
        self.current_content = None
        self.notification_var = ctk.StringVar()
        
        # Configure the window
        self.master.title("Titan Fitness Tracker/Dashboard")
        
        # Create main layout
        self.create_layout()
        
        # Show default content (overview)
        self.show_overview()

    def create_layout(self):
        # Welcome header
        self.create_welcome_header()
        
        # Create main container
        self.main_container = ctk.CTkFrame(self.master)
        self.main_container.pack(fill="both", expand=True)
        
        # Create sidebar
        self.create_sidebar()
        
        # Create main content area
        self.content_frame = ctk.CTkFrame(self.main_container, fg_color="white")
        self.content_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

    def create_welcome_header(self):
        try:
            welcome_icon = ctk.CTkImage(
                light_image=Image.open("icons/welcome_icon.png"),
                size=(20, 20)
            )
        except Exception:
            welcome_icon = None

        welcome_label = ctk.CTkLabel(
            self.master,
            text=f"Welcome, {self.user_data.get('name', 'User')}!",
            font=("Helvetica", 16),
            image=welcome_icon,
            compound="left"
        )
        welcome_label.pack(pady=20)

    def create_sidebar(self):
        # Create sidebar frame
        sidebar = ctk.CTkFrame(self.main_container, width=200, corner_radius=0)
        sidebar.pack(side="left", fill="y")
        
        # Create profile section
        self.create_profile_section(sidebar)
        
        # Create navigation buttons
        self.create_nav_buttons(sidebar)

    def create_profile_section(self, sidebar):
        profile_frame = ctk.CTkFrame(sidebar, height=150, corner_radius=0)
        profile_frame.pack(fill="x")

        try:
            profile_icon = ctk.CTkImage(
                light_image=Image.open("icons/logo2.png"),
                size=(80, 80)
            )
            profile_picture = ctk.CTkLabel(
                profile_frame,
                image=profile_icon,
                text=""
            )
            profile_picture.pack(pady=10)
        except Exception as e:
            logging.error(f"Error loading profile icon: {e}")

        profile_label = ctk.CTkLabel(
            profile_frame,
            text=self.user_data.get('email', 'User'),
            font=ctk.CTkFont(size=16, weight="bold")
        )
        profile_label.pack(pady=5)

    def create_nav_buttons(self, sidebar):
        nav_items = [
            ("Overview", self.show_overview),
            ("Workouts", self.show_workouts),
            ("Progress", self.show_progress),
            ("History", self.show_history),
            ("Settings", self.show_settings),
            ("Logout", self.logout)
        ]

        for text, command in nav_items:
            try:
                icon = ctk.CTkImage(
                    light_image=Image.open(f"icons/{text.lower()}.png"),
                    size=(20, 20)
                )
            except Exception:
                icon = None

            button = ctk.CTkButton(
                sidebar,
                text=text,
                image=icon,
                compound="left",
                command=command,
                font=ctk.CTkFont(size=14),
                corner_radius=10
            )
            button.pack(pady=10, padx=10, fill="x")
            self.nav_buttons.append(button)

    def clear_content(self):
        if self.current_content:
            self.current_content.destroy()
        self.current_content = ctk.CTkFrame(self.content_frame, fg_color="white")
        self.current_content.pack(fill="both", expand=True)

    def show_overview(self):
        self.clear_content()
        
        # Create overview widgets
        title = ctk.CTkLabel(
            self.current_content,
            text="Dashboard Overview",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=20)

        # Stats grid
        stats_frame = ctk.CTkFrame(self.current_content)
        stats_frame.pack(pady=20, padx=20, fill="x")

        stats = [
            ("Current Weight", f"{self.user_data.get('weight', 0)} kg"),
            ("BMI", f"{self.user_data.get('bmi', 0):.1f}"),
            ("Fitness Goal", self.user_data.get('fitness_goal', 'Not set')),
            ("Focus Areas", ", ".join(self.user_data.get('focus_areas', [])))
        ]

        for i, (label, value) in enumerate(stats):
            stat_frame = ctk.CTkFrame(stats_frame)
            stat_frame.grid(row=i//2, column=i%2, padx=10, pady=10, sticky="nsew")
            
            ctk.CTkLabel(
                stat_frame,
                text=label,
                font=ctk.CTkFont(size=14)
            ).pack(pady=5)
            
            ctk.CTkLabel(
                stat_frame,
                text=value,
                font=ctk.CTkFont(size=16, weight="bold")
            ).pack(pady=5)

    def show_workouts(self):
        self.clear_content()
        
        title = ctk.CTkLabel(
            self.current_content,
            text="Workout Planner",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=20)

        # Calendar widget
        calendar = Calendar(self.current_content)
        calendar.pack(pady=20)

        # Workout form
        form_frame = ctk.CTkFrame(self.current_content)
        form_frame.pack(pady=20, padx=20, fill="x")

        # Workout type selection
        workout_types = ["Cardio", "Strength", "Flexibility", "HIIT"]
        workout_var = ctk.StringVar(value=workout_types[0])
        
        ctk.CTkLabel(
            form_frame,
            text="Workout Type:"
        ).pack(pady=5)
        
        workout_menu = ctk.CTkOptionMenu(
            form_frame,
            values=workout_types,
            variable=workout_var
        )
        workout_menu.pack(pady=5)

        # Duration entry
        ctk.CTkLabel(
            form_frame,
            text="Duration (minutes):"
        ).pack(pady=5)
        
        duration_entry = ctk.CTkEntry(form_frame)
        duration_entry.pack(pady=5)

        # Save button
        save_button = ctk.CTkButton(
            form_frame,
            text="Save Workout",
            command=lambda: self.save_workout(
                calendar.get_date(),
                workout_var.get(),
                duration_entry.get()
            )
        )
        save_button.pack(pady=20)

    def show_progress(self):
        self.clear_content()
        
        title = ctk.CTkLabel(
            self.current_content,
            text="Progress Tracking",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=20)

        # Create matplotlib figure
        fig, ax = plt.subplots(figsize=(8, 6))
        
        # Sample data - replace with actual tracking data
        dates = ["Jan", "Feb", "Mar", "Apr", "May"]
        weights = [75, 74, 73, 72, 71]
        
        ax.plot(dates, weights, marker='o')
        ax.set_title("Weight Progress")
        ax.set_xlabel("Month")
        ax.set_ylabel("Weight (kg)")
        
        # Embed plot in tkinter
        canvas = FigureCanvasTkAgg(fig, self.current_content)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=20)

    def show_history(self):
        self.clear_content()
        
        title = ctk.CTkLabel(
            self.current_content,
            text="Workout History",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=20)

        # Create scrollable text widget
        history_text = ctk.CTkTextbox(
            self.current_content,
            width=400,
            height=300
        )
        history_text.pack(pady=20, padx=20)

        # Load workout history
        try:
            with open("workout_history.txt", "r") as file:
                history = file.read()
                history_text.insert("1.0", history)
        except FileNotFoundError:
            history_text.insert("1.0", "No workout history found.")
        
        history_text.configure(state="disabled")

    def show_settings(self):
        self.clear_content()
        
        title = ctk.CTkLabel(
            self.current_content,
            text="Settings",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=20)

        settings_frame = ctk.CTkFrame(self.current_content)
        settings_frame.pack(pady=20, padx=20, fill="x")

        # Theme setting
        theme_frame = ctk.CTkFrame(settings_frame)
        theme_frame.pack(pady=10, fill="x")
        
        ctk.CTkLabel(
            theme_frame,
            text="App Theme:"
        ).pack(side="left", padx=10)
        
        theme_var = ctk.StringVar(value=ctk.get_appearance_mode())
        theme_menu = ctk.CTkOptionMenu(
            theme_frame,
            values=["Light", "Dark", "System"],
            variable=theme_var,
            command=self.change_theme
        )
        theme_menu.pack(side="right", padx=10)

        # Notification settings
        notif_frame = ctk.CTkFrame(settings_frame)
        notif_frame.pack(pady=10, fill="x")
        
        ctk.CTkLabel(
            notif_frame,
            text="Notifications:"
        ).pack(side="left", padx=10)
        
        notif_var = ctk.BooleanVar(value=True)
        notif_switch = ctk.CTkSwitch(
            notif_frame,
            text="Enable",
            variable=notif_var,
            command=self.toggle_notifications
        )
        notif_switch.pack(side="right", padx=10)

    def save_workout(self, date, workout_type, duration):
        try:
            duration = int(duration)
            with open("workout_history.txt", "a") as file:
                file.write(f"{date}: {workout_type} - {duration} minutes\n")
            tkmb.showinfo("Success", "Workout saved successfully!")
        except ValueError:
            tkmb.showerror("Error", "Please enter a valid duration")

    def change_theme(self, new_theme):
        ctk.set_appearance_mode(new_theme)

    def toggle_notifications(self):
        # Implement notification toggle functionality
        pass

    def logout(self):
        if tkmb.askyesno("Logout", "Are you sure you want to logout?"):
            self.logout_callback()

    def destroy(self):
        self.master.destroy()

class FitnessTrackerApp:
    def __init__(self):
        # Initialize main window
        self.root = ctk.CTk()
        self.root.title("Titans Fitness Tracker")
        
        # Set default theme and appearance
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Set window size to fullscreen
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}+0+0")
        
        # Initialize data files
        self.initialize_data_files()
        
        # Start with splash screen
        self.show_splash()
        
        # Start the application
        self.root.mainloop()

    def initialize_data_files(self):
        """Initialize necessary data files if they don't exist"""
        required_files = [
            "FitnessTrackerData.txt",
            "workout_history.txt",
            "user_settings.json"
        ]
        
        for file in required_files:
            try:
                if not os.path.exists(file):
                    if file.endswith('.json'):
                        with open(file, 'w') as f:
                            json.dump({}, f)
                    else:
                        with open(file, 'w') as f:
                            pass
                    logging.info(f"Created new file: {file}")
            except Exception as e:
                logging.error(f"Error creating file {file}: {e}")

    def show_splash(self):
        """Show splash screen and schedule login screen"""
        self.clear_current_screen()
        self.current_screen = SplashScreen(self.root, self.show_login)

    def show_login(self):
        """Show login screen"""
        self.clear_current_screen()
        self.current_screen = LoginScreen(self.root, self.handle_login, self.show_register)

    def show_register(self):
        """Show registration screen"""
        self.clear_current_screen()
        self.current_screen = RegisterScreen(self.root, self.handle_registration)

    def show_welcome(self, user_data):
        """Show welcome screen"""
        self.clear_current_screen()
        self.current_screen = WelcomeScreen(self.root, user_data, lambda: self.show_goals(user_data))

    def show_goals(self, user_data):
        """Show goals selection screen"""
        self.clear_current_screen()
        self.current_screen = SetGoalsScreen(self.root, user_data, lambda: self.show_measurements(user_data))

    def show_measurements(self, user_data):
        """Show measurements screen"""
        self.clear_current_screen()
        self.current_screen = MeasurementsScreen(self.root, user_data, lambda: self.show_dashboard(user_data))

    def show_dashboard(self, user_data):
        """Show main dashboard"""
        self.clear_current_screen()
        self.current_screen = DashboardScreen(self.root, user_data, self.handle_logout)

    def clear_current_screen(self):
        """Clear the current screen if it exists"""
        if hasattr(self, 'current_screen') and self.current_screen:
            try:
                self.current_screen.destroy()
            except Exception as e:
                logging.error(f"Error destroying current screen: {e}")
            self.current_screen = None

    def handle_login(self, user_data):
        """Handle successful login"""
        try:
            self.load_user_settings(user_data['email'])
            self.show_welcome(user_data)
        except Exception as e:
            logging.error(f"Error handling login: {e}")
            tkmb.showerror("Error", "An error occurred during login")

    def handle_registration(self, user_data):
        """Handle successful registration"""
        try:
            self.create_user_settings(user_data['email'])
            self.show_welcome(user_data)
        except Exception as e:
            logging.error(f"Error handling registration: {e}")
            tkmb.showerror("Error", "An error occurred during registration")

    def handle_logout(self):
        """Handle user logout"""
        try:
            self.save_user_settings()
            self.show_login()
        except Exception as e:
            logging.error(f"Error handling logout: {e}")
            tkmb.showerror("Error", "An error occurred during logout")

    def load_user_settings(self, email):
        """Load user settings from JSON file"""
        try:
            with open("user_settings.json", 'r') as f:
                settings = json.load(f)
                if email in settings:
                    user_settings = settings[email]
                    ctk.set_appearance_mode(user_settings.get('theme', 'light'))
        except Exception as e:
            logging.error(f"Error loading user settings: {e}")

    def create_user_settings(self, email):
        """Create default settings for new user"""
        try:
            with open("user_settings.json", 'r+') as f:
                settings = json.load(f)
                settings[email] = {
                    'theme': 'light',
                    'notifications': True,
                    'reminders': True
                }
                f.seek(0)
                json.dump(settings, f)
        except Exception as e:
            logging.error(f"Error creating user settings: {e}")

    def save_user_settings(self):
        """Save current settings"""
        # Implementation depends on what settings need to be saved
        pass

def setup_logging():
    """Set up logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('fitness_tracker.log'),
            logging.StreamHandler()
        ]
    )

def check_dependencies():
    """Check if all required dependencies are available"""
    required_packages = [
        'customtkinter',
        'pillow',
        'tkcalendar',
        'matplotlib'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("Missing required packages:", ", ".join(missing_packages))
        print("Please install them using: pip install", " ".join(missing_packages))
        return False
    return True

def main():
    """Main entry point of the application"""
    try:
        # Set up logging
        setup_logging()
        
        # Check dependencies
        if not check_dependencies():
            return
        
        # Log application start
        logging.info("Starting Fitness Tracker Application")
        
        # Create and start the application
        app = FitnessTrackerApp()
        
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        tkmb.showerror("Fatal Error", 
                      "An unexpected error occurred. Please check the logs for details.")

if __name__ == "__main__":
    main()
