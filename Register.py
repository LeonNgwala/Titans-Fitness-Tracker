import customtkinter as ctk
import tkinter.messagebox as tkmb
import random
import string
import re
import subprocess

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("green")

def generate_password(length=12):
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special_chars = string.punctuation
    all_chars = lowercase + uppercase + digits + special_chars
    
    password = (
        random.choice(lowercase)
        + random.choice(uppercase)
        + random.choice(digits)
        + random.choice(special_chars)
        + ''.join(random.choice(all_chars) for _ in range(length - 4))
    )
    return ''.join(random.sample(password, len(password)))

def open_registration_window(main_app):
    main_app.withdraw()
    register_window = ctk.CTkToplevel(main_app)
    register_window.geometry("600x700")
    register_window.title("Titans Fitness Club - Register")
    register_window.geometry(f"{register_window.winfo_screenwidth()}x{register_window.winfo_screenheight()}+0+0")

    frame = ctk.CTkFrame(register_window, corner_radius=15, fg_color="dark gray")
    frame.pack(expand=True, fill="both", padx=20, pady=20)

    label_reg = ctk.CTkLabel(frame, text="Register", font=("Helvetica", 24, "bold"), text_color="black")
    label_reg.pack(pady=20)

    name_entry = ctk.CTkEntry(frame, placeholder_text="Full Name", width=300)
    name_entry.pack(pady=12)

    email_entry = ctk.CTkEntry(frame, placeholder_text="Email", width=300)
    email_entry.pack(pady=12)

    pass_entry = ctk.CTkEntry(frame, placeholder_text="Password", show="*", width=300)
    pass_entry.pack(pady=12)

    confirm_pass_entry = ctk.CTkEntry(frame, placeholder_text="Confirm Password", show="*", width=300)
    confirm_pass_entry.pack(pady=12)

    password_strength = ctk.CTkProgressBar(frame, width=300)
    password_strength.pack(pady=5)

    password_suggestion_label = ctk.CTkLabel(frame, text="Suggested Password:   ", font=("Roboto", 15), text_color="black")
    password_suggestion_label.pack(pady=5)

    def update_password_strength(*args):
        password = pass_entry.get()
        if not password:
            password_strength.set(0)
            password_strength.configure(progress_color="grey")
            return

        strength = 0
        if re.search(r"[a-z]", password): strength += 0.25
        if re.search(r"[A-Z]", password): strength += 0.25
        if re.search(r"\d", password): strength += 0.25
        if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password): strength += 0.25

        password_strength.set(strength)
        
        if strength < 0.5:
            password_strength.configure(progress_color="red")
        elif strength < 0.75:
            password_strength.configure(progress_color="yellow")
        else:
            password_strength.configure(progress_color="green")

    pass_entry.bind("<KeyRelease>", update_password_strength)

    def validate_email(email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+'
        return re.match(pattern, email) is not None

    def suggest_password():
        suggested_password = generate_password()
        password_suggestion_label.configure(text=f"Suggested Password: {suggested_password}")
        pass_entry.delete(0, 'end')
        pass_entry.insert(0, suggested_password)
        update_password_strength()

    def save_to_file(full_name, email, password):
        with open("FitnessTrackerData.txt", "a") as file:
            file.write(f"Full Name: {full_name}, Email: {email}, Password: {password}\n")
        tkmb.showinfo(title="Data Saved", message="Your data has been saved successfully!")

    def register():
        full_name = name_entry.get()
        email = email_entry.get()
        password = pass_entry.get()
        confirm_password = confirm_pass_entry.get()

        if not validate_email(email):
            tkmb.showerror(title="Invalid Email", message="Please enter a valid email address.")
            return

        if not (re.search(r"[a-z]", password) and re.search(r"[A-Z]", password) and 
                re.search(r"\d", password) and re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)):
            tkmb.showerror(title="Weak Password", message="Password must include lowercase, uppercase, numbers, and special characters.")
            return

        if password == confirm_password:
            save_to_file(full_name, email, password)
            tkmb.showinfo(title="Registration Successful", message=f"Welcome {full_name}! You've been registered.")
            register_window.destroy()

            # Save the email to a file for later tracking in login
            with open('current_user.txt', 'w') as user_file:
                user_file.write(f"{email}\n{password}\n")  # Save both email and password

            # Use subprocess to launch Welcome.py with the email
            print(f"Registering user with email: {email}")  # Debugging statement
            subprocess.Popen(['python', 'welcome.py', email])  # Pass email to Welcome.py

        else:
            tkmb.showerror(title="Registration Failed", message="Passwords do not match.")

    generate_pass_button = ctk.CTkButton(frame, text="Generate Strong Password", command=suggest_password, width=200)
    generate_pass_button.pack(pady=5)

    register_button = ctk.CTkButton(frame, text="Register", command=register, width=200)
    register_button.pack(pady=20)

    register_window.mainloop()
