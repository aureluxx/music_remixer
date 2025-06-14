import io
import tempfile
import random
import numpy as np
from pydub import AudioSegment
from pedalboard import (
    Pedalboard, Reverb, PitchShift, LowpassFilter, HighpassFilter,
    Distortion, Delay, Chorus, Phaser, Compressor
)

def ensure_format(audio: AudioSegment) -> AudioSegment:
    # Force stereo, 44.1kHz, 16-bit
    return audio.set_channels(2).set_frame_rate(44100).set_sample_width(2)

def get_theme_effects(theme):
    board = Pedalboard()
    speed = 1.0 # Default speed, though UI now controls this

    if theme == "Dreamy":
        board.append(Reverb(room_size=0.8, wet_level=0.5))
        board.append(PitchShift(-2))
        board.append(LowpassFilter(8000))
        speed = 0.85
    elif theme == "Vintage":
        board.append(Reverb(room_size=0.3, wet_level=0.2))
        board.append(Distortion(drive_db=10))
        board.append(LowpassFilter(6000))
        board.append(HighpassFilter(150))
        speed = 0.9
    elif theme == "Glitchy":
        board.append(Phaser(rate_hz=2.0))
        board.append(Chorus())
        board.append(Distortion(drive_db=8))
        speed = 1.1
    elif theme == "Hyperspeed":
        board.append(Chorus())
        board.append(PitchShift(5))
        board.append(Delay(delay_seconds=0.1))
        speed = 1.3
    elif theme == "Underwater":
        board.append(LowpassFilter(2000))
        board.append(Reverb(room_size=0.9, wet_level=0.4))
        board.append(Compressor())
        speed = 0.8
    elif theme == "Radio":
        board.append(HighpassFilter(400))
        board.append(LowpassFilter(4000))
        board.append(Distortion(drive_db=12))
        board.append(Delay(delay_seconds=0.05))
    elif theme == "Alien":
        board.append(PitchShift(random.choice([-12, 12])))
        board.append(Chorus())
        speed = random.choice([0.75, 1.25])
    elif theme == "Spooky":
        board.append(Reverb(room_size=0.9, wet_level=0.6))
        board.append(PitchShift(-4))
        board.append(Delay(delay_seconds=0.3))
        board.append(LowpassFilter(3000))
        speed = 0.85

    return board, speed

def audiosegment_to_numpy(audio: AudioSegment):
    samples = np.array(audio.get_array_of_samples()).astype(np.float32) / 32768.0
    if audio.channels == 2:
        samples = samples.reshape((-1, 2))
    else:
        samples = samples.reshape((-1, 1))
    return samples

def numpy_to_audiosegment(samples: np.ndarray, sample_rate=44100):
    samples = (samples * 32768).clip(-32768, 32767).astype(np.int16)
    if samples.ndim == 1:
        channels = 1
        interleaved = samples
    else:
        channels = samples.shape[1]
        interleaved = samples.flatten()
    return AudioSegment(
        interleaved.tobytes(), frame_rate=sample_rate, sample_width=2, channels=channels
    )

def remix_song(song_bytes, crackle_bytes=None, ambient_bytes=None,
               remix_mode="lofi", theme=None, pitch=0, speed=1.0,
               reverb_wet=0.3, crackle_vol=0.1, ambient_vol=0.2):

    song = ensure_format(AudioSegment.from_file(io.BytesIO(song_bytes)))
    original_duration = len(song)

    def prepare_bg(bg_bytes, volume):
        if not bg_bytes or volume <= 0:
            return AudioSegment.silent(duration=original_duration).set_channels(2)
        bg = ensure_format(AudioSegment.from_file(io.BytesIO(bg_bytes)))
        # Adjust volume using pydub's dB scale
        gain = -30 * (1.0 - volume)
        bg = bg + gain
        return (bg * ((original_duration // len(bg)) + 1))[:original_duration]

    crackle = prepare_bg(crackle_bytes, crackle_vol)
    ambient = prepare_bg(ambient_bytes, ambient_vol)

    board = Pedalboard()

    # The UI layer now determines all parameters. This engine just applies them.
    if remix_mode == "themed":
        # In themed mode, a complex board is retrieved, and sliders are ignored.
        board, _ = get_theme_effects(theme) # We ignore the speed returned here
    elif remix_mode == "chipmunk":
        board.append(PitchShift(pitch))
    elif remix_mode == "nightcore":
        board.append(PitchShift(pitch))
    else:  # lofi is the default
        board.append(PitchShift(pitch))
        board.append(Reverb(wet_level=reverb_wet))

    # Apply speed change directly from the UI-provided value
    if abs(speed - 1.0) > 0.01:
        song = song.speedup(playback_speed=speed)

    # Apply pedalboard effects
    samples = audiosegment_to_numpy(song)
    processed = board(samples, song.frame_rate)
    song = numpy_to_audiosegment(processed, sample_rate=song.frame_rate)

    # Overlay backgrounds
    final_mix = song.overlay(crackle).overlay(ambient)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        final_mix.export(f.name, format="mp3")
        return f.name
