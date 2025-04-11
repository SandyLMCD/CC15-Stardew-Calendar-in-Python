import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from stardew_calendar import Ui_MainWindow
from calendar_logic import CalendarLogic


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.calendar_logic = CalendarLogic()

        # Track the currently selected date and season
        self.selected_season = None
        self.selected_date = None

        # Set styles
        self.ui.selectedDateLabel.setStyleSheet("font-size: 16px;")
        self.ui.eventLabel.setStyleSheet("font-size: 16px;")
        self.ui.centralwidget.setStyleSheet("background-image: url('resources/background.jpg');")  # Adjust path if needed

        self.ui.selectedDateLabel.setText("Select a date from the calendar")
        self.ui.eventLabel.setText("No event selected")

        # Connect calendar buttons and markFavoriteButton
        self.connect_buttons()
        self.ui.markFavoriteButton.clicked.connect(self.mark_as_favorite)

    def connect_buttons(self):
        """Connect calendar buttons to event handler"""
        for button in self.ui.calendarGroupBox.findChildren(QPushButton):
            button.clicked.connect(self.update_selected_date_label)

    def update_selected_date_label(self):
        """Handle calendar button click"""
        clicked_button = self.sender()
        if not clicked_button:
            return

        # Get the selected season and date
        self.selected_season = self.ui.seasonComboBox.currentText()
        normalized_season = self.normalize_season_name(self.selected_season)
        try:
            self.selected_date = int(clicked_button.text())
        except ValueError:
            return

        # Update labels
        self.ui.selectedDateLabel.setText(f"{normalized_season} {self.selected_date}")
        event_text = self.calendar_logic.get_event(normalized_season, self.selected_date)
        self.ui.eventLabel.setText(event_text)

        # Reset the button color to default
        self.update_button_styles()

    def mark_as_favorite(self):
        """Mark the selected date as a favorite"""
        if self.selected_season and self.selected_date:
            normalized_season = self.normalize_season_name(self.selected_season)
            # Toggle the favorite status in the logic
            self.calendar_logic.toggle_favorite(normalized_season, self.selected_date)
            # Update the button color based on the new favorite status
            self.update_button_styles()

    def update_button_styles(self):
        """Update the color of each button based on favorite status"""
        for button in self.ui.calendarGroupBox.findChildren(QPushButton):
            try:
                date = int(button.text())
            except ValueError:
                continue

            if self.selected_season:
                normalized_season = self.normalize_season_name(self.selected_season)
                if self.calendar_logic.is_favorite(normalized_season, date):
                    # Mark as favorite (e.g., yellow background)
                    button.setStyleSheet("background-color: #FFEB3B; font-weight: bold;")
                else:
                    # Reset style
                    button.setStyleSheet("")

    def normalize_season_name(self, season):
        """Map UI season names to JSON keys"""
        season_mapping = {
            "Spring": "Spring 🌸",
            "Summer": "Summer ☀️",
            "Fall": "Fall 🍂",
            "Winter": "Winter ❄️"
        }
        return season_mapping.get(season, season)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
