import streamlit as st
from audio_recorder_streamlit import audio_recorder
from openai import OpenAI
from deepgram import DeepgramClient, PrerecordedOptions
import tempfile
import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play
import time
load_dotenv()

# --- Page Configuration ---
st.set_page_config(
    page_title="Voice AI Agent",
    page_icon="🤖",
    layout="centered",
)

# --- API Key Management ---
st.sidebar.header("API Configurations")
st.sidebar.markdown("""
Enter your API keys below. For deployed apps, it's recommended to use Streamlit's secrets management.
""")


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID") # Example Voice ID for "Bella"

# Initialize clients in session state to avoid re-creating them on every run
if 'openai_client' not in st.session_state:
    if OPENAI_API_KEY:
        st.session_state.openai_client = OpenAI(api_key=OPENAI_API_KEY)

if 'deepgram_client' not in st.session_state:
    if DEEPGRAM_API_KEY:
        st.session_state.deepgram_client = DeepgramClient(DEEPGRAM_API_KEY)

if 'elevenlabs_api_key' not in st.session_state:
    st.session_state.elevenlabs_api_key = ELEVENLABS_API_KEY


# --- Core Functions ---

def transcribe_audio(audio_bytes):
    """Transcribes audio bytes using Deepgram's API."""
    if not DEEPGRAM_API_KEY or 'deepgram_client' not in st.session_state:
        st.error("Deepgram API key is not set. Please enter it in the sidebar.")
        return None
        
    try:
        source = {'buffer': audio_bytes, 'mimetype': 'audio/wav'}
        options = PrerecordedOptions(model="nova-2", smart_format=True)
        response = st.session_state.deepgram_client.listen.rest.v("1").transcribe_file(source, options)
        return response["results"]["channels"][0]["alternatives"][0]["transcript"]
    except Exception as e:
        st.error(f"Error during transcription: {e}")
        return None

def get_ai_response(prompt):
    """Gets a response from OpenAI's chat model."""
    if not OPENAI_API_KEY or 'openai_client' not in st.session_state:
        st.error("OpenAI API key is not set. Please enter it in the sidebar.")
        return None
    try:
        response = st.session_state.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful and friendly assistant. Keep your answers concise."},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error getting AI response: {e}")
        return None

def text_to_speech(text):
    """Converts text to speech using ElevenLabs API."""
    if not st.session_state.elevenlabs_api_key:
        st.error("ElevenLabs API key is not set. Please enter it in the sidebar.")
        return None
    try:
        client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
        
        audio = client.text_to_speech.convert(
            text=text,
            voice_id=ELEVENLABS_VOICE_ID,
            model_id="eleven_multilingual_v2",
            # output_format="mp3_44100_128"
        )
        return audio
    except Exception as e:
        st.error(f"Error in text-to-speech conversion: {e}")
        return None

# --- Streamlit App Interface ---

st.title("🤖 Real-Time Voice AI Agent")
st.markdown("""
**How to use:**
1.  Click the microphone icon to start recording.
2.  Click the icon again to stop recording.
3.  The AI will transcribe your speech, think, and respond with voice.
""")

# Check if all API keys are provided before showing the recorder
if not all([DEEPGRAM_API_KEY, OPENAI_API_KEY, ELEVENLABS_API_KEY]):
    st.warning("Please provide all required API keys in the sidebar to activate the voice agent.")
else:
    # Audio recorder component
    audio_bytes = audio_recorder(
        text="Click to start/stop recording",
        recording_color="#e8b62c",
        neutral_color="#6aa36f",
        icon_name="microphone",
        pause_threshold=2.0,
        sample_rate=41_000,
        key="audio_recorder"
    )

    if audio_bytes:
        # Write the audio to a file for playback
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
            temp_audio_file.write(audio_bytes)
            temp_audio_path = temp_audio_file.name

        # --- Start the AI processing pipeline ---
        st.markdown("---")
        
        # Step 1: Transcribe the audio
        with st.spinner("Transcribing your voice..."):
            user_prompt = transcribe_audio(audio_bytes)

        if user_prompt:
            # Container for the conversation log
            with st.expander("Conversation Log", expanded=True):
                st.info(f"**You said:** {user_prompt}")
                
                # Step 2: Get AI response
                with st.spinner("🤖 Thinking..."):
                    ai_reply = get_ai_response(user_prompt)
                
                if ai_reply:
                    st.success(f"**AI says:** {ai_reply}")

                    # Step 3: Convert AI response to speech
                    with st.spinner("🔊 Generating voice response..."):
                        ai_audio = text_to_speech(ai_reply)
                    
                    if ai_audio:
                        # Show "AI is speaking" animation
                        with st.spinner("🔊 AI is speaking..."):
                            placeholder = st.empty()
                            icons = ["🔈", "🔉", "🔊"]
                            for _ in range(6):  # animate for a few seconds
                                for icon in icons:
                                    placeholder.markdown(f"<h4 style='text-align:center;'>{icon} AI Speaking...</h4>", unsafe_allow_html=True)
                                    time.sleep(0.3)
                            placeholder.empty()
                            # Play the actual audio
                            play(ai_audio)

                    else:
                        st.error("Failed to generate audio response.")
                else:
                    st.error("Failed to get a response from the AI.")
        else:
            st.error("Transcription failed. Please try speaking again.")
            
        # Clean up the temporary audio file
        os.remove(temp_audio_path)
    
    st.markdown("""
    ---
    **Note:** If the recorder is not working, please check the troubleshooting guide above. You may need to grant microphone permissions in your browser.
    """)