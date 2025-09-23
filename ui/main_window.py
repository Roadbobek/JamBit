import customtkinter as ctk
from ui.control_panel import ControlPanel
from ui.track_view import TrackView

class MainWindow(ctk.CTkFrame):
    def __init__(self, master, sequencer):
        super().__init__(master)
        self.sequencer = sequencer

        # --- Layout Configuration ---
        self.grid_rowconfigure(1, weight=1) # TrackView row takes most space
        self.grid_rowconfigure(2, weight=0) # Footer row does not expand
        self.grid_columnconfigure(0, weight=1)

        # --- Create and place the widgets ---
        self.control_panel = ControlPanel(self, sequencer=self.sequencer)
        self.control_panel.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew")

        self.track_view = TrackView(self, sequencer=self.sequencer)
        self.track_view.grid(row=1, column=0, padx=10, pady=(5, 10), sticky="nsew")

        self.footer = ctk.CTkLabel(self, text="JamBit v1.2.0  |  © 2025 Roadbobek  <3",
                                   font=ctk.CTkFont(size=12))
        self.footer.grid(row=2, column=0, padx=10, pady=(0, 5), sticky="ew")

        # --- Connect Engine to UI for Highlighting ---
        self.sequencer.add_step_change_listener(self.track_view.update_highlights)
