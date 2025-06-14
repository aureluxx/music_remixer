# Music Remixer

A simple web app to remix your songs with various effects and styles, powered by Streamlit, Pydub, and Spotify's Pedalboard.

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

## Installation

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

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
streamlit run app.py
```

---

## Requirements

- Python 3.8+
- Streamlit
- Pydub
- Pedalboard
- Numpy

---

## File Structure

```
music_remixer/
├── app.py             # Streamlit frontend app
├── remix_engine.py    # Core audio remixing engine
├── requirements.txt   # Dependencies list
├── README.md          # Project description
└── .gitignore         # Git ignored files
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
