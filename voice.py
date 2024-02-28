import pyttsx3

class SpeakEngine:

    def initiate_engine(self):
        # Initialize the text-to-speech engine
        engine = pyttsx3.init()

        # Set properties for female voice
        voices = engine.getProperty('voices')
        female_voice = [v for v in voices if "female" in v.name.lower()]
        if female_voice:
            engine.setProperty('voice', female_voice[0].id)

        # Set the voice rate (optional)
        rate = engine.getProperty('rate')
        engine.setProperty('rate', rate - 50)  # Slow down the voice slightly

        # Set the voice volume (optional)
        volume = engine.getProperty('volume')
        engine.setProperty('volume', volume + 0.5)  # Increase volume slightly
        
        return engine

    def speak(self, engine, text="Hello, world! This is another example of text-to-speech in Python."):
        # Text to be spoken
        text = text

        # Convert text to speech
        engine.say(text)

        # Play the speech
        engine.runAndWait()

        print("Speech completed.")


if __name__ == "__main__":
    speak_engine = SpeakEngine()
    engine = speak_engine.initiate_engine()
    engine.speak(engine, "Hellooo")
