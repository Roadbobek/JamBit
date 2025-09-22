import customtkinter as ctk

class ControlPanel(ctk.CTkFrame):
    def __init__(self, master, sequencer):
        super().__init__(master)
        self.sequencer = sequencer

        # --- Widgets ---
        self.play_button = ctk.CTkButton(self, text="Play", command=self.sequencer.play)
        self.stop_button = ctk.CTkButton(self, text="Stop", command=self.sequencer.stop)
        self.bpm_label = ctk.CTkLabel(self, text=f"BPM: {self.sequencer.bpm}")

        # --- Layout ---
        self.play_button.pack(side="left", padx=5, pady=10)
        self.stop_button.pack(side="left", padx=5, pady=10)
        self.bpm_label.pack(side="left", padx=10, pady=10)
