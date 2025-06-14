import streamlit as st
import io
import os
import random
from remix_engine import remix_song

# --- Preset Values (Single Source of Truth) ---
PRESETS = {
    "lofi": {"pitch": -3, "speed": 0.92, "reverb": 0.5, "crackle_vol": 0.35, "ambient_vol": 0.45},
    "chipmunk": {"pitch": 7, "speed": 1.15, "reverb": 0.25, "crackle_vol": 0.25, "ambient_vol": 0.3},
    "nightcore": {"pitch": 5, "speed": 1.3, "reverb": 0.3, "crackle_vol": 0.15, "ambient_vol": 0.25},
    "Dreamy": {"pitch": -3, "speed": 0.8, "reverb": 0.55, "crackle_vol": 0.25, "ambient_vol": 0.55},
    "Vintage": {"pitch": -1, "speed": 0.88, "reverb": 0.22, "crackle_vol": 0.45, "ambient_vol": 0.35},
    "Glitchy": {"pitch": 1, "speed": 1.12, "reverb": 0.12, "crackle_vol": 0.12, "ambient_vol": 0.15},
    "Hyperspeed": {"pitch": 6, "speed": 1.35, "reverb": 0.18, "crackle_vol": 0.1, "ambient_vol": 0.1},
    "Underwater": {"pitch": -2, "speed": 0.78, "reverb": 0.45, "crackle_vol": 0.25, "ambient_vol": 0.6},
    "Radio": {"pitch": 0, "speed": 1.0, "reverb": 0.15, "crackle_vol": 0.38, "ambient_vol": 0.3},
    "Alien": {"pitch": 12, "speed": 1.28, "reverb": 0.35, "crackle_vol": 0.2, "ambient_vol": 0.35},
    "Spooky": {"pitch": -5, "speed": 0.83, "reverb": 0.65, "crackle_vol": 0.35, "ambient_vol": 0.4},
}

# --- App Layout ---
st.set_page_config(page_title="🎚️ Audio Remix Studio", layout="centered")
st.title("🎚️ Audio Remix Studio")
st.markdown("Transform your tracks with professional effects and background layers")

# --- Callback to apply presets ---
def apply_preset():
    remix_mode = st.session_state.remix_mode
    theme = st.session_state.theme
    surprise_me = st.session_state.surprise_me

    preset_key = remix_mode
    if remix_mode == "themed":
        if surprise_me:
            theme_options = list({k for k in PRESETS.keys() if k not in ["lofi", "chipmunk", "nightcore"]})
            if len(theme_options) > 1 and "active_preset" in st.session_state:
                 if st.session_state.active_preset in theme_options:
                    theme_options.remove(st.session_state.active_preset)
            preset_key = random.choice(theme_options)
        else:
            preset_key = theme

    st.session_state.active_preset = preset_key
    preset_values = PRESETS.get(preset_key, {})

    for key, value in preset_values.items():
        st.session_state[key] = value

# --- Session State Initialization ---
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.remix_mode = "lofi"
    st.session_state.theme = "Dreamy"
    st.session_state.surprise_me = False
    apply_preset()

# --- File Upload ---
with st.expander("🎧 Upload Audio Files", expanded=True):
    main_audio = st.file_uploader("Main audio track (MP3)", type=["mp3"])
    col1, col2 = st.columns(2)
    with col1:
        crackle_audio = st.file_uploader("Vinyl crackle (optional)", type=["mp3", "wav"])
    with col2:
        ambient_audio = st.file_uploader("Ambient background (optional)", type=["mp3", "wav"])
    st.caption("🔍 Tip: Search for crackles or ambient sounds at [freesound.org](https://freesound.org)")

# --- Mode & Theme Selection ---
st.markdown("## 🎚️ Remix Settings")
remix_mode = st.selectbox(
    "Choose remix mode",
    ["lofi", "chipmunk", "nightcore", "themed"],
    key='remix_mode',
    on_change=apply_preset
)

is_themed_mode = remix_mode == "themed"
if is_themed_mode:
    theme_options = list({k for k in PRESETS.keys() if k not in ["lofi", "chipmunk", "nightcore"]})
    theme_col1, theme_col2 = st.columns([2,1])
    with theme_col1:
        st.selectbox("Choose a theme", theme_options, key="theme", on_change=apply_preset)
    with theme_col2:
        st.checkbox("🎲 Surprise me", key="surprise_me", on_change=apply_preset, help="Randomly picks a new theme.")

# --- Effect Controls ---
with st.expander("🎛️ Effect Controls", expanded=True):
    st.slider("Pitch Shift", -12, 12, key="pitch", disabled=is_themed_mode)
    st.slider("Playback Speed", 0.5, 2.0, key="speed", step=0.01, disabled=is_themed_mode)
    st.slider("Reverb Amount", 0.0, 1.0, key="reverb", step=0.01, disabled=is_themed_mode)
    if is_themed_mode:
        st.info("Pitch, Speed, and Reverb are controlled by the selected Theme.")

# --- Background Volume Sliders ---
if crackle_audio or ambient_audio:
    with st.expander("🔊 Background Mix", expanded=True):
        if crackle_audio:
            st.slider("Crackle Volume", 0.0, 1.0, key="crackle_vol", step=0.01)
        else:
            st.session_state.crackle_vol = 0.0
        if ambient_audio:
            st.slider("Ambient Volume", 0.0, 1.0, key="ambient_vol", step=0.01)
        else:
            st.session_state.ambient_vol = 0.0
else:
    st.session_state.crackle_vol = 0.0
    st.session_state.ambient_vol = 0.0

# --- Process Button ---
st.markdown("---")
if main_audio:
    if st.button("✨ Process Audio"):
        with st.spinner("🧑‍🎤 Remixing your track..."):
            try:
                output_path = remix_song(
                    song_bytes=main_audio.read(),
                    crackle_bytes=crackle_audio.read() if crackle_audio else None,
                    ambient_bytes=ambient_audio.read() if ambient_audio else None,
                    remix_mode=st.session_state.remix_mode,
                    pitch=st.session_state.pitch,
                    speed=st.session_state.speed,
                    reverb_wet=st.session_state.reverb,
                    crackle_vol=st.session_state.crackle_vol,
                    ambient_vol=st.session_state.ambient_vol,
                    theme=st.session_state.active_preset
                )

                with open(output_path, "rb") as f:
                    audio_bytes = f.read()
                    st.success("🎶 Remix complete! Listen to your creation:")
                    st.audio(audio_bytes, format="audio/mp3")
                    st.download_button("⬇️ Download Remix", audio_bytes, "remixed_track.mp3", "audio/mp3")
                os.unlink(output_path)
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.exception(e) # Also log the full traceback for debugging
else:
    st.warning("⚠️ Please upload a main audio file to begin.")
