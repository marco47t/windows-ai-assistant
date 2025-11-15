"""Voice service for Windows AI Assistant."""

import speech_recognition as sr
import pyttsx3
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

class VoiceService:
    """Main voice service class."""
    
    def __init__(self):
        """Initialize the voice service."""
        print("🎤 Initializing Voice Service...")
        
        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Initialize text-to-speech
        self.tts_engine = pyttsx3.init()
        self._configure_tts()
        
        print("✅ Voice Service initialized successfully")
    
    def _configure_tts(self):
        """Configure text-to-speech settings."""
        # Set properties
        self.tts_engine.setProperty('rate', 150)  # Speed
        self.tts_engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
        
        # Get available voices
        voices = self.tts_engine.getProperty('voices')
        # Use first available voice (can be configured later)
        if voices:
            self.tts_engine.setProperty('voice', voices[0].id)
    
    def listen(self, timeout=5, phrase_time_limit=10):
        """Listen for speech input."""
        try:
            with self.microphone as source:
                print("🎧 Listening...")
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                # Listen for audio
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
                
                print("🔄 Processing speech...")
                # Recognize speech using Google Speech Recognition
                text = self.recognizer.recognize_google(audio)
                print(f"📝 Recognized: {text}")
                return text
                
        except sr.WaitTimeoutError:
            print("⏱️ Listening timed out")
            return None
        except sr.UnknownValueError:
            print("❓ Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"❌ Could not request results; {e}")
            return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def speak(self, text: str):
        """Convert text to speech."""
        try:
            print(f"🔊 Speaking: {text}")
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"❌ Error speaking: {e}")
    
    def test_voice_service(self):
        """Test the voice service."""
        print("\n🧪 Testing Voice Service...\n")
        
        # Test TTS
        self.speak("Hello! Voice service is working correctly.")
        
        # Test speech recognition
        print("\nPlease say something...")
        text = self.listen()
        
        if text:
            self.speak(f"You said: {text}")
            print("\n✅ Voice service test completed successfully")
        else:
            print("\n⚠️ Speech recognition test failed")

def main():
    """Main function."""
    print("""
    ╔════════════════════════════════════════╗
    ║  Windows AI Assistant - Voice Service ║
    ║              Version 1.0.0             ║
    ╚════════════════════════════════════════╝
    """)
    
    # Initialize voice service
    voice_service = VoiceService()
    
    # Run test
    voice_service.test_voice_service()
    
    print("\n🎤 Voice service is ready!")
    print("Press Ctrl+C to exit\n")
    
    # Keep running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Voice service stopped")

if __name__ == "__main__":
    main()