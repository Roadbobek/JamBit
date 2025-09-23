import customtkinter as ctk

class Track(ctk.CTkFrame):
    """A single track in the sequencer, containing a name and step buttons."""
    def __init__(self, master, sound_name: str, sequencer):
        super().__init__(master)

        self.sound_name = sound_name
        self.sequencer = sequencer
        self.last_highlighted_step = -1

        # The pattern of 16 steps (0=off, 1=on)
        self.pattern = [0] * 16
        self.sequencer.patterns[self.sound_name] = self.pattern

        # --- Widgets ---
        self.name_label = ctk.CTkLabel(self, text=self.sound_name, width=100)
        self.steps = []
        for i in range(16):
            step_button = ctk.CTkButton(
                self, text="", width=30, fg_color="gray",
                command=lambda i=i: self.toggle_step(i)
            )
            self.steps.append(step_button)
        
        self.clear_button = ctk.CTkButton(self, text="Clear", width=50, command=self.clear_pattern)

        # --- Layout ---
        self.name_label.pack(side="left", padx=10, pady=10)
        for i, step in enumerate(self.steps):
            pad_x = (5, 15) if (i + 1) % 4 == 0 else 5
            step.pack(side="left", padx=pad_x, pady=10)
        
        self.clear_button.pack(side="left", padx=(15, 10), pady=10)

    def toggle_step(self, step_index):
        """Toggles a step on or off and updates its color."""
        if self.pattern[step_index] == 0:
            self.pattern[step_index] = 1
            self.steps[step_index].configure(fg_color="#3b82f6") # A nice blue
        else:
            self.pattern[step_index] = 0
            self.steps[step_index].configure(fg_color="gray")

    def clear_pattern(self):
        """Resets the track's pattern to all zeros and updates the UI.""" 
        for i in range(len(self.pattern)):
            self.pattern[i] = 0
        
        for step_button in self.steps:
            step_button.configure(fg_color="gray")

    def highlight_step(self, step_index):
        """Highlights the currently playing step by brightening its color."""
        # Reset the color of the previously highlighted step
        if self.last_highlighted_step != -1:
            last_step_color = "#3b82f6" if self.pattern[self.last_highlighted_step] == 1 else "gray"
            self.steps[self.last_highlighted_step].configure(fg_color=last_step_color)

        # Highlight the new step by making its color brighter
        if step_index != -1:
            is_on = self.pattern[step_index] == 1
            highlight_color = "#7aa5f8" if is_on else "#999999" # Light Blue if on, Darker Light Gray if off
            self.steps[step_index].configure(fg_color=highlight_color)
        
        self.last_highlighted_step = step_index

class TrackView(ctk.CTkFrame):
    """A container for all the tracks."""
    def __init__(self, master, sequencer):
        super().__init__(master)
        self.sequencer = sequencer

        # Add tracks, passing the sequencer to them
        self.kick_track = Track(self, sound_name="Kick", sequencer=self.sequencer)
        self.kick_track.pack(pady=(20, 5))

        self.snare_track = Track(self, sound_name="Snare", sequencer=self.sequencer)
        self.snare_track.pack(pady=5)

        self.hat_track = Track(self, sound_name="Hat", sequencer=self.sequencer)
        self.hat_track.pack(pady=5)

    def update_highlights(self, current_step):
        """The main listener method that tells all tracks to update their highlight."""
        self.kick_track.highlight_step(current_step)
        self.snare_track.highlight_step(current_step)
        self.hat_track.highlight_step(current_step)
