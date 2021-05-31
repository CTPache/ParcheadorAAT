# -*- coding: utf-8 -*-
from PyQt5 import QtGui
from PyQt5.QtWidgets import QGridLayout, QLabel, QProgressBar, QWidget, QMainWindow, QPushButton, QApplication
from PyQt5.QtCore import QObject, QThread, pyqtSignal, Qt
import requests
import zipfile
import os
import json
import subprocess
from datetime import datetime
import winreg
import sys

URL = 'https://api.github.com/repos/CTPache/ParcheadorAAT/releases/latest'

class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    label = pyqtSignal(str)

    def parcheaFichero(self, original, parche, destino, porciento):
            numfiles = 419
            cmd = '& \'' + resource_path('res\\xdelta3.exe') + "\' -d -f -s \'" + original + "\' \'" + parche + ".delta\' \'" + destino + "\'"
            
            if (self.execute(cmd, 1) == 1 ):
                self.label.emit('Ha sucedido un error al parchear el juego. Verifica los ficheros del juego en Steam y vuelve a \nintentarlo (Propiedades -> Archivos Locales -> Verificar integridad de los archivos del juego...).')
                sys.stdout.write('\rHa sucedido un error al parchear el fichero ' + original + '. Verifica los ficheros del juego en Steam y vuelve a \nintentarlo (Propiedades -> Archivos Locales -> Verificar integridad de los archivos de juego...)')
                return 0
            else:
                sys.stdout.write('\r')
                sys.stdout.write((str)(round((porciento / numfiles) * 100, 1)) + "%")
                self.progress.emit( int( (porciento / numfiles) * 100 ) )
                sys.stdout.flush()
                return porciento + 1
                

    def getRelease(self):
            r = requests.get(URL)
            jsonFile = json.loads(r.text)
            value = winreg.QueryValueEx(winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Steam App 787480"), "InstallLocation")
            value = value[0]
            try:
                versionID = open(value + "\\version.txt", 'r').readline()
            except:
                versionID = -1

            if versionID == (str)(jsonFile['id']) :
                return 0
            else:
                versionID = (str)(jsonFile['id'])

                sys.stdout.write('\rDescargando última versión del parche...' )
                self.label.emit('Descargando última versión del parche...')
                i = 0
                asset = jsonFile['assets'][i]
                while(asset['name']!='Patch.zip'):
                    i+=1
                    asset = jsonFile['assets'][i]
                r = requests.get(asset['browser_download_url'])
                
                open('patch.zip', 'wb').write(r.content)
                with zipfile.ZipFile('patch.zip', 'r') as zip_ref:
                    zip_ref.extractall('Patch')
                self.execute('rm patch.zip')

                sys.stdout.write('\r\n¡Parche descargado!\n')                
                self.label.emit('¡Parche descargado!')

                return versionID

    def parchear(self):

            versionID = self.getRelease()
            value = winreg.QueryValueEx(winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Steam App 787480"), "InstallLocation")
            value = value[0]
                
            if versionID:
                now = datetime.now()
                pcnt = 0
                og = value + "\\PWAAT_Data\\StreamingAssets\\"
                mod = "Patch\\StreamingAssets\\"
                sys.stdout.write('\r\nAplicando parche '+ versionID +'\n')                
                self.label.emit('Aplicando el parche...')
                file1 = open('Patch\\files.txt', 'r')
                Lines = file1.readlines()

                for line in Lines:
                    if line[-2] == '*':
                        if line[-3] == '*':
                            if line[-4] == '*':
                                modded = line[:-4]
                                original = og + line[:line.find('.') - 1] + 't' + line[line.find('.'):-4]
                            else:
                                modded = line[:-3]
                                original = og + line[:line.find('.') - 1] + 'u' + line[line.find('.'):-3]
                        else:
                            modded = line[:-2]
                            original = og + line[:line.find('.') - 1] + 'f' + line[line.find('.'):-2]
                    else:
                        modded = line[:-1]
                        original = og + line[:line.find('.') - 1] + 'g' + line[line.find('.'):-1]
                    pcnt = self.parcheaFichero(original, mod + modded, og + modded, pcnt)
                    if pcnt == 0:                
                        self.execute("Remove-Item -Path Patch -Force -Recurse")
                        self.finished.emit()
                        return

                file1.close()
                # Casos raros

                sound = "Sound\\se\\wsd\\"
                dictionary = [["se120", "se14d"], ["se121", "se14e"], ["se122", "se14f"], ["se123", "se150"],
                            ["se124", "se151"], ["se125", "se152"], [
                                "se126", "se153"], ["se127", "se154"], ["se128", "se155"], ["se129", "se156"],
                            ["se12a", "se157"], ["se12b", "se158"], ["se12c", "se159"]]
                for line in dictionary:
                    modded = sound + line[1] + ".unity3d"
                    original = og + sound + line[0] + ".unity3d"
                    pcnt = self.parcheaFichero(original, mod + modded, og + modded, pcnt)
                    if pcnt == 0:                
                        self.execute("Remove-Item -Path Patch -Force -Recurse")
                        self.finished.emit()
                        return

                menu = "menu\\text\\"
                originalNames = ['option_text', 'option_text_f', 'option_text_g', 'option_text_k',
                                'option_text_t', 'option_text_s', 'option_text_u', 'credit_text']

                for line in originalNames:
                    modded = menu + line + ".bin"
                    original = og + menu + line + ".bin"
                    pcnt = self.parcheaFichero(original, mod + modded, original + ".tmp", pcnt)
                    if pcnt == 0:                
                        self.execute("Remove-Item -Path Patch -Force -Recurse")
                        self.finished.emit()
                        return
                    self.execute("rm " + original)
                    self.execute("cp " + original + ".tmp " + original)
                    self.execute("rm " + original + ".tmp")

                science = "GS1\\science\\"
                scNnames = ['itm0060', 'itm0460', 'itm0480', 'itm04c0', 'itm0610', 'itm0820', 'itm0830']
                for line in scNnames:
                    modded = science + line + "e.unity3d"
                    original = og + science + line + ".unity3d"
                    pcnt = self.parcheaFichero(original, mod + modded, og + modded, pcnt)
                    if pcnt == 0:                
                        self.execute("Remove-Item -Path Patch -Force -Recurse")
                        self.finished.emit()
                        return

                og = value + "\\PWAAT_Data\\Managed\\Assembly-CSharp.dll"
                mod = "Patch\\Managed\\Assembly-CSharp.dll"
                pcnt = self.parcheaFichero(og, mod, og + ".tmp", pcnt)
                if pcnt == 0:            
                        self.execute("Remove-Item -Path Patch -Force -Recurse")
                        self.finished.emit()
                        return
                self.execute("rm '" + og + "'")
                self.execute("cp '" + og + ".tmp' '" + og + "'")
                self.execute("rm '" + og + ".tmp'")

                sys.stdout.write('\r')
                sys.stdout.write("Parche aplicado en " + (str)(datetime.now() - now))
                sys.stdout.flush()
                self.execute("Remove-Item -Path Patch -Force -Recurse")
                open(value + '\\version.txt', 'w+').write(versionID)                
                sys.stdout.write("¡Parche aplicado! Abre el juego desde tu biblioteca para jugar." )
                self.label.emit("¡Parche aplicado! Abre el juego desde tu biblioteca para jugar." )
            else:
                sys.stdout.write( "Parche en su última versión." )
                self.label.emit("Parche en su última versión." )
            self.finished.emit()

    def execute(self, cmd, verbose = 0):
            completed = subprocess.run(
                ["powershell", "-Command", cmd], capture_output=True)
            if verbose and (completed.stdout.decode('utf-8') != "" or completed.stderr.decode('utf-8') != "") :
                    print(completed.stdout.decode('utf-8'), completed.stderr.decode('utf-8'))
            return completed.returncode
    
    def run(self):
            self.parchear()


class Main(QWidget):
    def parchearThread(self):
        self.prog.setValue(0)
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.reportProgress)
        self.worker.label.connect(self.changelabel)
        self.thread.start()
        self.save.setEnabled(False)
        self.thread.finished.connect(
            lambda: self.save.setEnabled(True)
        )
        self.thread.finished.connect(
            lambda: self.prog.setValue(100)
        )

    def reportProgress(self, n):
        self.prog.setValue(n)

    def changelabel(self, n):
        self.label.setText(n)

    def __init__(self):
        super().__init__()
        
        layout = QGridLayout()
        self.save = QPushButton("", self)
        self.save.setToolTip("Parchear el juego a su última versión.")  
        self.save.clicked.connect(self.parchearThread)
        self.save.setFixedSize(154,30)
        
        self.prog = QProgressBar(self)

        self.label = QLabel()
        self.label.setText("Parchea tu copia original de Steam.")
        self.label.setFixedSize(624,40)
        layout.addWidget(self.prog, 0, 0)
        layout.addWidget(self.label, 1, 0)
        layout.addWidget(self.save, 0, 1)
        layout.setAlignment(Qt.AlignBottom)
        self.setLayout(layout)

def resource_path(relative_path):
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

class Window(QMainWindow):

    def __init__(self):
        super().__init__()
  
        self.setWindowIcon(QtGui.QIcon(resource_path('res\\logo.jpg')))
        self.setFixedSize(640,360)
        self.setWindowTitle("Parcheador de Ace Attorney Trilogy")
        bgPath = (str)(resource_path('res\\background.jpg').encode())[1:]
        bgPath = bgPath.replace("\\\\", "/")
        buttonPath = (str)(resource_path('res\\b1.png').encode())[1:]
        buttonPath = buttonPath.replace("\\\\", "/")
        buttonPath2 = (str)(resource_path('res\\b2.png').encode())[1:]
        buttonPath2 = buttonPath2.replace("\\\\", "/")

        self.setStyleSheet('\
        *   {\
                border-image: url('+ bgPath +') 0 0 0 0 stretch stretch;\
                font-size: 15px;\
            }\
        \
            ')
        self.setCentralWidget(Main())
        self.centralWidget().setStyleSheet('\
        QPushButton {\
                border-image: url('+ buttonPath +') 0 0 0 0 stretch stretch;\
                background-color: white;\
                border: 2px solid #ffc31d;\
                padding: 4px;\
                color: white;\
            }\
        QPushButton::pressed,\
        QPushButton::hover {\
                border-image: url('+ buttonPath2 +') 0 0 0 0 stretch stretch;\
                background-color: white;\
                border: 2px solid #ffc31d;\
                padding: 4px;\
                color: white;\
            }\
        QPushButton::!enabled {\
                border-image: url('+ buttonPath2 +') 0 0 0 0 stretch stretch;\
                background-color: grey;\
                border: 2px solid grey;\
                padding: 4px;\
                color: grey;\
            }\
        QProgressBar{\
                border-image: url();\
                border: 2px solid white;\
                color: black;\
                text-align: center;\
            }\
        QLabel{\
                border-image : url();\
                background-color : #88888888;\
                color : white;\
                padding : 1px;\
            }\
        QProgressBar::chunk {\
                border-image: url();\
                background-color: #338dbf;\
            }\
        QToolTip {\
                border-image: url();\
                background-color: #338dbf;\
            }\
        ')

def init():
    app = QApplication(sys.argv)

    win = Window()
    win.show()

    sys.exit(app.exec_())

init()