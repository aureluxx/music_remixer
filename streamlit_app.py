import streamlit as st
import io
import os
import random
from remix_engine import remix_song

# --- Preset Values ---
PRESETS = {
    "lofi": {"pitch": -3, "speed": 0.92, "reverb": 0.5, "slowdown": 0.8, "crackle_vol": 0.35, "ambient_vol": 0.45},
    "chipmunk": {"pitch": 7, "speed": 1.15, "reverb": 0.25, "crackle_vol": 0.25, "ambient_vol": 0.3},
    "nightcore": {"pitch": 5, "speed": 1.3, "reverb": 0.3, "crackle_vol": 0.15, "ambient_vol": 0.25},
    "Dreamy": {"pitch": -3, "speed": 0.8, "reverb": 0.55, "slowdown": 1.0, "crackle_vol": 0.25, "ambient_vol": 0.55},
    "Vintage": {"pitch": -1, "speed": 0.88, "reverb": 0.22, "slowdown": 1.0, "crackle_vol": 0.45, "ambient_vol": 0.35},
    "Glitchy": {"pitch": 1, "speed": 1.12, "reverb": 0.12, "slowdown": 1.0, "crackle_vol": 0.12, "ambient_vol": 0.15},
    "Hyperspeed": {"pitch": 6, "speed": 1.35, "reverb": 0.18, "slowdown": 1.0, "crackle_vol": 0.1, "ambient_vol": 0.1},
    "Underwater": {"pitch": -2, "speed": 0.78, "reverb": 0.45, "slowdown": 1.0, "crackle_vol": 0.25, "ambient_vol": 0.6},
    "Radio": {"pitch": 0, "speed": 1.0, "reverb": 0.15, "slowdown": 1.0, "crackle_vol": 0.38, "ambient_vol": 0.3},
    "Alien": {"pitch": 12, "speed": 1.28, "reverb": 0.35, "slowdown": 1.0, "crackle_vol": 0.2, "ambient_vol": 0.35},
    "Spooky": {"pitch": -5, "speed": 0.83, "reverb": 0.65, "slowdown": 1.0, "crackle_vol": 0.35, "ambient_vol": 0.4},
}

# --- App Layout ---
st.set_page_config(page_title="🎚️ Audio Remix Studio", layout="centered")
st.title("🎚️ Audio Remix Studio")
st.markdown("Transform your tracks with professional effects and background layers")

# --- File Upload ---
with st.expander("🎧 Upload Audio Files", expanded=True):
    main_audio = st.file_uploader("Main audio track (MP3)", type=["mp3"])
    col1, col2 = st.columns(2)
    with col1:
        crackle_audio = st.file_uploader("Vinyl crackle (optional)", type=["mp3", "wav"])
    with col2:
        ambient_audio = st.file_uploader("Ambient background (optional)", type=["mp3", "wav"])
    st.caption("🔍 Tip: Search for crackles or ambient sounds at [freesound.org](https://freesound.org)")

# --- Session State Init ---
def update_sliders_from_preset(preset):
    st.session_state.pitch = preset.get("pitch", 0)
    st.session_state.speed = preset.get("speed", 1.0)
    st.session_state.reverb = preset.get("reverb", 0.3)
    st.session_state.slowdown = preset.get("slowdown", 0.85)
    st.session_state.crackle_vol = preset.get("crackle_vol", 0.1)
    st.session_state.ambient_vol = preset.get("ambient_vol", 0.2)
    st.session_state.manual_speed = False  # Reset manual override

if "initialized" not in st.session_state:
    update_sliders_from_preset(PRESETS["lofi"])
    st.session_state.initialized = True

if "manual_speed" not in st.session_state:
    st.session_state.manual_speed = False

# --- Mode & Theme Selection ---
st.markdown("## 🎚️ Remix Settings")
remix_mode = st.selectbox("Choose remix mode", ["lofi", "chipmunk", "nightcore", "themed"])
theme = None
surprise_me = False

if remix_mode == "themed":
    theme_options = list({k for k in PRESETS.keys() if k not in ["lofi", "chipmunk", "nightcore"]})
    theme_col1, theme_col2 = st.columns(2)
    with theme_col1:
        theme = st.selectbox("Choose a theme", theme_options)
    with theme_col2:
        surprise_me = st.checkbox("🎲 Surprise me")
else:
    theme_options = []

# --- Auto Apply Preset ---
preset_key = random.choice(theme_options) if remix_mode == "themed" and surprise_me else (theme if remix_mode == "themed" else remix_mode)
preset = PRESETS.get(preset_key, {})
update_sliders_from_preset(preset)

# --- Effect Controls ---
with st.expander("🎛️ Effect Controls", expanded=True):
    pitch = st.slider("Pitch Shift", -12, 12, st.session_state.pitch)

    speed_slider = st.slider("Playback Speed", 0.5, 2.0, st.session_state.speed, 0.01)
    if speed_slider != st.session_state.speed:
        st.session_state.manual_speed = True
    st.session_state.speed = speed_slider
    speed = speed_slider

    reverb = st.slider("Reverb Amount", 0.0, 1.0, st.session_state.reverb, 0.01)
    slowdown = st.slider("Slowdown (Lofi only)", 0.5, 1.0, st.session_state.slowdown, 0.01)

# --- Background Volume Sliders ---
if crackle_audio or ambient_audio:
    with st.expander("🔊 Background Mix", expanded=True):
        if crackle_audio:
            crackle_vol = st.slider("Crackle Volume", 0.0, 1.0, st.session_state.crackle_vol, 0.01)
        else:
            crackle_vol = 0.0
        if ambient_audio:
            ambient_vol = st.slider("Ambient Volume", 0.0, 1.0, st.session_state.ambient_vol, 0.01)
        else:
            ambient_vol = 0.0
else:
    crackle_vol = 0.0
    ambient_vol = 0.0

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
                    remix_mode=remix_mode,
                    pitch=pitch,
                    speed=speed,
                    reverb_wet=reverb,
                    slowdown=slowdown,
                    crackle_vol=crackle_vol,
                    ambient_vol=ambient_vol,
                    theme=theme,
                    surprise_me=surprise_me,
                    manual_speed=st.session_state.manual_speed
                )

                with open(output_path, "rb") as f:
                    audio_bytes = f.read()
                    st.success("🎶 Remix complete! Listen to your creation:")
                    st.audio(audio_bytes, format="audio/mp3")
                    st.download_button("⬇️ Download Remix", audio_bytes, "remixed_track.mp3", "audio/mp3")
                os.unlink(output_path)
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
else:
    st.warning("⚠️ Please upload a main audio file to begin.")
