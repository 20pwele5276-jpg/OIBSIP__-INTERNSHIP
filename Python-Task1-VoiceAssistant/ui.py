import customtkinter as ctk
import threading
import datetime
import urllib.parse
import webbrowser
from assistant import VoiceAssistant


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class NovaUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Nova | AI Voice Assistant")
        self.geometry("850x650")
        self.minsize(700, 550)
        self.configure(fg_color="#0B1020")

        self.assistant = VoiceAssistant()
        self.listening = False

        # Header
        header = ctk.CTkFrame(self, fg_color="#141B30", corner_radius=18)
        header.pack(fill="x", padx=20, pady=(20, 12))

        ctk.CTkLabel(
            header, text="NOVA", font=("Segoe UI", 28, "bold"),
            text_color="#53E0FF"
        ).pack(anchor="w", padx=22, pady=(16, 0))

        ctk.CTkLabel(
            header, text="YOUR PERSONAL VOICE ASSISTANT",
            font=("Segoe UI", 11), text_color="#A8B4D0"
        ).pack(anchor="w", padx=24, pady=(0, 16))

        # Status
        self.status = ctk.CTkLabel(
            self, text="●  Ready to assist",
            text_color="#55E6A5", font=("Segoe UI", 13)
        )
        self.status.pack(anchor="w", padx=25, pady=(5, 8))

        # Conversation area
        self.chat = ctk.CTkTextbox(
            self, corner_radius=15, fg_color="#11182A",
            text_color="#E7EEFF", font=("Segoe UI", 14),
            wrap="word"
        )
        self.chat.pack(fill="both", expand=True, padx=20, pady=8)
        self.chat.insert("end", "NOVA: Hello! I'm ready. Choose a command below.\n\n")
        self.chat.configure(state="disabled")

        # Quick actions
        actions = ctk.CTkFrame(self, fg_color="transparent")
        actions.pack(fill="x", padx=20, pady=8)

        for label, command in [
            ("🕒 Time", self.show_time),
            ("📅 Date", self.show_date),
            ("🌐 Search", self.search_web),
        ]:
            ctk.CTkButton(
                actions, text=label, command=command,
                fg_color="#202B45", hover_color="#35466B",
                height=38, corner_radius=10
            ).pack(side="left", expand=True, fill="x", padx=5)

        # Microphone and stop controls
        controls = ctk.CTkFrame(self, fg_color="transparent")
        controls.pack(fill="x", padx=20, pady=(8, 20))

        self.mic_button = ctk.CTkButton(
            controls, text="🎙  Start Listening",
            command=self.start_listening,
            fg_color="#087FAD", hover_color="#09658A",
            height=48, corner_radius=12,
            font=("Segoe UI", 14, "bold")
        )
        self.mic_button.pack(side="left", expand=True, fill="x", padx=(0, 8))

        ctk.CTkButton(
            controls, text="Exit",
            command=self.destroy,
            fg_color="#702D49", hover_color="#8D3458",
            height=48, corner_radius=12, width=100
        ).pack(side="right")

    def add_message(self, speaker, message):
        self.chat.configure(state="normal")
        self.chat.insert("end", f"{speaker}: {message}\n\n")
        self.chat.see("end")
        self.chat.configure(state="disabled")

    def speak_response(self, message):
        self.add_message("NOVA", message)
        threading.Thread(
            target=self.assistant.speak,
            args=(message,),
            daemon=True
        ).start()

    def show_time(self):
        now = datetime.datetime.now().strftime("%I:%M %p")
        self.speak_response(f"The current time is {now}.")

    def show_date(self):
        today = datetime.datetime.now().strftime("%A, %d %B %Y")
        self.speak_response(f"Today is {today}.")

    def search_web(self):
        dialog = ctk.CTkInputDialog(
            text="What would you like to search for?",
            title="Web Search"
        )
        topic = dialog.get_input()

        if topic and topic.strip():
            topic = topic.strip()
            webbrowser.open(
                "https://www.google.com/search?q="
                + urllib.parse.quote(topic)
            )
            self.speak_response(f"Searching the web for {topic}.")

    def start_listening(self):
        if self.listening:
            return

        self.listening = True
        self.mic_button.configure(state="disabled", text="Listening...")
        self.status.configure(text="●  Listening for a command", text_color="#53E0FF")
        threading.Thread(target=self.listen_once, daemon=True).start()

    def listen_once(self):
        try:
            command = self.assistant.listen()

            if command:
                self.after(0, self.add_message, "YOU", command)
                self.after(0, self.process_command, command)
            else:
                self.after(
                    0, self.add_message, "NOVA",
                    "I couldn't understand. Please try again."
                )
        finally:
            self.after(0, self.finish_listening)

    def process_command(self, command):
        if any(word in command for word in ["exit", "quit", "goodbye", "stop"]):
            self.speak_response("Goodbye! Have a nice day.")
            self.after(1200, self.destroy)
            return

        if "hello" in command or command == "hi":
            response = "Hello! How can I help you today?"
        elif "time" in command:
            response = f"The current time is {datetime.datetime.now():%I:%M %p}."
        elif "date" in command or "today" in command:
            response = f"Today is {datetime.datetime.now():%A, %d %B %Y}."
        elif command.startswith("search for ") or command.startswith("search "):
            topic = command.removeprefix("search for ").removeprefix("search ").strip()
            if topic:
                webbrowser.open(
                    "https://www.google.com/search?q="
                    + urllib.parse.quote(topic)
                )
                response = f"Searching the web for {topic}."
            else:
                response = "Please say what you want to search for."
        else:
            response = "I don't know that command yet. Try hello, time, date, or search."

        self.speak_response(response)

    def finish_listening(self):
        self.listening = False
        if self.winfo_exists():
            self.mic_button.configure(state="normal", text="🎙  Start Listening")
            self.status.configure(text="●  Ready to assist", text_color="#55E6A5")


if __name__ == "__main__":
    app = NovaUI()
    app.mainloop()