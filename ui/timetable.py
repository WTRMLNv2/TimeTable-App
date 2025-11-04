# TimetableUI main class
# Merges all the functions into a single class for the UI
# ================================================================================================= #

import customtkinter as ctk
import tkinter as tk
from core import *
import datetime
import math
from ui.popups import *
from ui.dragdrop import *
from ui.utils import *

class TimetableUI(ctk.CTk):
    def draw_events(self):
        events = get_all_event()

        # color map by event type
        type_colors = {
            "study": "#B388FF",  # purple
            "fun": "#69F0AE",    # green
            "break": "#FFD740",  # yellow
        }

        for idx, event in enumerate(events):
            for name, details in event.items():
                try:
                    event_date = datetime.datetime.strptime(details["date"], "%d-%m-%Y").date()
                    start_h, start_m = int_to_time(details["start_time"])
                    end_h, end_m = int_to_time(details["end_time"])
                except Exception as e:
                    print(f"⚠️ Skipping malformed event '{name}': {e}")
                    continue

                day_index = event_date.weekday()
                if not (0 <= day_index < len(self.days)):
                    continue
                col = day_index + 1

                start_minutes = start_h * 60 + start_m
                end_minutes = end_h * 60 + end_m
                slot_start = (start_minutes - self.start_hour * 60) / self.slot_minutes
                slot_end = (end_minutes - self.start_hour * 60) / self.slot_minutes

                slot_start_clipped = max(0.0, slot_start)
                slot_end_clipped = min(self.total_slots, slot_end)
                if slot_end_clipped <= 0 or slot_start_clipped >= self.total_slots:
                    continue

                grid_row = 1 + int(math.floor(slot_start_clipped))
                rowspan = max(1, int(math.ceil(slot_end_clipped - math.floor(slot_start_clipped))))

                event_type = details.get("type", "").lower()
                color = type_colors.get(event_type, "#B0BEC5")

                block = ctk.CTkFrame(self.container, fg_color=color, corner_radius=6, border_width=0, border_color=color)
                block.grid(row=grid_row, column=col, rowspan=rowspan, sticky="nsew", padx=2, pady=1)

                block.grid_meta = {"row": grid_row, "column": col, "rowspan": rowspan, 
                                 "event_name": name, "event_details": details.copy()}

                # label
                start_str = f"{start_h:02d}:{start_m:02d}"
                end_str = f"{end_h:02d}:{end_m:02d}"
                text = f"{name}\n{start_str} - {end_str}"

                lbl = ctk.CTkLabel(block, text=text, anchor="w", justify="left", text_color="black")
                lbl.pack(expand=True, fill="both", padx=4, pady=4)
    def __init__(self, start_hour=8, end_hour=18, slot_minutes=30):
        super().__init__()
        self.title("Weekly Timetable")
        # Drag-and-drop feature removed for cleaner code
        screen_w = self.winfo_screenwidth()
        app_w = 1100
        app_h = 700
        x = (screen_w // 2) - (app_w // 2)
        y = 0
        self.geometry(f"{app_w}x{app_h}+{x}+{y}")
        self.days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        self.start_hour = start_hour
        self.end_hour = end_hour
        self.slot_minutes = slot_minutes
        try:
            events_for_range = get_all_event()
            latest_end_minutes = None
            for ev in events_for_range:
                for _, details in ev.items():
                    try:
                        et = details.get("end_time")
                        if isinstance(et, int):
                            eh = et // 100
                            em = et % 100
                            minutes = eh * 60 + em
                            if latest_end_minutes is None or minutes > latest_end_minutes:
                                latest_end_minutes = minutes
                    except Exception:
                        continue
            if latest_end_minutes is not None:
                needed_end_hour = math.ceil(latest_end_minutes / 60)
                if needed_end_hour > self.end_hour:
                    self.end_hour = min(24, needed_end_hour)
        except Exception:
            pass
        self.total_slots = int((self.end_hour - self.start_hour) * 60 / self.slot_minutes)
        self.container = ctk.CTkFrame(self)
        self.container.place(relx=0.43, rely=0.495, anchor="center", relwidth=0.85, relheight=0.98)
        for col, day in enumerate(["Time"] + self.days):
            lbl = ctk.CTkLabel(self.container, text=day, height=30, anchor="center", corner_radius=6, text_color="white")
            lbl.grid(row=0, column=col, sticky="nsew", padx=2, pady=2)
        for slot in range(self.total_slots):
            minutes_since_midnight = self.start_hour * 60 + slot * self.slot_minutes
            hh = minutes_since_midnight // 60
            mm = minutes_since_midnight % 60
            time_text = f"{hh:02d}:{mm:02d}" if mm == 0 else ""
            tlabel = ctk.CTkLabel(self.container, text=time_text, anchor="w", text_color="white")
            tlabel.grid(row=1 + slot, column=0, sticky="nsew", padx=2, pady=1)
        cols = len(self.days) + 1
        for c in range(cols):
            self.container.grid_columnconfigure(c, weight=1)
        for r in range(self.total_slots + 1):
            self.container.grid_rowconfigure(r, weight=1)
        self.draw_events()
        self.add_buttons()
        self._current_context_popup = None

    def open_clear_all_popup(self):
        from ui.popups import open_clear_all_popup
        open_clear_all_popup(self, self.refresh_timetable)

    def open_delete_event_popup(self):
        from ui.popups import open_delete_event_popup
        open_delete_event_popup(self, self.refresh_timetable)

    def open_add_event_popup(self):
        from ui.popups import open_add_event_popup
        open_add_event_popup(self, self.refresh_timetable)

    def open_edit_event_popup(self, orig_name, orig_details):
        from ui.popups import open_edit_event_popup
        open_edit_event_popup(self, orig_name, orig_details, self.refresh_timetable)

    def _get_grid_position(self, x, y):
        return get_grid_position(self.container, x, y, self.days, self.total_slots)

    def add_buttons(self):
        """Add action buttons (Add / Remove / Clear All) to the main window."""
        try:
            ctk.CTkButton(self, text="Add Event", corner_radius=20, fg_color="#8B5CF6", hover_color="#6946BD", text_color="white", command=self.open_add_event_popup).place(relx=0.99, rely=0.1, relwidth=0.13, anchor="e")
            ctk.CTkButton(self, text="Remove Event", corner_radius=20, fg_color="#EF4444", hover_color="#B91C1C", text_color="white", command=self.open_delete_event_popup).place(relx=0.99, rely=0.15, relwidth=0.13, anchor="e")
            ctk.CTkButton(self, text="Clear All", corner_radius=20, fg_color="#F59E0B", hover_color="#D97706", text_color="white", command=self.open_clear_all_popup).place(relx=0.99, rely=0.2, relwidth=0.13, anchor="e")
        except Exception:
            # If CTk isn't available or placement fails, silently continue to avoid crash
            pass

    def refresh_timetable(self):
        """Clear and rebuild the grid, then redraw events."""
        # clear old events and redraw
        for widget in self.container.winfo_children():
            widget.destroy()
        # rebuild header + grid
        for col, day in enumerate(["Time"] + self.days):
            lbl = ctk.CTkLabel(self.container, text=day, height=30, anchor="center", corner_radius=6, text_color="white")
            lbl.grid(row=0, column=col, sticky="nsew", padx=2, pady=2)
        for slot in range(self.total_slots):
            minutes_since_midnight = self.start_hour * 60 + slot * self.slot_minutes
            hh = minutes_since_midnight // 60
            mm = minutes_since_midnight % 60
            time_text = f"{hh:02d}:{mm:02d}" if mm == 0 else ""
            tlabel = ctk.CTkLabel(self.container, text=time_text, anchor="w", text_color="white")
            tlabel.grid(row=1 + slot, column=0, sticky="nsew", padx=2, pady=1)
        self.draw_events()
