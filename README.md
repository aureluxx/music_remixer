# Music Remixer 🎛🎶

[![Streamlit App](https://img.shields.io/badge/Streamlit-Live-green)](https://musicremixer-aureluxx.streamlit.app)
[![License](https://img.shields.io/github/license/aureluxx/music_remixer)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/aureluxx/music_remixer?style=social)](https://github.com/aureluxx/music_remixer/stargazers)

A simple web app that lets you remix your songs with various effects and styles, powered by Streamlit, Pydub, and Spotify's Pedalboard.

🌐 **Live Demo:**  
Try it out on Streamlit Cloud 👉 [Launch Music Remixer](https://musicremixer-aureluxx.streamlit.app)

---

## Features

- 🎛 Apply audio effects such as reverb, pitch shift, distortion, and more.
- 🎚 Multiple remix presets like:
  - Lofi
  - Chipmunk
  - Nightcore
  - Dreamy
  - Vintage
  - Glitchy
  - Hyperspeed
  - Underwater
- 📂 Upload any song (MP3, WAV, etc.) and download the remixed version.
- 🌐 Fully browser-based interface via Streamlit.

---

## Installation (for local development)

### 1. Clone the repository

```bash
git clone https://github.com/aureluxx/music_remixer.git
cd music_remixer
```

### 2. Create a virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Pyhton dependencies

```bash
pip install -r requirements.txt
```

### 4. Install system dependencies (for audio processing)

This project uses `ffmpeg` (which includes `ffprobe`) to process audio via the Pydub library.

To install `ffmpeg` locally:

- **macOS (Homebrew):** `brew install ffmpeg`  
- **Ubuntu/Debian:** `sudo apt install ffmpeg`  
- **Windows:** Download from https://ffmpeg.org/download.html and ensure `ffmpeg` is added to your system PATH.

> 🛠 For **Streamlit Cloud deployment**, `ffmpeg` is installed automatically via the `packages.txt` file included in this repository.

### 5. Run the app

```bash
streamlit run streamlit_app.py
```

---

## Sample Usage

1. Start the Streamlit server.
2. Upload your audio file.
3. Select the remix preset.
4. Download your remixed audio file!

---

## Credits

- Built using [Streamlit](https://streamlit.io/)
- Audio processing via [Pydub](https://github.com/jiaaro/pydub) and [Spotify Pedalboard](https://github.com/spotify/pedalboard)

---

## License

This project is licensed under the MIT License.