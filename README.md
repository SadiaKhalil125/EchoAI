# EchoAI: Real-Time Voice AI Agent

EchoAI is an interactive and user-friendly voice-powered AI assistant. It leverages state-of-the-art AI services for speech-to-text, natural language processing, and text-to-speech to provide a seamless conversational experience.

## Features

-   **Voice-based Interaction:** Speak directly to the AI through your microphone.
-   **Real-time Transcription:** Fast and accurate speech-to-text conversion.
-   **Intelligent Responses:** Get coherent and contextually relevant answers from a powerful language model.
-   **Natural Voice Output:** Hear the AI's response in a high-quality, natural-sounding voice.
-   **Web-based Interface:** Easy-to-use interface built with Streamlit that runs directly in your browser.
-   **Conversation Log:** Keep track of the dialogue with an expandable conversation log.

## How It Works

EchoAI processes your voice input in a sequential pipeline:

1.  **Audio Recording:** The Streamlit application uses an audio recorder component to capture your voice from the microphone.
2.  **Speech-to-Text:** The recorded audio is sent to the Deepgram API, which transcribes it into text.
3.  **AI Response Generation:** The transcribed text is then sent as a prompt to the OpenAI API (using the GPT-3.5-turbo model), which generates a thoughtful and relevant response.
4.  **Text-to-Speech:** The AI's text response is converted into audible speech using the ElevenLabs API.
5.  **Audio Playback:** The generated audio is then played back to you directly in the browser.

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

Make sure you have Python 3.8 or higher installed on your system. You will also need to have accounts with the following services to obtain the necessary API keys:

-   [OpenAI](https://platform.openai.com/signup)
-   [Deepgram](https://console.deepgram.com/signup)
-   [ElevenLabs](https://beta.elevenlabs.io/sign-up)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/EchoAI.git
    cd EchoAI
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required Python libraries:**
    ```bash
    pip install -r requirements.txt
    ```
    *Note: If a `requirements.txt` file is not available, you can create one with the following content or install the packages manually:*

    ```
    streamlit
    audio-recorder-streamlit
    openai
    deepgram-sdk
    python-dotenv
    elevenlabs
    ```

    Then run `pip install -r requirements.txt`.

## Configuration

This application requires API keys for OpenAI, Deepgram, and ElevenLabs to function correctly.

1.  Create a file named `.env` in the root directory of your project.

2.  Add your API keys and your chosen ElevenLabs Voice ID to the `.env` file in the following format:

    ```env
    OPENAI_API_KEY="your_openai_api_key"
    DEEPGRAM_API_KEY="your_deepgram_api_key"
    ELEVENLABS_API_KEY="your_elevenlabs_api_key"
    ELEVENLABS_VOICE_ID="your_elevenlabs_voice_id"
    ```
    *You can find your Voice ID on the "Voice Lab" page of your ElevenLabs account.*

## Usage

Once you have completed the installation and configuration steps, you can run the Streamlit application.

1.  Open your terminal or command prompt in the project's root directory.

2.  Run the following command:
    ```bash
    streamlit run app.py
    ```
    *(Assuming you have named the Python script `app.py`)*

3.  The application will open in a new tab in your default web browser.

4.  Make sure to grant the browser permission to use your microphone when prompted.

## Technologies Used

-   **Streamlit:** For creating and running the web application.
-   **audio-recorder-streamlit:** A custom component for recording audio in Streamlit.
-   **OpenAI API (GPT-3.5-turbo):** For generating intelligent text-based responses.
-   **Deepgram API (Nova-2):** For high-quality speech-to-text transcription.
-   **ElevenLabs API:** For converting text into natural-sounding speech.
-   **Python-dotenv:** For managing environment variables and API keys.

## Troubleshooting

-   **Recorder Not Working:** If the audio recorder is not functioning, ensure you have granted microphone permissions to your browser for the application's URL. You can usually manage this in your browser's settings.
-   **API Key Errors:** If you encounter errors related to API keys, double-check that your `.env` file is correctly formatted and that the keys have been copied accurately.
-   **Audio Playback Issues:** Some browsers may have restrictions on autoplaying audio. Ensure your browser is up to date and that there are no extensions blocking audio playback.
