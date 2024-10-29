import customtkinter as ctk
from PIL import Image, ImageTk
import subprocess
import random
import logging

class SplashScreen:
    def __init__(self, duration=3000, config=None):
        self.duration = duration
        self.config = config or self.load_default_config()
        self.setup_logging()
        self.splash = ctk.CTk()
        self.splash.geometry(f"{self.splash.winfo_screenwidth()}x{self.splash.winfo_screenheight()}")
        self.splash.title("Welcome to Titans Fitness Club")
        self.splash.attributes('-fullscreen', True)
        self.splash.configure(fg_color="white")

        # Load and resize logo image
        self.load_logo()

        # Center frame for content
        center_frame = ctk.CTkFrame(self.splash, fg_color="transparent")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Display the logo
        if self.logo_photo:
            self.logo_label = ctk.CTkLabel(center_frame, image=self.logo_photo, text="")
            self.logo_label.pack(pady=(0, 20))

        # Overlay text
        self.overlay_label = ctk.CTkLabel(center_frame, text="Titans Fitness", font=("Helvetica", 40, "bold"), text_color="black")
        self.overlay_label.pack(pady=(0, 20))

        # Fitness message label
        self.message_label = ctk.CTkLabel(center_frame, text="", font=("Helvetica", 16), text_color="black")
        self.message_label.pack(pady=(0, 20))

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(center_frame, width=300, fg_color="white", progress_color="black")
        self.progress_bar.pack(pady=(0, 20))
        self.progress_bar.set(0)

        # Version label
        version_label = ctk.CTkLabel(self.splash, text="Version 1.0", font=("Helvetica", 12), text_color="black")
        version_label.place(relx=0.95, rely=0.98, anchor="se")

        # Start loading animation
        self.load_animation()

    def setup_logging(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def load_default_config(self):
        return {
            "logo_path": "icons/logo.jpg",
            "messages": [
                "Stay fit, stay healthy!",
                "Push your limits!",
                # ... more messages ...
            ],
            "version": "1.0"
        }

    def load_logo(self):
        try:
            logo_image = Image.open(self.config["logo_path"])
            max_size = (600, 400)  # Maximum size for the logo
            logo_image.thumbnail(max_size, Image.LANCZOS)  # Resize while maintaining aspect ratio
            self.logo_photo = ctk.CTkImage(light_image=logo_image, dark_image=logo_image)
        except FileNotFoundError:
            logging.error("Logo image not found. Using text instead.")
            self.logo_photo = None

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
            self.message_label.configure(text=random.choice(fitness_messages))  # Update message using configure
            self.splash.after(int(self.duration / 100), self.load_animation, step + 1)
        else:
            self.close()

    def close(self):
        self.splash.destroy()
        try:
            import Login  # Directly import the Login screen
            Login.main()  # Call the main function in the Login.py script
        except ModuleNotFoundError:
            logging.error("Login.py not found. Please check the file name and path.")

    def run(self):
        self.splash.mainloop()

if __name__ == "__main__":
    splash_screen = SplashScreen(duration=3000)  # Changed from 9000 to 3000
    splash_screen.run()
