import openai
import speech_recognition as sr
import os
from dotenv import load_dotenv
import subprocess
import requests
from datetime import datetime
import cv2
import threading

class Jarvis:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Setup OpenAI
        self.openai_key = os.getenv('OPENAI_API_KEY')
        if not self.openai_key:
            raise ValueError("OpenAI API key not found in .env file")
        openai.api_key = self.openai_key
        
        # Setup ElevenLabs
        self.eleven_key = os.getenv('ELEVENLABS_API_KEY')
        self.voice_id = os.getenv('ELEVENLABS_VOICE_ID')
        self.use_eleven = self.eleven_key is not None and self.voice_id is not None
        
        if not self.use_eleven:
            print("No ElevenLabs API key or Voice ID found. Using system voice instead.")
        
        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Adjust microphone for ambient noise
        print("Calibrating microphone for ambient noise... Please wait.")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
        print("Microphone calibrated.")

    def listen(self):
        """Listen for user input through microphone"""
        with self.microphone as source:
            print("\nListening...")
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                print("Processing speech...")
                text = self.recognizer.recognize_google(audio)
                print(f"You said: {text}")
                return text
            except sr.WaitTimeoutError:
                self.speak("No speech detected, please try again.")
                return None
            except sr.UnknownValueError:
                self.speak("I couldn't understand that, could you please repeat?")
                return None
            except sr.RequestError as e:
                self.speak("There seems to be an issue with the speech recognition service.")
                return None

    def process_query(self, text):
        """Process query using GPT-4o or handle special queries directly"""
        try:
            # Check if the query is asking for the time
            if "time" in text.lower():
                current_time = datetime.now().strftime("%H:%M %p")
                return f"The current time is {current_time}."
            
            # Handle query related to camera
            if "see me" in text.lower() or "camera" in text.lower():
                camera_thread = threading.Thread(target=self.see_through_camera)
                camera_thread.start()
                return "Activating the camera feed now. Please look at the screen."

            # Otherwise, process the query using GPT-4o
            response = openai.ChatCompletion.create(
                model="gpt-4o",  # Updated to use GPT-4o model
                messages=[
                    {"role": "system", "content": "You are JARVIS, a highly sophisticated AI assistant similar to the one from Iron Man. Be professional, precise, and occasionally witty. Keep responses concise yet informative."},
                    {"role": "user", "content": text}
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            return response.choices[0].message["content"]

        except Exception as e:
            print(f"Error in processing: {e}")
            return "I apologize, but I encountered an error processing your request."

    def see_through_camera(self):
        """Access the MacBook's camera, display the feed, and interact verbally"""
        try:
            self.speak("Activating the camera feed. Please wait.")
            
            # Try initializing camera with a different backend to improve compatibility
            cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)  # Use AVFoundation backend for macOS
            
            if not cap.isOpened():
                self.speak("I'm unable to access the camera, please make sure it is not being used by another application.")
                return

            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

            while True:
                ret, frame = cap.read()
                if not ret:
                    self.speak("Unable to retrieve video feed. Please check the camera.")
                    break

                # Convert to grayscale for face detection
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

                # Draw rectangles around detected faces
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

                # Speak if a face is detected
                if len(faces) > 0:
                    self.speak("I see you. How can I assist you further?")
                
                # Display the frame
                cv2.putText(frame, "Press 'q' to exit.", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.imshow('Jarvis Camera Feed', frame)

                # Exit camera feed if 'q' is pressed
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            cap.release()
            cv2.destroyAllWindows()
            self.speak("Camera feed closed.")
        except cv2.error as e:
            # Handle specific OpenCV exceptions
            print(f"OpenCV error: {e}")
            self.speak("I encountered an issue while trying to access the camera.")
        except Exception as e:
            print(f"Camera access error: {e}")
            self.speak("I encountered an unexpected issue while trying to access the camera.")

    def generate_speech(self, text):
        """Convert text to speech using ElevenLabs API"""
        try:
            if self.use_eleven:
                url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}/stream"
                
                headers = {
                    "Accept": "audio/mpeg",
                    "xi-api-key": self.eleven_key
                }

                data = {
                    "text": text,
                    "model_id": "eleven_monolingual_v1",
                    "voice_settings": {
                        "stability": 0.5,
                        "similarity_boost": 0.8
                    }
                }

                response = requests.post(url, headers=headers, json=data, stream=True)

                if response.status_code == 200:
                    with open("output.mp3", "wb") as f:
                        for chunk in response.iter_content(chunk_size=1024):
                            if chunk:
                                f.write(chunk)
                    subprocess.run(["afplay", "output.mp3"])  # On macOS, use afplay to play the audio file
                else:
                    print(f"Error: {response.status_code} - {response.text}")
                    self.speak("I encountered an issue generating the audio.")
            else:
                subprocess.run(['say', '-v', 'Daniel', '-r', '190', text])
        except Exception as e:
            print(f"Speech generation error: {e}")

    def speak(self, text):
        """Fallback for speech synthesis if ElevenLabs is not available"""
        self.generate_speech(text)

    def run(self):
        welcome = "JARVIS online. At your service. You may speak now."
        print("\nJARVIS:", welcome)
        self.speak(welcome)
        
        while True:
            try:
                # Get voice input
                user_input = self.listen()
                
                if not user_input:
                    continue
                
                # Check for exit commands
                if any(word in user_input.lower() for word in ['exit', 'quit', 'goodbye', 'bye']):
                    farewell = "Shutting down systems. It's been a pleasure assisting you."
                    print("JARVIS:", farewell)
                    self.speak(farewell)
                    break
                
                # Process query and speak response
                response = self.process_query(user_input)
                print("JARVIS:", response)
                self.speak(response)
                
            except KeyboardInterrupt:
                print("\nEmergency shutdown initiated...")
                self.speak("Emergency shutdown protocol engaged. Goodbye.")
                break
            except Exception as e:
                print(f"Error: {e}")
                self.speak("I apologize, but I encountered an unexpected error.")

if __name__ == "__main__":
    print("Initializing JARVIS AI System...")
    try:
        assistant = Jarvis()
        assistant.run()
    except Exception as e:
        print(f"Startup Error: {e}")
        print("Please ensure your .env file contains valid API keys and your microphone is working.")

