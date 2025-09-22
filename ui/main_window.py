import customtkinter as ctk
from ui.control_panel import ControlPanel
from ui.track_view import TrackView

class MainWindow(ctk.CTkFrame):
    def __init__(self, master, sequencer):
        super().__init__(master)
        self.sequencer = sequencer

        # --- Layout Configuration ---
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # --- Create and place the widgets ---
        # Pass the sequencer to the control panel
        self.control_panel = ControlPanel(self, sequencer=self.sequencer)
        self.control_panel.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Pass the sequencer to the track view
        self.track_view = TrackView(self, sequencer=self.sequencer)
        self.track_view.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
