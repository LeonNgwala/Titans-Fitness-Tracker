import customtkinter as ctk
from tkinter import messagebox
import subprocess
import sys
from PIL import Image, ImageTk
import dashboard  # Add this import at the top

DATA_FILE = "FitnessTrackerData.txt"

class FitnessApp(ctk.CTk):
    def __init__(self, email):
        super().__init__()
        self.title("Titans Fitness Club - Measurements")
        # Set the window size to full screen
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")

        # Store email
        self.email = email  

        # Load arrow image for buttons
        try:
            self.arrow_image = ImageTk.PhotoImage(Image.open("./img/arrow.png").resize((20, 20)))
            print("Arrow image loaded successfully")
        except Exception as e:
            print(f"Error loading arrow image: {e}")
            self.arrow_image = None

        # Load back icon for top-left corner
        try:
            self.logo_image = Image.open("./img/back-icon.png").resize((50, 50))  
            self.logo_image_tk = ImageTk.PhotoImage(self.logo_image)
            print("Logo image loaded successfully")
        except Exception as e:
            print(f"Error loading logo image: {e}")
            self.logo_image_tk = None

        # Create label for the logo image and place it at the top-left
        self.logo_label = ctk.CTkLabel(self, image=self.logo_image_tk, text="")  # Empty text for just the image
        self.logo_label.place(x=20, y=20)  # Adjust the x, y coordinates for positioning
        self.logo_label.bind("<Button-1>", self.go_back)

        # Create UI elements
        self.create_widgets()

    def create_widgets(self):
        # Title Label
        title_label = ctk.CTkLabel(self, text="Measurements", font=("Helvetica", 24))
        title_label.pack(pady=30)

        # Create shadow frame
        shadow_frame = ctk.CTkFrame(self,fg_color="#fbfcf8", width=600, height=600, border_color="#fffdd0")  # Adjust size for shadow
        shadow_frame.place(relx=0.5, rely=0.5, anchor="center", x=5, y=5)  # Slightly offset for shadow effect

        # Create the main frame and center it
        main_frame = ctk.CTkFrame(self, fg_color="#d9dadd", width=800, height=590)  # Adjust height accordingly
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Gender selection
        gender_label = ctk.CTkLabel(main_frame, text="Select your gender", text_color="#2c4fd1", font=("Helvetica", 14))
        gender_label.pack(pady=10)

        # Load gender icons
        try:
            self.male_icon = ImageTk.PhotoImage(Image.open("./img/male.png").resize((40, 40)))
            self.female_icon = ImageTk.PhotoImage(Image.open("./img/female.png").resize((40, 40)))
        except Exception as e:
            print(f"Error loading gender icons: {e}")
            self.male_icon = self.female_icon = None

        # Male and Female buttons with icons
        self.gender_var = ctk.StringVar(value="Male")
        self.male_button = ctk.CTkButton(main_frame, text="Male", image=self.male_icon, compound="left", fg_color="white", text_color="black", command=lambda: self.select_gender("Male"))
        self.female_button = ctk.CTkButton(main_frame, text="Female", image=self.female_icon, compound="left", fg_color="white", text_color="black", command=lambda: self.select_gender("Female"))
        self.male_button.pack(pady=5)
        self.female_button.pack(pady=5)

        # Load weight, height, and age icons
        try:
            self.weight_icon = ImageTk.PhotoImage(Image.open("./img/weight.png").resize((20, 20)))
            self.height_icon = ImageTk.PhotoImage(Image.open("./img/height.png").resize((20, 20)))
            self.age_icon = ImageTk.PhotoImage(Image.open("./img/age.png").resize((20, 20)))
        except Exception as e:
            print(f"Error loading input icons: {e}")
            self.weight_icon = self.height_icon = self.age_icon = None

        # Weight entry with icon
        weight_label = ctk.CTkLabel(main_frame, text=" Weight", image=self.weight_icon, compound="left", text_color="#2c4fd1", font=("Helvetica", 14))
        weight_label.pack(pady=10)
        self.weight_entry = ctk.CTkEntry(main_frame, placeholder_text="Weight in kg", corner_radius=10, width=300)
        self.weight_entry.pack(pady=10)

        # Height entry with icon
        height_label = ctk.CTkLabel(main_frame, text=" Height", image=self.height_icon, compound="left", text_color="#2c4fd1", font=("Helvetica", 14))
        height_label.pack(pady=10)
        self.height_entry = ctk.CTkEntry(main_frame, placeholder_text="Height in meters", corner_radius=10, width=300)
        self.height_entry.pack(pady=10)

        # Age entry with icon
        age_label = ctk.CTkLabel(main_frame, text=" Age", image=self.age_icon, compound="left", text_color="#2c4fd1", font=("Helvetica", 14))
        age_label.pack(pady=10)
        self.age_entry = ctk.CTkEntry(main_frame, placeholder_text="Age", corner_radius=10, width=300)
        self.age_entry.pack(pady=10)

        # Continue button with arrow
        continue_button = ctk.CTkButton(main_frame, text="Continue", image=self.arrow_image, compound="right", command=self.calculate_bmi, corner_radius=10)
        continue_button.pack(pady=20)

    def go_back(self, event):
        self.destroy()  # Close the window and return to the previous screen

    def select_gender(self, gender):
        self.gender_var.set(gender)
        if gender == "Male":
            self.male_button.configure(fg_color="#a5c6ff")  # Highlight male button
            self.female_button.configure(fg_color="white")  # Reset female button
        else:
            self.female_button.configure(fg_color="#ffb3c6")  # Highlight female button
            self.male_button.configure(fg_color="white")  # Reset male button

    def calculate_bmi(self):
        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())
            gender = self.gender_var.get()
            age = self.age_entry.get()

            if height <= 0:
                raise ValueError("Height must be greater than 0")

            # Calculate BMI
            bmi = weight / (height ** 2)

            # Categorize the BMI result
            if bmi < 18.5:
                category = "Underweight"
            elif 18.5 <= bmi < 25:
                category = "Normal weight"
            elif 25 <= bmi < 30:
                category = "Overweight"
            else:
                category = "Obesity"

            # Save the result to a file along with the email
            with open(DATA_FILE, "a") as file:
                file.write(f"Email: {self.email}, Weight: {weight} kg, Height: {height} m, BMI: {bmi:.2f}, Category: {category}, Gender: {gender}, Age: {age} |\n")

            # Show the result to the user
            messagebox.showinfo("BMI Result", f"Your BMI is {bmi:.2f} ({category})")

            # Open logworkout.py, passing the email
            self.open_logworkout()

        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid input: {e}")

    def open_logworkout(self):
        # Create dictionary with user data
        user_data = {
            'email': self.email,
            'weight': float(self.weight_entry.get()),
            'height': float(self.height_entry.get()),
            'bmi': float(self.weight_entry.get()) / (float(self.height_entry.get()) ** 2),
            'gender': self.gender_var.get(),
            'age': int(self.age_entry.get())
        }
        
        # Open dashboard directly with user data
        dashboard.DashboardApp(user_data)
        self.destroy()

if __name__ == "__main__": 
    if len(sys.argv) > 1 and sys.argv[1]:  # Check if email is provided
        user_email = sys.argv[1]
    else:
        raise ValueError("No email provided. Please register first.")  # Raise an error for clarity

    app = FitnessApp(user_email)
    app.mainloop()
