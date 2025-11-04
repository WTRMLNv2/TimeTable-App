# core.py
# contains some functions of the app
# ============================Imports============================
import json
import os


# ============================Functions============================
def get_all_event():
    with open(EVENTS_FILE, 'r') as file:
        data = json.load(file)
    return data.get("events", [])
# -------------------------------------------------------------



def add_event(eventName, eventDate, eventStart, eventEnd, eventType="study"):
    # Load existing events.json
    with open(EVENTS_FILE, "r") as file:
        data = json.load(file)
    # Create the new event structure
    new_event = {
        eventName: {
            "type": eventType,
            "start_time": eventStart,
            "end_time": eventEnd,
            "date": eventDate
        }
    }
    # Add to the "events" list
    data["events"].append(new_event)
    # Save back to events.json
    with open(EVENTS_FILE, "w") as file:
        json.dump(data, file, indent=4)
    print(f"✅ Event '{eventName}' added successfully!")
# -------------------------------------------------------------
def delete_event(eventName):
    # Load existing events.json
    with open(EVENTS_FILE, "r") as file:
        data = json.load(file)
    # Find and remove the event by name
    original_length = len(data["events"])
    data["events"] = [event for event in data["events"] if eventName not in event]
    if len(data["events"]) < original_length:
        # Save back to events.json
        with open(EVENTS_FILE, "w") as file:
            json.dump(data, file, indent=4)
        print(f"✅ Event '{eventName}' deleted successfully!")
    else:
        print(f"❌ Event '{eventName}' not found.")
# -------------------------------------------------------------
def delete_event_exact(eventName, eventDate, eventStart, eventEnd):
    """
    Delete a single event that exactly matches name, date, start and end times.
    This avoids removing all events that share the same name.
    """
    with open(EVENTS_FILE, "r") as file:
        data = json.load(file)

    removed = False
    for i, event in enumerate(data.get("events", [])):
        # each event is a dict with a single key = name
        if eventName in event:
            details = event[eventName]
            if (
                details.get("date") == eventDate
                and details.get("start_time") == eventStart
                and details.get("end_time") == eventEnd
            ):
                # remove this exact entry
                del data["events"][i]
                removed = True
                break

    if removed:
        with open(EVENTS_FILE, "w") as file:
            json.dump(data, file, indent=4)
        print(f"✅ Event '{eventName}' ({eventDate} {eventStart}-{eventEnd}) deleted successfully!")
    else:
        print(f"❌ Exact event not found for '{eventName}' ({eventDate} {eventStart}-{eventEnd}).")


def update_event(orig_name, orig_date, orig_start, orig_end, new_name, new_date, new_start, new_end, new_type="study"):
    """
    Update a single event that exactly matches the original identifying fields.
    Replaces it with the new values provided.
    Returns True if updated, False if not found.
    """
    with open(EVENTS_FILE, "r") as file:
        data = json.load(file)

    updated = False
    for i, event in enumerate(data.get("events", [])):
        if orig_name in event:
            details = event[orig_name]
            if (
                details.get("date") == orig_date
                and details.get("start_time") == orig_start
                and details.get("end_time") == orig_end
            ):
                # replace with new event (keep structure: {name: {...}})
                new_event = {
                    new_name: {
                        "type": new_type,
                        "start_time": new_start,
                        "end_time": new_end,
                        "date": new_date,
                    }
                }
                data["events"][i] = new_event
                updated = True
                break

    if updated:
        with open(EVENTS_FILE, "w") as file:
            json.dump(data, file, indent=4)
        print(f"✅ Event updated: '{orig_name}' -> '{new_name}' ({new_date} {new_start}-{new_end})")
        return True
    else:
        print(f"❌ Exact event to update not found: '{orig_name}' ({orig_date} {orig_start}-{orig_end})")
        return False
def clear_all_events():
    # overwrite with empty list
    data = {"events": []}
    with open(EVENTS_FILE, "w") as file:
        json.dump(data, file, indent=4)
    print("🧹 All events cleared successfully!")


# Resolve events.json location relative to this file so the app works when
# run from any working directory. If the file doesn't exist, create an empty
# structure so other functions can operate without errors.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EVENTS_FILE = os.path.join(BASE_DIR, "events.json")

if not os.path.exists(EVENTS_FILE):
    try:
        with open(EVENTS_FILE, "w") as f:
            json.dump({"events": []}, f, indent=4)
    except Exception:
        # If we can't create the file, let functions that open it raise the
        # appropriate error later. This keeps behavior predictable.
        pass


