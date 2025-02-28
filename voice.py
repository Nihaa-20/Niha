import openai
import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Set OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty("rate", 150)  # Adjust speed

# Initialize Speech Recognition
recognizer = sr.Recognizer()

def speak(text):
    """Convert text to speech"""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Capture voice input"""
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"User said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand that."
        except sr.RequestError:
            return "Error connecting to voice recognition service."

def process_command(command):
    """Process user commands"""
    if "open google" in command:
        webbrowser.open("https://www.google.com")
        return "Opening Google."
    elif "time" in command:
        now = datetime.datetime.now().strftime("%H:%M:%S")
        return f"The time is {now}."
    else:
        return ai_response(command)

def ai_response(text):
    """Generate response using OpenAI"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": text}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/voice-command", methods=["POST"])
def voice_command():
    """API endpoint to process voice commands"""
    data = request.json
    command = data.get("command", "")
    response = process_command(command)
    speak(response)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(ssl_context=('cert.pem', 'key.pem'), port=5000)  # HTTPS enabled
