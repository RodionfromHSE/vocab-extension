from setuptools import setup

APP = ['main.py']
OPTIONS = {
    'argv_emulation': False,  # Changed from True to False
    'packages': ['PyQt5', 'pynput'],
    # 'iconfile': 'main.icns',  # Optional: add if you have an icon file
    'plist': {
        'CFBundleShortVersionString': '1.0.0',
        'LSBackgroundOnly': True,  # Makes it a background app
        'LSUIElement': True,       # Hides it from Dock
    },
    # Add these excludes to avoid Carbon framework issues
    'excludes': ['tkinter', 'Carbon'],  
    # Include these specific modules needed by PyQt
    'includes': ['PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtWidgets'],
}

setup(
    app=APP,
    name="WordSaver",
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    version="1.0.0",
)