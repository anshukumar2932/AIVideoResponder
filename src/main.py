from src.stt import get_user_input
from src.predict_intent import predict_intent
from src.response_generator import generate_response
from src.tts import speak


def main():
    print("\n===== KHAPEETAR AI Assistant Started =====\n")

    while True:
        print("\nListening...\n")

        user_text = get_user_input()

        if not user_text.strip():
            print("No speech detected. Try again.")
            continue

        print(f"\nUser said: {user_text}")

        # Exit condition
        if user_text.lower() in ["exit", "quit", "stop", "bye"]:
            print("Shutting down assistant...")
            speak("Goodbye. Have a great day.")
            break

        # Predict intent
        intent = predict_intent(user_text)
        print(f"Predicted Intent: {intent}")

        # Generate response
        response = generate_response(intent)
        print(f"Bot: {response}")

        # Speak response
        speak(response)


if __name__ == "__main__":
    main()