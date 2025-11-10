# TimeTable

A friendly desktop weekly timetable app built with CustomTkinter and plain JSON storage. It lets you add, edit, delete, and visualise weekly events in a simple, modern UI.

**Note**:
 - Don't want this mess of a zip and downloading all the dependencies? Download the .exe version [here](https://github.com/WTRMLNv2/TimeTable-App/releases/tag/1.0)! 

## Highlights

- Clean weekly timetable UI showing a 7-day grid (Mon–Sun).
- Add / edit / remove individual events via modal popups.
- Persist events in a single `events.json` file at the project root.
- Lightweight: no database required — just Python + customtkinter.
- Small, modular codebase: `core.py` provides event storage helpers; `ui/` contains UI components and helpers.

## Quick demo (what it does)

- Open the app and see a weekly view with time slots.
- Click "Add Event" to create a new entry with name, date, start/end times (as integers like `900` for 09:00), and a type (study/fun/break).
- Right-click an event to edit or delete it.
- Use "Remove Event" to pick from existing events and remove one exactly.
- Use "Clear All" to wipe all events.

## Requirements

- Python 3.8+
- tkinter (built-in on most Python installers; on some Linux you may need to install `python3-tk`)
- customtkinter (install via pip)

Install the Python dependency:

```powershell
# from project root (Windows PowerShell)
python -m pip install --upgrade pip
python -m pip install customtkinter
```
(or you can always download a .exe version [here](https://github.com/WTRMLNv2/TimeTable-App/releases/tag/1.0) and **skip** all these steps!) 

## Run

There are two ways to start the app from the project root folder:

```powershell
# Option A: run the packaged entry script
python .\ui\main.py

# Option B: run as module (works from root too)
python -m ui.main
```

Note: `UI.py` contains a Timetable class at the project root; the recommended entry is `ui/main.py`, which configures appearance and launches the UI.

## Project layout

- `core.py` — event helper functions (add_event, delete_event, delete_event_exact, update_event, get_all_event, clear_all_events)
- `events.json` — JSON file storing events; created automatically if missing. Contains a top-level `{ "events": [ ... ] }` array of objects.
- `UI.py` — an alternative TimetableUI implementation and UI helpers.
- `ui/` — package with modular UI code:
  - `ui/main.py` — entrypoint that launches the timetable
  - `ui/timetable.py` — main TimetableUI class and grid logic
  - `ui/utils.py` — small helpers (time formatting, grid math)
  - `ui/popups.py`, `ui/dragdrop.py` — popup dialogues and drag/drop helpers

## events.json format and examples

`events.json` keeps an `events` array. Each item is an object with a single key = event name, and the value contains details.

Example:

```json
{
  "events": [
    {
      "Math class": {
        "type": "study",
        "start_time": 900,
        "end_time": 1030,
        "date": "03-11-2025"
      }
    }
  ]
}
```

- `start_time`, `end_time`: integers like `930` (09:30) or `1400` (14:00).
- `date`: string in `DD-MM-YYYY` format.
- `type`: one of `study`, `fun`, `break` (used for colouring, extendable).

## Using the Python helpers (quick examples)

You can manipulate events from Python using `core.py` helpers. Example:

```python
from core import add_event, get_all_event, delete_event_exact

add_event("Math class", "03-11-2025", 900, 1030, eventType="study")
print(get_all_event())
# delete a single exact event
delete_event_exact("Math class", "03-11-2025", 900, 1030)
```

These helpers operate directly on `events.json` in the project root.

## Development notes

- The UI uses `customtkinter` for a modern look. If you prefer base tkinter, you can adapt the widgets.
- Times are parsed and displayed using helper `int_to_time` and `fmt_time` in `ui/utils.py`.
- The timetable grid computes rows from `start_hour`, `end_hour`, and `slot_minutes` passed to the UI class.
- When events end after the configured `end_hour`, the UI will expand the grid to include them.

## Extending / Ideas

- Add recurring events (weekly, monthly).
- Export/import (CSV / iCal) features.
- Add reminders / notifications.
- Add keyboard shortcuts and better accessibility.

## Troubleshooting

- If the UI fails to start: ensure `customtkinter` is installed and you are using a supported Python version.
- If `events.json` is missing, the app will create an empty one automatically. If permission errors occur, run in a folder where you have write access.

## Contributing

Contributions welcome. Please open issues or pull requests. Keep changes small and include tests or screenshots when relevant.

## License

This project is provided under the MIT license — feel free to reuse and modify.

---

If you'd like, I can:
- Add a short example script to seed `events.json` with demo events.
- Add a minimal `requirements.txt` or `pyproject.toml`.
- Add usage screenshots or a short GIF (you'd need to provide one).

Tell me which extras you want, and I will add them next.
