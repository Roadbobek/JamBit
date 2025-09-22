import customtkinter as ctk
from ui.main_window import MainWindow
from engine.sequencer import Sequencer
from engine.audio_manager import AudioManager

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("JamBit")
        self.geometry("900x600")

        # Set the appearance mode
        ctk.set_appearance_mode("Dark")

        # Create the audio engine and manager
        self.audio_manager = AudioManager()
        self.sequencer = Sequencer(audio_manager=self.audio_manager)

        # Create and show the main window, passing the sequencer to it
        self.main_window = MainWindow(self, sequencer=self.sequencer)
        self.main_window.pack(expand=True, fill="both")

if __name__ == "__main__":
    app = App()
    app.mainloop()
