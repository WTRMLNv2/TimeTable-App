# popups.py
# Popup dialog implementations for adding, editing, deleting, and clearing events
import customtkinter as ctk
import datetime
from core import clear_all_events, get_all_event, delete_event, delete_event_exact, update_event, add_event

def open_clear_all_popup(parent, refresh_callback):
	popup = ctk.CTkToplevel(parent)
	popup.title("Clear All Events")
	popup.geometry("350x200")
	popup.grab_set()

	ctk.CTkLabel(
		popup,
		text="⚠ Are you sure you want to clear ALL events?",
		font=("Arial", 14, "bold"),
		text_color="red",
		wraplength=300,
		justify="center"
	).pack(pady=20, padx=10)

	def confirm_clear():
		clear_all_events()
		popup.destroy()
		refresh_callback()

	button_frame = ctk.CTkFrame(popup, fg_color="transparent")
	button_frame.pack(pady=10)

	ctk.CTkButton(
		button_frame,
		text="Yes, Clear All",
		fg_color="#EF4444",
		hover_color="#B91C1C",
		text_color="white",
		corner_radius=20,
		command=confirm_clear
	).pack(side="left", padx=10)

	ctk.CTkButton(
		button_frame,
		text="Cancel",
		fg_color="#6B7280",
		hover_color="#4B5563",
		text_color="white",
		corner_radius=20,
		command=popup.destroy
	).pack(side="left", padx=10)

def open_delete_event_popup(parent, refresh_callback):
	popup = ctk.CTkToplevel(parent)
	popup.title("Remove Event")
	popup.geometry("350x300")
	popup.grab_set()

	ctk.CTkLabel(popup, text="Remove Event", font=("Arial", 18, "bold")).pack(pady=10)

	events = get_all_event()
	event_names = []
	for ev in events:
		for nm, det in ev.items():
			def fmt_time(t):
				try:
					hh = t // 100
					mm = t % 100
					return f"{hh:02d}:{mm:02d}"
				except Exception:
					return str(t)
			start_s = fmt_time(det.get("start_time"))
			end_s = fmt_time(det.get("end_time"))
			display = f"{nm} | {det.get('date')} | {start_s} - {end_s}"
			event_names.append(display)

	if not event_names:
		ctk.CTkLabel(popup, text="No events found.", text_color="gray").pack(pady=20)
		return

	selected_event = ctk.StringVar(value=event_names[0])
	dropdown = ctk.CTkOptionMenu(popup, values=event_names, variable=selected_event)
	dropdown.pack(pady=15, padx=20)

	def confirm_delete():
		sel = selected_event.get()
		try:
			parts = [p.strip() for p in sel.split("|")]
			s_name = parts[0]
			s_date = parts[1]
			times = parts[2].split("-")
			s_start = int(times[0].strip().replace(':', ''))
			s_end = int(times[1].strip().replace(':', ''))
		except Exception:
			s_name = sel
			s_date = None
			s_start = None
			s_end = None

		if s_date is not None and s_start is not None and s_end is not None:
			delete_event_exact(s_name, s_date, s_start, s_end)
		else:
			delete_event(s_name)
		popup.destroy()
		refresh_callback()

	ctk.CTkButton(
		popup,
		text="Delete Event",
		fg_color="#EF4444",
		hover_color="#B91C1C",
		text_color="white",
		corner_radius=20,
		command=confirm_delete
	).pack(pady=15)

	ctk.CTkButton(
		popup,
		text="Cancel",
		fg_color="#6B7280",
		hover_color="#4B5563",
		text_color="white",
		corner_radius=20,
		command=popup.destroy
	).pack(pady=5)

def open_add_event_popup(parent, refresh_callback):
	popup = ctk.CTkToplevel(parent)
	popup.title("Add Event")
	popup.geometry("350x420")
	popup.grab_set()

	ctk.CTkLabel(popup, text="Add New Event", font=("Arial", 18, "bold")).pack(pady=10)

	name_entry = ctk.CTkEntry(popup, placeholder_text="Event name")
	name_entry.pack(pady=5, fill="x", padx=20)

	today_str = datetime.date.today().strftime("%d-%m-%Y")
	date_entry = ctk.CTkEntry(popup)
	date_entry.insert(0, today_str)
	date_entry.pack(pady=5, fill="x", padx=20)

	start_entry = ctk.CTkEntry(popup, placeholder_text="Start Time (e.g. 930)")
	start_entry.pack(pady=5, fill="x", padx=20)

	end_entry = ctk.CTkEntry(popup, placeholder_text="End Time (e.g. 1030)")
	end_entry.pack(pady=5, fill="x", padx=20)

	type_option = ctk.CTkOptionMenu(popup, values=["study", "fun", "break"])
	type_option.pack(pady=5)

	def submit():
		name = name_entry.get().strip()
		date = date_entry.get().strip()
		try:
			start = int(start_entry.get().strip())
			end = int(end_entry.get().strip())
		except Exception:
			ctk.CTkLabel(popup, text="⚠ Invalid start/end time", text_color="red").pack()
			return
		type_ = type_option.get()

		if not (name and date and start and end):
			ctk.CTkLabel(popup, text="⚠ Please fill all fields!", text_color="red").pack()
			return

		add_event(name, date, start, end, type_)
		popup.destroy()
		refresh_callback()

	ctk.CTkButton(popup, text="Add", fg_color="#8B5CF6", hover_color="#6946BD", command=submit).pack(pady=15)

def open_edit_event_popup(parent, orig_name, orig_details, refresh_callback):
	popup = ctk.CTkToplevel(parent)
	popup.title("Edit Event")
	popup.geometry("360x460")
	popup.grab_set()

	ctk.CTkLabel(popup, text="Edit Event", font=("Arial", 18, "bold")).pack(pady=10)

	name_entry = ctk.CTkEntry(popup)
	name_entry.insert(0, orig_name)
	name_entry.pack(pady=6, fill="x", padx=20)

	date_entry = ctk.CTkEntry(popup)
	date_entry.insert(0, orig_details.get("date", ""))
	date_entry.pack(pady=6, fill="x", padx=20)

	start_entry = ctk.CTkEntry(popup)
	start_entry.insert(0, str(orig_details.get("start_time", "")))
	start_entry.pack(pady=6, fill="x", padx=20)

	end_entry = ctk.CTkEntry(popup)
	end_entry.insert(0, str(orig_details.get("end_time", "")))
	end_entry.pack(pady=6, fill="x", padx=20)

	type_option = ctk.CTkOptionMenu(popup, values=["study", "fun", "break"])
	type_option.set(orig_details.get("type", "study"))
	type_option.pack(pady=6)

	def submit():
		new_name = name_entry.get().strip()
		new_date = date_entry.get().strip()
		try:
			new_start = int(start_entry.get().strip())
			new_end = int(end_entry.get().strip())
		except Exception:
			ctk.CTkLabel(popup, text="⚠ Invalid start/end time", text_color="red").pack()
			return
		new_type = type_option.get()

		update_event(
			orig_name,
			orig_details.get("date"),
			orig_details.get("start_time"),
			orig_details.get("end_time"),
			new_name,
			new_date,
			new_start,
			new_end,
			new_type,
		)
		popup.destroy()
		refresh_callback()

	ctk.CTkButton(popup, text="Save", fg_color="#8B5CF6", hover_color="#6946BD", command=submit).pack(pady=14)
	ctk.CTkButton(popup, text="Cancel", fg_color="#6B7280", hover_color="#4B5563", command=popup.destroy).pack()
