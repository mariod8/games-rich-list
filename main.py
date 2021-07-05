import sys
import webbrowser
import os
import re
import random
import json
import utils as u
from PyQt5 import QtGui
from googlesearch import search
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QGridLayout,
    QGroupBox,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QWidget,
)

width = 640
height = 640
gamesData = {}
placeholderGames = [
    "Layers Of Fear",
    "Doom Eternal",
    "Halo Infinite",
    "Terraria",
    "Prey",
    "Among Us"
]


class Game(QListWidgetItem):
    def __init__(self, text):
        super(QListWidgetItem, self).__init__()
        self.setText(text)
        data = getGameInfo(self)
        gamesData[text] = {
            "name": text,
            "description": data["description"],
            "url": data["url"]
        }


class GameList(QListWidget):
    def __init__(self):
        super(QListWidget, self).__init__()

    def addGame(self, text):
        self.addItem(Game(text))

    def loadGames(self):
        try:
            global gamesData
            gamesData = json.load(open("GRLdata.json"))
            for game in gamesData:
                self.addItem(QListWidgetItem(game))
        except:
            Exception("file not exists")


class GameInput(QLineEdit):
    def __init__(self):
        super(QLineEdit, self).__init__()
        self.setPlaceholderText(random.choice(placeholderGames))


class GameInfo(QLabel):
    def __init__(self):
        super(QLabel, self).__init__()
        self.setAlignment(Qt.AlignTop)
        self.setWordWrap(True)
        self.setOpenExternalLinks(True)
        self.setTextFormat(Qt.RichText)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Games To Play List")
        self.setFixedSize(width, height)

        # Group boxes
        self.listLayout = QGroupBox("Lista de Juegos", self)
        self.addGameLayout = QGroupBox("Añade un Juego", self)
        self.gameInfoLayout = QGroupBox("Información", self)

        # Grids
        self.gridDown = QGridLayout()
        self.grid = QGridLayout()
        self.gridRight = QGridLayout()

        self.gameList = GameList()
        self.inputLine = GameInput()
        self.gameInfo = GameInfo()
        self.icon = None

        self.grid.addWidget(self.gameList, 0, 0)

        self.gridDown.addWidget(self.inputLine, 0, 0)

        self.gridRight.addWidget(self.gameInfo, 0, 0)

        self.listLayout.setLayout(self.grid)
        self.addGameLayout.setLayout(self.gridDown)
        self.gameInfoLayout.setLayout(self.gridRight)

        self.inputLine.returnPressed.connect(
            self.addGame)
        self.gameList.itemClicked.connect(handleItemClick)

        self.widget = QWidget()
        self.finalLayout = QGridLayout()

        self.finalLayout.addWidget(self.listLayout, 0, 0)
        self.finalLayout.addWidget(self.addGameLayout, 1, 0)
        self.finalLayout.addWidget(self.gameInfoLayout, 0, 1)

        self.finalLayout.setColumnStretch(1, 20)

        self.widget.setLayout(self.finalLayout)
        self.setCentralWidget(self.widget)
        self.setWindowIcon(QtGui.QIcon(os.path.dirname(
            os.path.realpath(__file__)) + os.path.sep + "icon.png"))

        # Menu Bar ######
        self.menuBar = self.menuBar()
        self.fileMenu = self.menuBar.addMenu("Archivo")

        # Guardar
        saveData = QAction("Guardar", self)
        saveData.setShortcut("Ctrl+S")
        saveData.triggered.connect(save)

        # Salir
        exit = QAction("Salir", self)
        exit.setShortcut("Ctrl+Q")
        exit.triggered.connect(exitHandler)

        self.fileMenu.addAction(saveData)
        self.fileMenu.addAction(exit)

        #################

        self.gameList.loadGames()

        self.inputLine.setFocus()

    def addGame(self):
        text = self.inputLine.text().title()
        if not text:
            return
        self.gameList.addGame(text)
        self.inputLine.clear()

    def closeEvent(self, *args, **kwargs):
        exitHandler


def exitHandler():
    save
    app.exit()


def getGameInfo(item):
    url = getGameLink(item)
    if "https://store.steampowered.com/" not in url:
        raise Exception("page link not valid")
    html = u.getHTML(url)
    info = {
        "description":  re.search(
            "<meta content=\"(.*)\" property=\"og:description", html).group(1),
        "url": url
    }
    return info


def handleItemClick(item):
    try:
        game = gamesData[item.text()]
        result = f"<b>{game['name']}</b><br><br>{game['description']}<br><br><a href=\"{game['url']}\">Enlace</a>"
        window.gameInfo.setText(result)
    except Exception as error:
        print(f"Error: {error}")


def openBrowser(item):
    webbrowser.open(getGameLink(item))


def getGameLink(item, args=None):
    if args:
        return search(item.text() + args, num_results=1, lang="es")[0]
    else:
        return search(item.text() + " game buy steam español", num_results=1, lang="es")[0]


def save():
    with open("GRLdata.json", "w") as jf:
        d = json.dumps(gamesData, indent=4)
        jf.write(d)
        jf.close()


app = QApplication(sys.argv)
app.aboutToQuit.connect(exitHandler)

window = MainWindow()
window.show()
app.exec()
