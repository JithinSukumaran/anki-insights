from aqt import mw
from aqt.qt import QAction, QDialog, QVBoxLayout, QLabel, QPushButton, QDialogButtonBox, QTextEdit
from aqt.utils import qconnect, showInfo
import time

class StatisticsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Anki Statistics")
        self.setMinimumWidth(600)
        self.setMinimumHeight(400)
        
        layout = QVBoxLayout()

        # Add a label for total number of cards
        self.total_cards_label = QLabel()
        layout.addWidget(self.total_cards_label)

        # Add a label for total time elapsed in studies
        self.total_time_label = QLabel()
        layout.addWidget(self.total_time_label)

        # Add a text edit for cards per deck (this will include the bar chart)
        self.cards_per_deck_chart = QTextEdit()
        self.cards_per_deck_chart.setReadOnly(True)
        layout.addWidget(self.cards_per_deck_chart)

        # Add OK button
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def update_statistics(self, total_cards, total_time, cards_per_deck):
        self.total_cards_label.setText(f"Total number of cards: {total_cards}")

        # minutes, seconds = divmod(int(total_time), 60)
        # self.total_time_label.setText(f"Total time elapsed in studies: {minutes} minutes and {seconds} seconds")


        total_seconds = int(total_time)
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.total_time_label.setText(f"Total time elapsed in studies: {hours} hours : {minutes} minutes : {seconds} seconds")



        # Generate the HTML content for the bar chart
        html_content = self.generate_bar_chart_html(cards_per_deck)
        self.cards_per_deck_chart.setHtml(html_content)

    def generate_bar_chart_html(self, cards_per_deck):
        # Create HTML content for the bar chart
        bars = ""
        for deck, count in cards_per_deck.items():
            bar_width = count * 5  # Scale the bar width
            bars += f"""
            <div style="margin: 5px 0;">
                <span style="display: inline-block; width: 150px;">{deck}</span>
                <div style="display: inline-block; background-color: brown; width: {bar_width}px; height: 20px;"></div>
                <span> {count} cards</span>
            </div>
            """
        html = f"""
        <html>
        <head>
            <style>
                .bar-chart {{
                    font-family: Arial, sans-serif;
                }}
            </style>
        </head>
        <body>
            <div class="bar-chart">
                {bars}
            </div>
        </body>
        </html>
        """
        return html

def show_statistics():
    col = mw.col
    if not col:
        showInfo("No collection loaded.")
        return

    # Total number of cards
    total_cards = col.card_count()

    # Cards per deck
    cards_per_deck = {deck['name']: col.db.scalar("SELECT COUNT() FROM cards WHERE did = ?", deck['id']) for deck in col.decks.all()}

    # Total time elapsed in studies (in seconds)
    total_time = col.db.scalar("SELECT SUM(time)/1000 FROM revlog")
    if total_time is None:
        total_time = 0

    # Show the statistics dialog
    dialog = StatisticsDialog(mw)
    dialog.update_statistics(total_cards, total_time, cards_per_deck)
    dialog.exec()

# Create a new menu item in the Tools menu
action = QAction("Show Anki Insights", mw)
qconnect(action.triggered, show_statistics)
mw.form.menuTools.addAction(action)