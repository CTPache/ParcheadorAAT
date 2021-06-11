# -*- coding: utf-8 -*-
from PyQt5 import QtGui
from PyQt5.QtWidgets import QGridLayout, QLabel, QProgressBar, QWidget, QMainWindow, QPushButton, QApplication
from PyQt5.QtCore import QObject, QThread, pyqtSignal, Qt
import requests
import zipfile
import os
import json
import subprocess
import winreg
import sys
import winsound
from joblib import Parallel, delayed

URL = 'https://api.github.com/repos/CTPache/ParcheadorAAT/releases/latest'


def execute(cmd):
            completed = subprocess.run(
                ["powershell", "-Command", cmd], capture_output=True)
            return completed.returncode

def executePatch(line, path, patch, callback, flag):

            if line[0] == '#' or flag == 0:
                return
                    
            files = line.split(',')
            parche = patch + files[1].replace('\n','')
            original = path + files[0].replace('\n','')
            dest = path + files[1].replace('\n','')
            
            tmp = 0
            if original == dest:
                tmp = 1
                dest = dest + '.tmp'
            cmd = '& \'' + resource_path('res\\xdelta3.exe') + "\' -d -f -s \'" + original + "\' \'" + parche + ".delta\' \'" + dest + '\''
            result = execute(cmd)
            
            if tmp and result == 0:
                execute('rm \''+ original + '\'')
                result = execute('mv -Force \''+ dest + '\'' +' \'' + original +'\'')
            callback(result)

class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    label = pyqtSignal(str)
    percent = 0
    path = winreg.QueryValueEx(winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Steam App 787480"), "InstallLocation")[0] + "\\"
    patch = ".\\Patch\\"
    flag = 1

    def getRelease(self):
            r = requests.get(URL)
            jsonFile = json.loads(r.text)
           
            try:
                versionID = open(self.path + "version.txt", 'r').readline().split(',')[0]
            except:
                versionID = -1

            if versionID == (str)(jsonFile['name']) :
                return 0
            else:
                versionID = (str)(jsonFile['name'])

                
                if not os.path.isdir('./Patch'):
                    
                    self.label.emit('Descargando última versión del parche...')
                    i = 0
                    asset = jsonFile['assets'][i]
                    while(asset['name']!='Patcher.zip'):
                        i+=1
                        asset = jsonFile['assets'][i]      
                    patcherZip = requests.get(asset['browser_download_url'])
                    open('patcher.zip', 'wb').write(patcherZip.content)
                    with zipfile.ZipFile('patcher.zip', 'r') as zip_ref:
                        zip_ref.extractall(self.path)
                    execute('rm patcher.zip')

                    i = 0
                    asset = jsonFile['assets'][i]
                    while(asset['name']!='Patch.zip'):
                        i+=1
                        asset = jsonFile['assets'][i]                   
                    patchZip = requests.get(asset['browser_download_url'])                
                    open('patch.zip', 'wb').write(patchZip.content)
                    with zipfile.ZipFile('patch.zip', 'r') as zip_ref:
                        zip_ref.extractall('Patch')
                    execute('rm patch.zip')
             
                    self.label.emit('¡Parche descargado!')

                return versionID
                
    def parcheaFichero(self):
                        
            results = Parallel(n_jobs= -1, backend="threading")(delayed(executePatch)(i, self.path, self.patch, self.callback, self.flag) for i in self.lines)
            
    def callback(self, result):
                if result or self.flag == 0:
                    self.flag = 0
                    self.lines = []
                else:
                    self.percent += 1
                    self.progress.emit( int( (self.percent / len(self.lines)) * 100 ) )
                     

    def run(self):

            versionID = self.getRelease()
                            
            if versionID:
                         
                self.label.emit('Aplicando el parche...')
                file1 = open('Patch\\files.txt', 'r')
                self.lines = file1.readlines()
                file1.close()
                self.parcheaFichero()
                if self.flag == 0:
                    self.label.emit('Ha sucedido un error al parchear el juego. Verifica los ficheros del juego en Steam y vuelve a \nintentarlo (Propiedades -> Archivos Locales -> Verificar integridad de los archivos del juego...).')
                    self.finished.emit()
                    return
                execute("Remove-Item -Path Patch -Force -Recurse")
                versionfile = open(self.path + '\\version.txt', 'w+') 
                versionfile.writelines([versionID, ',' ,URL])          
                versionfile.close()
                execute("rm \'"+self.path+"\\Patcher.exe\'")
                self.label.emit("¡Parche aplicado! Abre el juego desde tu biblioteca para jugar." )
            else:
                self.label.emit("Parche en su última versión." )
            self.finished.emit()


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
        self.thread.finished.connect(self.finished)
        self.thread.finished.connect(
            lambda: self.prog.setValue(100)
        )
    def finished(self):
        self.save.setEnabled(True)
        winsound.MessageBeep()

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
        self.setWindowTitle("Parcheador de Ace Attorney Trilogy - versión 1.0.1")
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
