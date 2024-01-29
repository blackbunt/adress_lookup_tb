from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QWidget, QLineEdit, QStatusBar
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtPrintSupport import QPrintPreviewDialog


from PyQt5.QtCore import QUrl
import sys
import time
import re
import os
import io
from opencage.geocoder import OpenCageGeocode
from opencage.geocoder import InvalidInputError, RateLimitExceededError, UnknownError
import address_ally
import viewMap

# load config
api_key, user_loc = address_ally.load_config()
if api_key and user_loc:
# Create an instance of the OpenCage geocoder
    geocoder = OpenCageGeocode(api_key)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()



    def initUI(self):
        self.setWindowTitle('Adress Ally')
        self.setGeometry(0, 0, 1024, 800)
        self.centerOnScreen()
        # Zentral-Widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Layout für das Zentral-Widget
        layout = QHBoxLayout(central_widget)

        # Erstellen einer WebEngineView
        self.browser = QWebEngineView()
        coordinates = address_ally.get_origin_coordinates(user_loc)
        print (coordinates[0])
        map = viewMap.map(coordinates[0], 15)

        # Laden einer Website, z.B. OpenStreetMap
        self.browser.setHtml(map)
        self.setCentralWidget(self.browser)

        # Erstellen eines Suchfeldes als Kind-Widget der WebEngineView
        self.searchField = QLineEdit(self.browser)
        self.searchField.setPlaceholderText("Adresse suchen...")
        self.searchField.setGeometry(500, 20, 400, 50)  # Position und Größe des Suchfeldes
        self.searchField.setStyleSheet(
            "background-color: rgba(255, 255, 255, 0.8);")  # Leicht transparenter Hintergrund
        # Verbinden der "Enter"-Taste mit einer Suchfunktion
        self.searchField.returnPressed.connect(self.onSearch)

        # Event für Größenänderungen des Hauptfensters
        self.browser.resizeEvent = self.onResize

        # Statusleiste erstellen
        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)

        # Widget für die Buttons in der Statusleiste
        statusBarWidget = QWidget(self)
        statusBarLayout = QHBoxLayout(statusBarWidget)
        statusBarLayout.setContentsMargins(0, 0, 0, 0)  # Keine äußeren Abstände


        button_text = ["Adresse kopieren",
                       "Straße kopieren",
                       "PLZ Stadt kopieren",
                       "PLZ kopieren",
                       "Stadt kopieren",
                       ]
                       #"Drucken"]

        button_actions = [
            self.copyAddress,
            self.copyStreet,
            self.copyPLZCity,
            self.copyPLZ,
            self.copyCity,
            self.printWebContent
        ]




        # Buttons erstellen und zum Layout hinzufügen
        for i in range(len(button_text)):
            button = QPushButton(button_text[i], self)
            statusBarLayout.addWidget(button)
            # Verbinden des Buttons mit der entsprechenden Funktion
            button.clicked.connect(button_actions[i])

        # Widget der Statusleiste hinzufügen
        self.statusBar.addPermanentWidget(statusBarWidget)

    def printWebContent(self):
        # Erstellen eines Druckvorschau-Dialogs
        dialog = QPrintPreviewDialog()
        # Verbinden des `paintRequested`-Signals mit der `print_`-Methode des QWebEngineView
        dialog.paintRequested.connect(self.browser.print_)
        # Anzeigen des Dialogs
        dialog.exec_()

    def centerOnScreen(self):
        resolution = QDesktopWidget().screenGeometry()
        self.move(int((resolution.width() / 2) - (self.frameSize().width() / 2)),
                  int((resolution.height() / 2) - (self.frameSize().height() / 2)))

    def onResize(self, event):
        # Position des Suchfeldes aktualisieren, wenn das Fenster seine Größe ändert
        self.searchField.move(self.browser.width() - self.searchField.width() - 25, 25)
        QWidget.resizeEvent(self.browser, event)


    def onSearch(self):
        # Ihre Suchlogik hier
        destination = self.searchField.text()
        print("Suche nach:", destination)
        try:
            # adress suche durchführen
            destination_adress, start_adress, destination_coordinates, start_coordinates = address_ally.get_address(user_loc, destination)
            #print(f"start adresse {start_adress}")
            #print(f"ziel adresse {destination_adress}")
            #print(f"start koordinaten {start_coordinates}")
            #print(f"ziel koordinaten {destination_coordinates}")

            if destination_coordinates:
                # Erstellen einer neuen Karte mit einem Marker an den Zielkoordinaten
                map_html = viewMap.map_with_marker(destination_coordinates, 15, destination_adress)
                # Aktualisieren des QWebEngineView mit der neuen Karte
                self.browser.setHtml(map_html)
                self.street_name = destination_adress[0]
                self.street_number = destination_adress[1]
                self.plz = destination_adress[2]
                self.city = destination_adress[3]
            else:
                print("Keine Koordinaten für die angegebene Adresse gefunden.")
        except Exception as e:
            print("Fehler beim Abrufen der Koordinaten:", e)

    def copyAddress(self):
        print("Adresse kopieren")
        address_ally.copy_to_clipboard(f'{self.street_name} {self.street_number}\n{self.plz} {self.city}')

    def copyStreet(self):
        print("Straße kopieren")
        address_ally.copy_to_clipboard(f'{self.street_name} {self.street_number}')

    def copyPLZCity(self):
        print("PLZ und Stadt kopieren")
        address_ally.copy_to_clipboard(f'{self.plz} {self.city}')
    def copyPLZ(self):
        print("PLZ kopieren")
        address_ally.copy_to_clipboard(f'{self.plz}')

    def copyCity(self):
        print("Stadt kopieren")
        address_ally.copy_to_clipboard(f'{self.city}')

    def printInfo(self):
        print("Drucken")





if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

