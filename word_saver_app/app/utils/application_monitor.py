"""
Module for monitoring active applications.

This module provides functionality to detect the currently active application
and check if it's in a list of allowed applications.
"""

import platform
import subprocess
from typing import Optional

class ApplicationMonitor:
    """
    Monitors the currently active application and determines if it's in the allowed list.
    """
    
    @staticmethod
    def get_active_application() -> Optional[str]:
        """
        Get the name of the currently active application.
        
        Returns:
            str or None: Name of the active application, or None if it couldn't be determined.
        """
        system = platform.system()
        
        if system == "Darwin":  # macOS
            try:
                script = 'tell application "System Events" to get name of first application process whose frontmost is true'
                result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, check=True)
                return result.stdout.strip()
            except subprocess.SubprocessError:
                print("Error getting active application on macOS")
                return None
                
        elif system == "Windows":
            try:
                # Using PowerShell to get the active window title and process
                script = "(Get-Process | Where-Object {$_.MainWindowTitle -ne \"\"} | Select-Object -First 1).ProcessName"
                result = subprocess.run(["powershell", "-Command", script], 
                                       capture_output=True, text=True, check=True)
                return result.stdout.strip()
            except subprocess.SubprocessError:
                print("Error getting active application on Windows")
                return None
                
        elif system == "Linux":
            try:
                # Using xdotool on Linux
                result = subprocess.run(["xdotool", "getwindowfocus", "getwindowname"], 
                                      capture_output=True, text=True, check=True)
                return result.stdout.strip()
            except (subprocess.SubprocessError, FileNotFoundError):
                try:
                    # Alternative method using wmctrl
                    result = subprocess.run(["wmctrl", "-a", ":ACTIVE:"], 
                                          capture_output=True, text=True, check=True)
                    return result.stdout.strip()
                except (subprocess.SubprocessError, FileNotFoundError):
                    print("Error getting active application on Linux")
                    return None
        
        return None
    
    @staticmethod
    def is_allowed_application(allowed_apps: list[str]) -> bool:
        """
        Check if the currently active application is in the allowed list.
        
        Args:
            allowed_apps (list[str]): List of allowed application names.
            
        Returns:
            bool: True if the active application is in the allowed list, False otherwise.
        """
        active_app = ApplicationMonitor.get_active_application()
        print(f"Active application detected: {active_app}")
        
        if active_app is None:
            print("Could not determine active application, defaulting to not allowed")
            return False
            
        # Check if any of the allowed apps is contained in the active app name
        # This is more flexible than exact matching
        return any(allowed_app.lower() in active_app.lower() for allowed_app in allowed_apps)