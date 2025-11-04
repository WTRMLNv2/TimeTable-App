# main.py
# The main, runnable script.
# Entry point for Timetable UI
# ================================================================================================== #
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from timetable import TimetableUI

if __name__ == "__main__":
    import customtkinter as ctk
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("dark-blue")
    app = TimetableUI(start_hour=8, end_hour=20, slot_minutes=30)
    app.mainloop()
