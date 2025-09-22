import time
import threading

class Sequencer:
    def __init__(self, audio_manager, bpm=120):
        self.audio_manager = audio_manager
        self.bpm = bpm
        self.is_playing = False
        self.current_step = 0
        self.steps_per_beat = 4  # 16th notes
        self.total_steps = 16

        # This holds the pattern data, e.g., {"Kick": [1,0,0,0,...]}
        self.patterns = {}

        # Run the sequencer loop in a separate thread
        self.thread = threading.Thread(target=self._sequencer_loop, daemon=True)
        self.thread.start()

    def _sequencer_loop(self):
        """The main loop that drives the sequencer forward in time."""
        while True:
            if self.is_playing:
                # --- Trigger sounds for the current step ---
                for sound_name, pattern in self.patterns.items():
                    if pattern[self.current_step] == 1:
                        self.audio_manager.play_sound(sound_name)

                # --- Advance to the next step ---
                self.current_step = (self.current_step + 1) % self.total_steps

                # --- Wait for the next step ---
                sleep_duration = (60 / self.bpm) / self.steps_per_beat
                time.sleep(sleep_duration)
            else:
                # If not playing, sleep a little to avoid busy-waiting
                time.sleep(0.1)

    def play(self):
        """Starts the sequencer playback."""
        self.current_step = 0
        self.is_playing = True
        print("Sequencer: Play")

    def stop(self):
        """Stops the sequencer playback."""
        self.is_playing = False
        print("Sequencer: Stop")

    def set_bpm(self, bpm):
        """Sets the tempo in beats per minute."""
        self.bpm = max(30, min(300, bpm)) # Clamp BPM to a reasonable range
        print(f"Sequencer: BPM set to {self.bpm}")
