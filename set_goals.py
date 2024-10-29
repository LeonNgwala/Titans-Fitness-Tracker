import customtkinter as ctk
from PIL import Image
import subprocess
import sys
import measurements
import welcome

class FitnessTrackerApp(ctk.CTk):
    def __init__(self, email):
        super().__init__()

        self.email = email  
        self.selected_fitness_goal = None  
        self.selected_focus_areas = []  
        self.checkboxes = {}

        self.title("Goal Setting and Focus")
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")

        # Create the main frame
        self.main_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="white")  
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.create_main_menu()

    def create_main_menu(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        self.main_frame.configure(fg_color="white")

        back_image = Image.open("img/icons-back.png").resize((30, 30), Image.LANCZOS)
        self.back_icon = ctk.CTkImage(back_image, size=(30, 30))
        back_button = ctk.CTkButton(self.main_frame, image=self.back_icon, text="", command=self.go_to_welcome, width=40)
        back_button.pack(side="top", anchor="nw", padx=10, pady=(10, 0))

        self.label = ctk.CTkLabel(self.main_frame, text="Select Your Fitness Goal", font=("Arial", 30), fg_color="white")
        self.label.pack(pady=40)

        self.weight_loss_button = ctk.CTkButton(self.main_frame, text="Weight Loss", font=("Arial", 28), command=lambda: self.show_focus_areas("Weight Loss"))
        self.weight_loss_button.pack(pady=10)

        self.muscle_gain_button = ctk.CTkButton(self.main_frame, text="Muscle Gain", font=("Arial", 28), command=lambda: self.show_focus_areas("Muscle Gain"))
        self.muscle_gain_button.pack(pady=10)

        self.body_shape_button = ctk.CTkButton(self.main_frame, text="Body Shape", font=("Arial", 28), command=lambda: self.show_focus_areas("Body Shape"))
        self.body_shape_button.pack(pady=10)

        self.cardio_button = ctk.CTkButton(self.main_frame, text="Cardio", font=("Arial", 28), command=lambda: self.show_focus_areas("Cardio"))
        self.cardio_button.pack(pady=10)

    def show_focus_areas(self, goal):
        self.selected_fitness_goal = goal  

        for widget in self.main_frame.winfo_children():
            widget.destroy()

        self.main_frame.configure(fg_color="white")

        back_image = Image.open("img/icons-back.png").resize((30, 30), Image.LANCZOS)
        self.back_icon = ctk.CTkImage(back_image, size=(30, 30))
        back_button = ctk.CTkButton(self.main_frame, image=self.back_icon, text="", command=self.create_main_menu, width=40)
        back_button.pack(side="top", anchor="nw", padx=10, pady=(10, 0))

        self.label = ctk.CTkLabel(self.main_frame, text=f"Select Focus Areas for {goal}", font=("Arial", 30), fg_color="white")
        self.label.pack(pady=40)

        focus_areas = ['Legs', 'Back', 'Shoulders', 'Arms', 'Abs', 'Butt', 'Chest', 'Full Body']
        for area in focus_areas:
            var = ctk.BooleanVar()  
            checkbox = ctk.CTkCheckBox(self.main_frame, text=area, font=("Arial", 25), variable=var, command=lambda a=area, v=var: self.update_selection(a, v))
            checkbox.pack(pady=10)
            self.checkboxes[area] = var  

        continue_button = ctk.CTkButton(self.main_frame, text="Continue", font=("Arial", 25), command=self.continue_to_next_page)
        continue_button.pack(pady=30)

    def update_selection(self, area, var):
        if var.get():
            self.selected_focus_areas.append(area)  
        else:
            self.selected_focus_areas.remove(area)  

    def continue_to_next_page(self):
        if self.selected_focus_areas:
            with open("FitnessTrackerData.txt", "a") as file:
                file.write(f"Email: {self.email}, Fitness Goal: {self.selected_fitness_goal}, Focus Areas: {', '.join(self.selected_focus_areas)}\n")
            
            # Replace subprocess with direct module import
            measurements_app = measurements.MeasurementsApp(
                email=self.email,
                fitness_goal=self.selected_fitness_goal,
                focus_areas=self.selected_focus_areas
            )
            self.destroy()
            measurements_app.mainloop()
        else:
            print("No focus areas selected.")

    def go_to_welcome(self):
        # Replace subprocess with direct module import
        welcome_app = welcome.WelcomeApp()
        self.destroy()
        welcome_app.mainloop()

if __name__ == "__main__":
    user_email = sys.argv[1] if len(sys.argv) > 1 else None  # Handle missing email
    app = FitnessTrackerApp(email=user_email)
    app.mainloop()
