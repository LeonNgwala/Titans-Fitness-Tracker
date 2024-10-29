import customtkinter as ctk
import tkinter.messagebox as tkmb
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import dashboard  # Add this import at the top

# Set the appearance mode and default color theme
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("green")

# Create the main app window
app = ctk.CTk()
app.title("Titans Fitness Club - Login")

# Set the window size to full screen
app.geometry(f"{app.winfo_screenwidth()}x{app.winfo_screenheight()}+0+0")

# Create a main frame to hold all widgets with a matching background
main_frame = ctk.CTkFrame(app, fg_color="dark gray")
main_frame.pack(expand=True, fill="both")

# Function to get user data from the file
def get_user_data():
    user_data = {}
    try:
        with open("FitnessTrackerData.txt", "r") as file:
            for line in file:
                # Split by commas
                parts = line.strip().split(", ")
                if len(parts) == 3:  # Ensure correct number of elements
                    try:
                        # Split by ": " to get key-value pairs
                        name = parts[0].split(": ")[1]
                        email = parts[1].split(": ")[1]
                        password = parts[2].split(": ")[1]
                        user_data[email] = {"name": name, "password": password}
                    except IndexError:
                        print(f"Error parsing line: {line}. Skipping.")
                else:
                    print(f"Line format incorrect: {line}. Skipping.")
    except FileNotFoundError:
        print("FitnessTrackerData.txt not found. No user data available.")
    
    return user_data

# Login function
def login():
    email = username_entry.get()
    password = password_entry.get()

    # Load the user data from the file
    users = get_user_data()

    # Check if the email exists and password matches
    if email in users:
        if users[email]["password"] == password:
            tkmb.showinfo(title="Login Successful", message=f"Welcome {users[email]['name']}!")
            app.withdraw()  # Hide the login window instead of destroying it
            dashboard.open_dashboard(email, users[email])  # Pass both email and user data
            app.destroy()  # Close the login window after dashboard is closed
        else:
            tkmb.showerror(title="Login Failed", message="Invalid password")
    else:
        tkmb.showerror(title="Login Failed", message="Invalid email")

# Function to open the registration window
def open_registration_window():
    import Register  # Import the Register module
    Register.open_registration_window(app)

# Function to send reset password email
def send_reset_email(recipient_email):
    sender_email = "your_email@example.com"  # Replace with your email
    sender_password = "your_password"  # Replace with your email password

    subject = "Password Reset Request"
    body = "Click the link below to reset your password:\n\nhttp://example.com/reset-password"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:  # For Gmail
            server.starttls()  # Enable security
            server.login(sender_email, sender_password)  # Log in
            server.send_message(msg)  # Send email
            tkmb.showinfo("Success", f"Reset link has been sent to {recipient_email}")
    except Exception as e:
        print(e)  # Print the error to the console
        tkmb.showerror("Error", f"Failed to send email: {str(e)}")

# Function to handle forgot password
def forgot_password():
    email = username_entry.get().strip()
    if not email:
        tkmb.showerror("Error", "Please enter your email address")
        return
    
    # Check if the email exists in user data
    users = get_user_data()
    if email in users:
        send_reset_email(email)  # Send the reset email
        tkmb.showinfo("Info", "If your email exists in our records, a password reset link has been sent.")
    else:
        tkmb.showerror("Error", "Email not found in our records.")

# Label for the app title
label = ctk.CTkLabel(main_frame, text="Login", font=("Helvetica", 24, "bold"), text_color="black")
label.pack(pady=20)

# Email entry
username_entry = ctk.CTkEntry(main_frame, placeholder_text="Username (email)", width=300)
username_entry.pack(pady=12)

# Password entry
password_entry = ctk.CTkEntry(main_frame, placeholder_text="Password", show="*", width=300)
password_entry.pack(pady=12)

# Login button
login_button = ctk.CTkButton(main_frame, text="Login", command=login, width=300, fg_color="black", text_color="white")
login_button.pack(pady=12)

# Forgot password label (link-like)
forgot_password_label = ctk.CTkLabel(main_frame, text="Forgot Password?", cursor="hand2", text_color="white")
forgot_password_label.pack(pady=12)
forgot_password_label.bind("<Button-1>", lambda e: forgot_password())  # Bind click to forgot_password function

# Register label
register_label = ctk.CTkLabel(main_frame, text="Don't have an account? Register here", cursor="hand2", text_color="white")
register_label.pack(pady=12)
register_label.bind("<Button-1>", lambda e: open_registration_window())

# Start the application
app.mainloop()
