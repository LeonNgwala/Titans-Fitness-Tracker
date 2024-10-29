import customtkinter as ctk
from PIL import Image, ImageTk
import os
import random

def create_workout_app():
    # Initialize the application
    app = ctk.CTk()
    
   
    # Set a background color
    inspiring_color = "#D3D3D3"
    
    # Function to exit fullscreen mode
    def exit_fullscreen(event=None):
        app.attributes("-fullscreen", False)
    
    # Bind the escape key to exit fullscreen
    app.bind("<Escape>", exit_fullscreen)
    
    # Configure the grid for the application
    app.grid_rowconfigure(0, weight=1)
    app.grid_rowconfigure(1, weight=8)
    app.grid_columnconfigure(0, weight=1)
    app.grid_columnconfigure(1, weight=3)
    
    # Header section
    header_frame = ctk.CTkFrame(app, height=100, fg_color=inspiring_color)
    header_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

    header_label = ctk.CTkLabel(header_frame, text="Workout Lessons", font=ctk.CTkFont(size=30, weight="bold"), text_color="black")
    header_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")

    # Sidebar for exercise list
    sidebar_frame = ctk.CTkFrame(app, width=350, fg_color=inspiring_color)
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
    exercise_list_label = ctk.CTkLabel(scrollable_frame, text="Exercises", font=ctk.CTkFont(size=22, weight="bold"), text_color="black")
    exercise_list_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    # Image directory
    image_directory = r"F:\Recent Fitness App\New fitness App"

    # List of exercises
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

        ("Bent Over Rowing", "Bent over rowing.jpg", 
         "1. Stand with feet shoulder-width apart, bend at your hips, and pull the weight toward your body.\n"
         "2. Keep your back straight and core tight.\n"
         "3. Lower the weights back down with control."),

        ("Donkey Kicks", "Donkey Kicks,.png", 
         "1. Start on all fours and kick one leg back, keeping the knee bent.\n"
         "2. Squeeze your glute at the top of the movement.\n"
         "3. Alternate legs for a balanced workout."),

        ("Overhead Press", "Overhead press.jpg", 
         "1. Stand with feet shoulder-width apart and press the barbell overhead.\n"
         "2. Keep your core tight and avoid arching your back.\n"
         "3. Lower the barbell back to shoulder level."),

        ("Reverse Lunge", "Reverse Lunge.jpg", 
         "1. Step one leg back into a lunge position while keeping your chest upright.\n"
         "2. Push through your front heel to return to standing.\n"
         "3. Alternate legs to work both sides."),

        ("Leg Press", "leg press.jpg", 
         "1. Sit on the machine and press the platform upwards using your legs.\n"
         "2. Keep your knees aligned with your toes.\n"
         "3. Slowly return to the starting position."),

        ("EZ bar biceps curl", "EZ bar biceps curl.jpg", 
         "1. Stand with feet shoulder-width apart, holding the EZ bar with an underhand grip.\n"
         "2. Curl the bar toward your shoulders while keeping your elbows close to your sides.\n"
         "3. Lower the bar back down in a controlled manner, fully extending your arms."),
        
       ("Wall Sit", "wall-sit.jpg", 
         "1. Stand with your back against a wall and slide down until your thighs are parallel to the ground.\n"
         "2. Keep your back straight and shoulders relaxed against the wall.\n"
         "3. Hold the position for as long as possible, engaging your core and keeping your knees behind your toes."),
       
        ("Mountain Climbers", "Mountain Climber.jpg", 
         "1. Start in a high plank position with your hands directly under your shoulders.\n"
         "2. Engage your core and quickly drive one knee toward your chest.\n"
         "3. Alternate legs rapidly, as if you're running in place, while keeping your hips level."),
        
        ("Tuck Jump", "Tuck Jump.jpg", 
         "1. Stand with your feet shoulder-width apart and lower into a slight squat.\n"
         "2. Jump up explosively, bringing your knees toward your chest as you leap.\n"
         "3. Land softly with your knees slightly bent and immediately go into the next jump."),
        
        ("Pull-Ups", "Pull Ups.jpg", 
         "1. Hang from a pull-up bar with your palms facing away and hands shoulder-width apart.\n"
         "2. Engage your core and pull your body up until your chin is above the bar.\n"
         "3. Lower yourself back down in a controlled manner to the starting position."),
        
        ("Squats", "Squat 1.jpg",
         "1. Stand with your feet shoulder-width apart and your toes slightly turned out.\n"
         "2. Lower your body by bending your knees and pushing your hips back, keeping your chest up.\n"
         "3. Go as low as you can while keeping your heels on the ground, then push through your heels to return to standing.")
    ]

    # Main content frame for exercise details
    main_content_frame = ctk.CTkFrame(app, fg_color=inspiring_color)
    main_content_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

    # Global variable for quote_label
    quote_label = None

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
        app.after(5000, update_quote)

    # Function to display exercise details
    def display_exercise(exercise_name, image_file, instructions):
        for widget in main_content_frame.winfo_children():
            widget.destroy()

        try:
            image_path = os.path.join(image_directory, image_file)
            if not os.path.exists(image_path):
                print(f"Exercise image not found: {image_path}")
                return
            
            img = Image.open(image_path)
            img = img.resize((400, 300), Image.LANCZOS)
            img = ImageTk.PhotoImage(img)

            image_label = ctk.CTkLabel(main_content_frame, image=img, text="")
            image_label.image = img
            image_label.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

            instructions_label = ctk.CTkLabel(main_content_frame, text=f"{exercise_name}\n\n{instructions}", font=ctk.CTkFont(size=18), justify="left")
            instructions_label.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")

            # Back icon path and button
            back_icon_path = os.path.join(image_directory, "back-icon.png")  # Change to your icon filename
            back_icon = Image.open(back_icon_path)
            back_icon = back_icon.resize((30, 30), Image.LANCZOS)
            back_icon = ImageTk.PhotoImage(back_icon)

            back_button = ctk.CTkButton(main_content_frame, image=back_icon, text=" Back", command=load_exercises)
            back_button.image = back_icon  # Keep a reference to avoid garbage collection
            back_button.grid(row=3, column=0, padx=20, pady=20, sticky="e")

        except Exception as e:
            print(f"Error loading image {image_file}: {e}")

    # Load exercises dynamically
    def load_exercises():
        global quote_label  # Access the global variable

        for widget in main_content_frame.winfo_children():
            widget.destroy()

        # Recreate the quote label
        quote_label = ctk.CTkLabel(main_content_frame, text="", font=ctk.CTkFont(size=24, weight="bold"), text_color="black")
        quote_label.grid(row=0, column=0, pady=20, sticky="n")  # Center the quote vertically at the top

        # Center quote horizontally
        main_content_frame.grid_columnconfigure(0, weight=1)  # Make the column expand

        update_quote()  # Start updating quotes

        for index, (exercise, image_file, instructions) in enumerate(exercises):
            try:
                image_path = os.path.join(image_directory, image_file)
                if not os.path.exists(image_path):
                    print(f"Exercise image not found: {image_path}")
                    continue

                img = Image.open(image_path)
                img = img.resize((200, 200), Image.LANCZOS)
                img = ImageTk.PhotoImage(img)

                label = ctk.CTkLabel(scrollable_frame, image=img, text=exercise, compound="left", padx=10, pady=5)
                label.image = img
                label.grid(row=index + 1, column=0, padx=10, pady=5, sticky="w")

                label.bind("<Button-1>", lambda e, ex=exercise, img=image_file, ins=instructions: display_exercise(ex, img, ins))

            except Exception as e:
                print(f"Error loading image {image_file}: {e}")

    # Load exercises on startup
    load_exercises()

    return app

if __name__ == "__main__":
    app = create_workout_app()
    app.mainloop()

