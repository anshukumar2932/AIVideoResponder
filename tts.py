import pyttsx3

def init_engine():
    engine = pyttsx3.init()
    
    # Adjust speed (lower = deeper feel)
    engine.setProperty('rate', 135)
    engine.setProperty('volume', 1.0)
    
    return engine

engine = init_engine()

def speak(text: str):
    if not text or text.strip() == "":
        print("Empty text. Nothing to speak.")
        return
    
    print("Bot speaking...")
    engine.say(text)
    engine.runAndWait()


# Allow standalone testing
if __name__ == "__main__":
    user_input = input("Enter text to speak: ")
    speak(user_input)