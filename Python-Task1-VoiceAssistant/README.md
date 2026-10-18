# Voice Assistant

A Python-based voice assistant that listens to spoken commands and responds aloud.

## Features

- Voice input using SpeechRecognition
- Spoken responses using pyttsx3
- Greeting and basic command handling
- Current date and time
- Web searches through the default browser
- Error handling for unclear speech and microphone problems
- Customizable settings in config.json (integration planned)

## Technologies

- Python
- SpeechRecognition
- PyAudio
- pyttsx3
- Google Speech Recognition service
- Web browser integration

## Requirements

- Python 3.10 or newer
- Working microphone
- Internet connection for speech recognition and web searches

## Setup

1. Clone or download this project.
2. Open a terminal in the project folder.
3. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Run the assistant:

   ```bash
   python main.py
   ```

## Example Commands

- "Hello"
- "What is the time?"
- "What is today's date?"
- "Search for artificial intelligence"
- "Goodbye"

## Privacy

Voice commands are sent to Google's online speech recognition service for transcription. Avoid speaking passwords, financial information, or other sensitive data. Web searches open in your default browser.

## Limitations

This is a beginner-friendly project. It currently supports a limited set of commands and requires an internet connection for speech recognition.

## Future Improvements

- Connect customizable commands from config.json
- Add natural-language intent handling
- Add timed reminders
- Add weather information
- Add email functionality

## License

For educational and portfolio use.
