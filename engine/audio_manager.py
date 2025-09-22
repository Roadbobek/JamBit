import pygame
import numpy as np

class AudioManager:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        try:
            # Explicitly request a 2-channel (stereo) mixer
            pygame.mixer.init(frequency=self.sample_rate, size=-16, channels=2, buffer=256)
            print("Audio mixer initialized successfully.")
        except pygame.error as e:
            print(f"Error initializing audio mixer: {e}")
            pygame.mixer.init(driver='dummy')

        self.sounds = {}
        self._generate_sounds()

    def _generate_sounds(self):
        """Creates a set of basic synthesized sounds."""
        self.sounds["Kick"] = self.create_kick(frequency=150, length_ms=150)
        self.sounds["Snare"] = self.create_snare(length_ms=150)
        self.sounds["Hat"] = self.create_hat(length_ms=80)
        print("Synthesized sounds created.")

    def _ms_to_samples(self, ms):
        """Converts milliseconds to number of samples."""
        return int(self.sample_rate * (ms / 1000.0))

    def _generate_waveform(self, frequency, length_ms, wave_type='square', decay=True):
        """Generates a numpy array representing a waveform."""
        num_samples = self._ms_to_samples(length_ms)
        t = np.linspace(0, length_ms / 1000.0, num_samples, False)

        if wave_type == 'square':
            wave = 0.5 * np.sign(np.sin(2 * np.pi * frequency * t))
        elif wave_type == 'noise':
            wave = np.random.uniform(-0.5, 0.5, num_samples)
        else:
            wave = np.zeros(num_samples)

        if decay:
            decay_rate = np.linspace(1, 0, num_samples)
            wave *= decay_rate**2

        return wave

    def _to_pygame_sound(self, wave):
        """Converts a numpy wave array to a playable stereo pygame.Sound object."""
        # Scale to 16-bit integer range
        wave_int = (wave * 32767).astype(np.int16)

        # Create a 2-channel (stereo) array
        stereo_wave = np.zeros((len(wave_int), 2), dtype=np.int16)
        stereo_wave[:, 0] = wave_int  # Left channel
        stereo_wave[:, 1] = wave_int  # Right channel

        return pygame.sndarray.make_sound(stereo_wave)

    def create_kick(self, frequency, length_ms):
        """Creates a kick drum sound with a pitch drop."""
        num_samples = self._ms_to_samples(length_ms)
        t = np.linspace(0, length_ms / 1000.0, num_samples, False)
        
        instant_freq = np.linspace(frequency, 40, num_samples)
        # Increased amplitude from 0.5 to 0.9 for a louder kick
        wave = 0.9 * np.sin(2 * np.pi * instant_freq * t)

        decay = np.linspace(1, 0, num_samples)
        wave *= decay**2.5

        return self._to_pygame_sound(wave)

    def create_snare(self, length_ms):
        """Creates a snare sound from a noise burst and a sine pop."""
        noise_part = self._generate_waveform(0, length_ms, 'noise', decay=True)
        
        tone_part = self._generate_waveform(250, length_ms // 2, 'square', decay=True)
        noise_part[:len(tone_part)] += tone_part * 0.5

        # Reduce the final amplitude to lower the snare's volume
        noise_part *= 0.5

        return self._to_pygame_sound(noise_part)

    def create_hat(self, length_ms):
        """Creates a hi-hat sound from a short burst of white noise."""
        wave = self._generate_waveform(0, length_ms, 'noise', decay=True)
        return self._to_pygame_sound(wave)

    def play_sound(self, sound_name):
        """Plays a loaded sound by its name."""
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
        else:
            print(f"Attempted to play a sound that is not loaded: {sound_name}")

    def set_global_volume(self, volume):
        """Sets the volume for all sounds.
        Args:
            volume (float): A value from 0.0 (silent) to 1.0 (full).
        """
        for sound in self.sounds.values():
            sound.set_volume(volume)
