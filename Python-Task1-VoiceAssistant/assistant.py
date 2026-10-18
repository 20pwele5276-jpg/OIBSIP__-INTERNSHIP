import datetime
import urllib.parse
import webbrowser

import pyttsx3
import speech_recognition as sr


class VoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.speaker = pyttsx3.init()
        self.speaker.setProperty("rate", 175)

    def speak(self, message):
        print(f"Assistant: {message}")
        self.speaker.say(message)
        self.speaker.runAndWait()

    def listen(self):
        try:
            with sr.Microphone() as source:
                print("\nListening... Speak now.")
                self.recognizer.adjust_for_ambient_noise(
                    source, duration=0.5
                )
                audio = self.recognizer.listen(
                    source, timeout=5, phrase_time_limit=8
                )

            text = self.recognizer.recognize_google(audio)
            print(f"You: {text}")
            return text.lower().strip()

        except sr.WaitTimeoutError:
            self.speak("I did not hear anything. Please try again.")
        except sr.UnknownValueError:
            self.speak("Sorry, I could not understand. Please repeat.")
        except sr.RequestError:
            self.speak("Speech recognition is unavailable. Check your internet.")
        except OSError:
            self.speak("I cannot access your microphone. Check its connection.")

        return ""

    def handle_command(self, command):
        if not command:
            return True

        if any(word in command for word in ["exit", "quit", "goodbye", "stop"]):
            self.speak("Goodbye! Have a nice day.")
            return False

        if "hello" in command or "hi" == command:
            self.speak("Hello! How can I help you today?")

        elif "time" in command:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            self.speak(f"The current time is {current_time}.")

        elif "date" in command or "today" in command:
            current_date = datetime.datetime.now().strftime("%A, %d %B %Y")
            self.speak(f"Today is {current_date}.")

        elif command.startswith("search for "):
            topic = command.removeprefix("search for ").strip()
            if topic:
                url = "https://www.google.com/search?q=" + urllib.parse.quote(topic)
                webbrowser.open(url)
                self.speak(f"Searching the web for {topic}.")

        elif command.startswith("search "):
            topic = command.removeprefix("search ").strip()
            if topic:
                url = "https://www.google.com/search?q=" + urllib.parse.quote(topic)
                webbrowser.open(url)
                self.speak(f"Searching the web for {topic}.")

        else:
            self.speak(
                "I do not know that command yet. "
                "You can ask for the time, date, or a web search."
            )

        return True

    def run(self):
        self.speak("Voice Assistant is ready. Say hello to begin.")
        running = True

        while running:
            command = self.listen()
            if command:
                running = self.handle_command(command)


if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.run()
