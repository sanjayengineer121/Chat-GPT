from customtkinter import *
from PIL import Image
import requests
import json
import threading
import itertools
import re
from customtkinter import CTkLabel
import customtkinter as ctk


class App(CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.is_loading = False
        self.loader_label = None
        self.loader_animation = itertools.cycle(["⏳", "🔄", "⌛", "🌀"])  # Animated loader

        # Bottom Frame (Input and Button)
        self.FRAME0 = CTkFrame(master=self, width=850, height=64, fg_color="#1E1E1E")
        self.FRAME0.pack_propagate(False)
        self.FRAME0.pack(side="bottom", fill="x", padx=10, pady=5)

        # Entry Widget
        # self.ENTRY1 = CTkEntry(master=self.FRAME0, placeholder_text="💬 Type a message...", width=700, height=60)
        # self.ENTRY1.pack(side="left", padx=5)


        self.ENTRY1 = CTkTextbox(
            master=self.FRAME0, 
            width=700, 
            height=60, 
            corner_radius=10, 
            wrap="word"
        )
        self.ENTRY1.pack(side="left", padx=5, pady=5, fill="both", expand=True)


        # Button Frame
        self.FRAME8 = CTkFrame(master=self.FRAME0, width=70, height=60, fg_color="#1E1E1E")
        self.FRAME8.pack_propagate(False)
        self.FRAME8.pack(side="right", padx=5)

        # Button with Image
        self.BUTTON9 = CTkButton(
            master=self.FRAME8, text="", height=58, corner_radius=5,
            image=CTkImage(Image.open("Assets/send.png"), size=(50, 50)),
            command=self.send_request
        )
        self.BUTTON9.pack(pady=2)

        # Scrollable Frame for Messages
        # Create a faster and smoother scrollable frame
        self.SCROLLABLEFRAME7 = CTkScrollableFrame(
            master=self, width=800, height=400, fg_color="#121212"
        )
        self.SCROLLABLEFRAME7.pack(pady=10, fill="both", expand=True)

        # Speed up scrolling (increase step size)


    def send_request(self):
        """Handles input, clears the field, and starts the API request."""
        text = self.ENTRY1.get("1.0", "end-1c").strip()  # Get text properly
        if not text:
            return

        self.ENTRY1.delete("1.0", "end")  # ✅ Corrected: Clear input field for CTkTextbox
        self.BUTTON9.configure(state="disabled")
        self.ENTRY1.configure(state="disabled")

        self.show_loader()
        threading.Thread(target=self.fetch_response, args=(text,), daemon=True).start()


    def fetch_response(self, text):
        """Sends request to the API and streams response."""
        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": "Bearer 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",
                    "Content-Type": "application/json",
                },
                data=json.dumps({
                    "model": "deepseek/deepseek-r1-distill-llama-70b:free",
                    "messages": [{"role": "user", "content": text}],
                })
            )
            
            output = response.json()
            if "choices" not in output:
                raise ValueError("❌ API response is missing 'choices' key!")
            
            answer = output["choices"][0]["message"]["content"]
            print(answer)
            self.after(0, lambda: self.start_streaming_text(answer))
        
        except Exception as error:
            error_message = f"❌ Error: {str(error)}"
            self.after(0, lambda: self.start_streaming_text(error_message))
    
    


    def show_loader(self):
        """Displays a proper spinning loader animation."""
        self.is_loading = True
        self.loader_label = CTkLabel(self.SCROLLABLEFRAME7, text="⏳", font=("Arial", 24), text_color="#00FF7F")
        self.loader_label.pack(pady=10)
        self.animate_loader()

    def animate_loader(self):
        """Rotates the loader animation while waiting."""
        if self.is_loading:
            self.loader_label.configure(text=next(self.loader_animation))
            self.after(200, self.animate_loader)  # Updates every 200ms

    def hide_loader(self):
        """Hides the loader once response is received."""
        self.is_loading = False
        if self.loader_label:
            self.loader_label.pack_forget()




    def start_streaming_text(self, answer):
        """Creates separate message boxes for each response and applies formatting."""
        self.hide_loader()
        self.BUTTON9.configure(state="normal")
        self.ENTRY1.configure(state="normal")

        response_frame = ctk.CTkFrame(self.SCROLLABLEFRAME7, fg_color="#1E1E1E", corner_radius=10)
        response_frame.pack(fill="x", padx=5, pady=5, anchor="w")

        formatted_labels = self.format_text(answer, response_frame)

        for label in formatted_labels:
            label.pack(fill="x", expand=True, anchor="w")

        self.SCROLLABLEFRAME7._parent_canvas.update_idletasks()  # Force update
        self.SCROLLABLEFRAME7._parent_canvas.yview_moveto(1.0)   # Instantly scrolls to the bottom






    # def stream_text(self, label, answer, index=0):
    #     """Streams text letter by letter for a typing effect."""
    #     if index < len(answer):
    #         label.configure(text=answer[:index + 1])

    #         # Ensure auto-scroll is smooth
    #         if hasattr(self.SCROLLABLEFRAME7, "_parent_canvas"):
    #             self.SCROLLABLEFRAME7._parent_canvas.yview_moveto(1)

    #         self.after(10, lambda: self.stream_text(label, answer, index + 1))  # Adjust speed


    def format_text(self, text, parent_frame):
        """Formats text using CTkLabels with different styles based on markdown-like syntax."""
        
        labels = []  # List to store label elements

        for line in text.split("\n"):
            if line.startswith("###"):  # Green bold for headings
                formatted_label = ctk.CTkLabel(
                    parent_frame, text=line.replace("###", "").strip(),
                    font=("Arial", 18, "bold"), text_color="#00FF00"  # Green
                )
            
            elif "**" in line:  # Red bold for **bold**
                bold_text = re.sub(r"\*\*(.*?)\*\*", r"\1", line)
                formatted_label = ctk.CTkLabel(
                    parent_frame, text=bold_text.strip(),
                    font=("Arial", 16, "bold"), text_color="#FF0000"  # Red
                )

            elif "*" in line:  # Red normal for *italic*
                italic_text = re.sub(r"\*(.*?)\*", r"\1", line)
                formatted_label = ctk.CTkLabel(
                    parent_frame, text=italic_text.strip(),
                    font=("Arial", 16, "italic"), text_color="#FF0000"  # Red
                )

            else:  # Normal text (default style)
                formatted_label = ctk.CTkLabel(
                    parent_frame, text=line.strip(),
                    font=("Arial", 16), text_color="#FFFFFF"  # White
                )

            labels.append(formatted_label)

        return labels  # Return list of CTkLabel elemen

    

# App Configuration
root = App()
root.geometry("950x550")
root.title("💬 AI Chatbot")
root.configure(fg_color="#000000")
root.mainloop()
