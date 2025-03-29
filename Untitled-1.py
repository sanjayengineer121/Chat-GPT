# import customtkinter as ctk

# class TrainSpeedApp(ctk.CTk):
#     def __init__(self):
#         super().__init__()
#         self.title("Train Speed Calculation")
#         self.geometry("700x500")

#         # Main Frame
#         self.frame = ctk.CTkFrame(self, fg_color="#1E1E1E")
#         self.frame.pack(fill="both", expand=True, padx=20, pady=20)

#         # Step 1: Title
#         title = ctk.CTkLabel(self.frame, text="We can determine the **length of the train** using the formula for speed:", 
#                              font=("Arial", 16, "bold"), text_color="white", justify="left")
#         title.pack(anchor="w", pady=10)

#         # Speed Formula
#         formula = ctk.CTkLabel(self.frame, text="Speed = Distance / Time", 
#                                font=("Arial", 18, "bold"), text_color="#00FF7F")
#         formula.pack(anchor="w", pady=5)

#         # Given Data
#         given_data = ctk.CTkLabel(self.frame, text="• Speed of the train = 60 km/hr\n• Time taken to cross the pole = 9 seconds", 
#                                   font=("Arial", 14), text_color="white", justify="left")
#         given_data.pack(anchor="w", pady=10)

#         # Step 2: Speed Conversion
#         step1 = ctk.CTkLabel(self.frame, text="Step 1: Convert Speed from km/hr to m/s", 
#                              font=("Arial", 15, "bold"), text_color="lightblue")
#         step1.pack(anchor="w", pady=5)

#         conversion = ctk.CTkLabel(self.frame, text="60 × (5/18) = 16.67 m/s", 
#                                   font=("Arial", 14), text_color="white")
#         conversion.pack(anchor="w", pady=5)

#         # Step 3: Use Formula
#         step2 = ctk.CTkLabel(self.frame, text="Step 2: Use the Formula to Find Distance (Train Length)", 
#                              font=("Arial", 15, "bold"), text_color="lightblue")
#         step2.pack(anchor="w", pady=5)

#         distance_calc = ctk.CTkLabel(self.frame, text="Distance = Speed × Time\n16.67 × 9 = 150 metres", 
#                                      font=("Arial", 14), text_color="white")
#         distance_calc.pack(anchor="w", pady=5)

#         # Final Answer Box
#         final_answer = ctk.CTkLabel(self.frame, text="150 metres ✅", 
#                                     font=("Arial", 18, "bold"), text_color="WHITE", fg_color="GREEN", 
#                                     corner_radius=10, padx=20, pady=5)
#         final_answer.pack(pady=10)

# # Run the App
# app = TrainSpeedApp()
# app.mainloop()


# import itertools
# import sys
# import time

# def spinner_loader():
#     spinner = itertools.cycle(["-", "/", "|", "\\"])
#     for _ in range(50):
#         sys.stdout.write(f"\rLoading {next(spinner)}")
#         sys.stdout.flush()
#         time.sleep(0.1)

# spinner_loader()



# from alive_progress import alive_bar
# import time

# def alive_loader():
#     with alive_bar(100, title="Processing") as bar:
#         for _ in range(100):
#             time.sleep(0.05)  # Simulating work
#             bar()  # Update bar

# alive_loader()


# from rich.progress import Progress
# import time

# def rich_loader():
#     with Progress() as progress:
#         task = progress.add_task("[cyan]Loading...", total=100)
#         while not progress.finished:
#             progress.update(task, advance=1)
#             time.sleep(0.05)

# rich_loader()


# from tqdm import tqdm
# import time

# def loading_animation():
#     for _ in tqdm(range(100), desc="Processing", ncols=75, ascii=" █", colour="cyan"):
#         time.sleep(0.05)  # Simulating work

# loading_animation()


import customtkinter as ctk
import itertools
import threading
import time

class LoaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Loader Example")
        self.geometry("400x300")

        self.loader_label = ctk.CTkLabel(self, text="⏳", font=("Arial", 50))
        self.loader_label.pack(pady=20)

        self.start_loader()

    def start_loader(self):
        self.running = True
        self.loader_thread = threading.Thread(target=self.animate_loader, daemon=True)
        self.loader_thread.start()

        # Simulate some work (stop loader after 5 seconds)
        self.after(5000, self.stop_loader)

    def animate_loader(self):
        spinner = itertools.cycle(["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"])
        while self.running:
            self.loader_label.configure(text=next(spinner))
            time.sleep(0.1)  # Adjust speed

    def stop_loader(self):
        self.running = False
        self.loader_label.configure(text="✅ Done")

if __name__ == "__main__":
    app = LoaderApp()
    app.mainloop()
