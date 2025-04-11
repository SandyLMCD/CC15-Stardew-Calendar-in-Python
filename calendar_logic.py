import json
import os

class CalendarLogic:
    def __init__(self):
        try:
            base_path = os.path.dirname(os.path.abspath(__file__))
            events_path = os.path.join(base_path, "data", "events.json")
            with open(events_path, "r", encoding="utf-8") as file:
                self.events_data = json.load(file)
        except Exception as e:
            print(f"Error loading events: {e}")
            self.events_data = {}

        # Initialize favorites dictionary
        self.favorites = {}  # Example: {"Spring": [4, 14], "Summer": [10]}

    def get_event(self, season, day):
        """Get the event for a specific season and day."""
        print(f"Looking up event for season: {season}, Day: {day}")  # Debug line
        season_events = self.events_data.get(season, {})
        return season_events.get(str(day), "No events for this date.")

    def toggle_favorite(self, season, day):
        """Toggle favorite status for a date. Return True if marked as favorite, False if unmarked."""
        if season not in self.favorites:
            self.favorites[season] = []

        if day in self.favorites[season]:
            self.favorites[season].remove(day)
            print(f"Unmarked {season} {day} as favorite")
            return False  # Unmarked
        else:
            self.favorites[season].append(day)
            print(f"Marked {season} {day} as favorite")
            return True  # Marked

    def is_favorite(self, season, day):
        """Check if a date is marked as favorite."""
        return day in self.favorites.get(season, [])
