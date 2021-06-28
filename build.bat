pyinstaller --clean --noconfirm --onefile --console --icon "./res/icon.ico" --add-data "./res;res"  ".\Patcher.py"
Rmdir /S /Q __pycache__
Rmdir /S /Q build
del Patcher.spec
copy dist\Patcher.exe PatcherNew.exe
Rmdir /S /Q dist