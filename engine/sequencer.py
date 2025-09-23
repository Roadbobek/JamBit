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
        self.volume = 0.5 # Start at 50% volume
        self.step_change_listeners = [] # A list of functions to call on step change

        # This holds the pattern data, e.g., {"Kick": [1,0,0,0,...]}
        self.patterns = {}

        # Run the sequencer loop in a separate thread
        self.thread = threading.Thread(target=self._sequencer_loop, daemon=True)
        self.thread.start()

    def add_step_change_listener(self, listener_func):
        """Adds a function to be called every time the step changes."""
        self.step_change_listeners.append(listener_func)

    def _sequencer_loop(self):
        """The main loop that drives the sequencer forward in time."""
        while True:
            if self.is_playing:
                # --- Trigger sounds for the current step ---
                for sound_name, pattern in self.patterns.items():
                    if pattern[self.current_step] == 1:
                        self.audio_manager.play_sound(sound_name)

                # --- Announce the new step to all listeners ---
                for listener in self.step_change_listeners:
                    listener(self.current_step)

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
        # When stopping, tell listeners to clear the highlight
        for listener in self.step_change_listeners:
            listener(-1) # Use -1 to indicate "no step"
        print("Sequencer: Stop")

    def set_bpm(self, bpm):
        """Sets the tempo in beats per minute, handling potential errors."""
        try:
            bpm_val = int(float(bpm)) # Allow float strings like "120.0"
            self.bpm = max(30, min(300, bpm_val)) # Clamp BPM
            print(f"Sequencer: BPM set to {self.bpm}")
        except (ValueError, TypeError):
            print(f"Invalid BPM value received: {bpm}")

    def set_volume(self, volume):
        """Passes the volume command to the audio manager and stores it."""
        self.volume = max(0.0, min(1.0, float(volume))) # Ensure volume is between 0.0 and 1.0
        self.audio_manager.set_global_volume(self.volume)
        print(f"Sequencer: Volume set to {self.volume:.2f}")
