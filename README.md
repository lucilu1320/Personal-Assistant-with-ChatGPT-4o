# JARVIS Virtual Assistant

A Python-based virtual assistant inspired by Iron Man's JARVIS. This assistant listens to voice commands, processes natural language queries, interacts with the camera, and can speak back to the user in a natural, human-like way. It leverages OpenAI's API for understanding natural language and ElevenLabs for high-quality voice responses.

## Features
- **Natural Language Understanding**: Uses OpenAI's GPT-4o for processing and generating responses to user queries.
- **Voice Interaction**: Uses Google Speech Recognition for understanding commands and ElevenLabs API for responding (optional).
- **Camera Integration**: Uses OpenCV to interact with the user via the laptop's camera.

## Requirements
- **Python 3.7+**
- **API Keys**: OpenAI API Key, ElevenLabs API Key (optional for advanced voice synthesis).
- **Microphone and Camera**: To interact via voice and video.

## Setup

1. **Clone this Repository**:
   ```sh
   git clone https://github.com/your-username/Personal-Assistant-with-ChatGPT-4o.git
   cd Personal-Assistant-with-ChatGPT-4o
   ```

2. **Install Required Packages**:
   Install all the required Python packages using `pip`:
   ```sh
   pip install -r requirements.txt
   ```

3. **Environment Variables**:
   - Create a `.env` file in the root directory.
   - Copy the content of `.env.example` and rename it to `.env`. Replace the placeholders with your actual API keys.

   Example `.env` file:
   ```dotenv
   OPENAI_API_KEY=your_openai_api_key_here
   ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
   ELEVENLABS_VOICE_ID=your_voice_id_here
   ```

4. **Run JARVIS**:
   Start the virtual assistant using:
   ```sh
   python3 jarvis.py
   ```

## Usage
- JARVIS will start by introducing itself and wait for your commands.
- You can ask questions like:
  - "What time is it?"
  - "Can you see me?" (JARVIS will activate the camera and display the video feed)
  - "What's the weather like today?" (requires proper API integration for weather services)
- To stop JARVIS, use commands like "exit", "quit", "goodbye", or press `CTRL+C` to terminate.

## File Structure
- **jarvis.py**: The main script to run the JARVIS assistant.
- **.env.example**: Example file for environment variables.
- **requirements.txt**: Lists all the dependencies required for the project.
- **README.md**: Documentation for setting up and using the JARVIS assistant.
- **assets/**: (Optional) Folder for storing related images or media files.
- **docs/**: Folder for additional usage documentation or guides.

## Camera Interaction
JARVIS can access your camera to provide a visual interaction. The assistant will acknowledge when it "sees" you by recognizing faces and responding verbally. Press `'q'` to quit the camera feed.

### Note on Camera Permissions
On macOS, you might need to allow camera access to Python. Go to `System Preferences` -> `Security & Privacy` -> `Camera` and ensure that Python has permission to access the camera.

## Troubleshooting
- **API Key Issues**: Ensure that your `.env` file has valid API keys.
- **Microphone Issues**: Make sure your microphone is properly connected and permissions are granted.
- **Camera Issues**: If JARVIS can't access your camera, check that it is not being used by another application and has the necessary permissions.
- **Dependencies**: If you face issues with missing packages, try reinstalling dependencies:
  ```sh
  pip install -r requirements.txt
  ```

## Contribution
Feel free to fork this repository, submit issues, or create pull requests. Contributions are always welcome!

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer
This project is for educational purposes only and is not affiliated with Marvel or the Iron Man franchise.

## Contact
For any questions or suggestions, please reach out to [your-email@example.com].

