import customtkinter as ctk

class ControlPanel(ctk.CTkFrame):
    def __init__(self, master, sequencer):
        super().__init__(master)
        self.sequencer = sequencer

        # --- Widgets ---
        self.play_button = ctk.CTkButton(self, text="Play", height=37, command=self.sequencer.play)
        self.stop_button = ctk.CTkButton(self, text="Stop", height=37, command=self.sequencer.stop)
        
        # BPM Controls Frame
        self.bpm_frame = ctk.CTkFrame(self)
        self.bpm_label_static = ctk.CTkLabel(self.bpm_frame, text="BPM:")
        self.bpm_label_value = ctk.CTkLabel(self.bpm_frame, text=str(self.sequencer.bpm), width=50)
        self.bpm_label_value.bind("<Button-1>", self._on_bpm_label_click) # Make label clickable
        self.bpm_entry = ctk.CTkEntry(self.bpm_frame, width=50)
        self.bpm_entry.bind("<Return>", self._on_bpm_entry_submit)
        self.bpm_entry.bind("<FocusOut>", self._on_bpm_entry_submit)
        self.bpm_slider = ctk.CTkSlider(self.bpm_frame, from_=30, to=300, command=self._on_bpm_slider_change)
        self.bpm_slider.set(self.sequencer.bpm)

        # Update volume label and slider to reflect the new default
        self.volume_label = ctk.CTkLabel(self, text=f"Volume: {int(self.sequencer.volume * 100)}%")
        self.volume_slider = ctk.CTkSlider(self, from_=0.0, to=1.0, command=self._on_volume_change)
        self.volume_slider.set(self.sequencer.volume)

        # --- Layout ---
        self.play_button.pack(side="left", padx=(15, 5), pady=10)
        self.stop_button.pack(side="left", padx=5, pady=10)
        
        self.bpm_frame.pack(side="left", padx=10, pady=10)
        self.bpm_frame.grid_columnconfigure(1, weight=1)

        self.bpm_label_static.grid(row=0, column=0, padx=(15, 5), pady=10, sticky="w")
        self.bpm_label_value.grid(row=0, column=1, pady=10, sticky="w")
        self.bpm_slider.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        self.volume_slider.pack(side="right", padx=10, pady=10, fill="x", expand=True)
        self.volume_label.pack(side="right", padx=(10, 0), pady=10)

        # Set initial volume in the audio engine on startup
        self.sequencer.set_volume(self.sequencer.volume)

    def _on_bpm_slider_change(self, value):
        bpm_int = int(value)
        self.sequencer.set_bpm(bpm_int)
        self.bpm_label_value.configure(text=str(bpm_int))
        if self.bpm_entry.winfo_ismapped():
            self.bpm_entry.delete(0, ctk.END)
            self.bpm_entry.insert(0, str(bpm_int))

    def _on_bpm_label_click(self, event):
        self.bpm_label_value.grid_forget()
        self.bpm_entry.grid(row=0, column=1, pady=10, sticky="w")
        self.bpm_entry.delete(0, ctk.END)
        self.bpm_entry.insert(0, str(self.sequencer.bpm))
        self.bpm_entry.focus_set()

    def _on_bpm_entry_submit(self, event):
        try:
            new_bpm = int(self.bpm_entry.get())
            self.sequencer.set_bpm(new_bpm)
            self.bpm_slider.set(self.sequencer.bpm)
            self.bpm_label_value.configure(text=str(self.sequencer.bpm))
        except ValueError:
            self.bpm_label_value.configure(text=str(self.sequencer.bpm))
        finally:
            self.bpm_entry.grid_forget()
            self.bpm_label_value.grid(row=0, column=1, pady=10, sticky="w")

    def _on_volume_change(self, value):
        self.sequencer.set_volume(value)
        self.volume_label.configure(text=f"Volume: {int(value * 100)}%")
