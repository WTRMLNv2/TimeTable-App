# utils.py
# Utility functions for the UI components
def int_to_time(num):
	"""Convert integer time (e.g. 930) to (hour, minute) tuple."""
	hh = num // 100
	mm = num % 100
	return hh, mm

def fmt_time(t):
	"""Format integer time as HH:MM string."""
	try:
		hh = t // 100
		mm = t % 100
		return f"{hh:02d}:{mm:02d}"
	except Exception:
		return str(t)

def get_grid_position(container, x, y, days, total_slots):
	"""Convert window coordinates to grid position (row, column)."""
	cx = container.winfo_rootx()
	cy = container.winfo_rooty()
	rx = x - cx
	ry = y - cy
	cell_width = container.winfo_width() / (len(days) + 1)
	cell_height = container.winfo_height() / (total_slots + 1)
	col = int(rx / cell_width)
	row = int(ry / cell_height)
	col = max(1, min(col, len(days)))
	row = max(1, min(row, total_slots))
	return row, col
