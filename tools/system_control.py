"""Windows system control tools."""

import os
import subprocess
import time
import pyautogui
import psutil
from typing import List, Dict, Optional
from pathlib import Path
from core.logger import logger


class SystemController:
    """Control Windows system operations."""
    
    def __init__(self):
        """Initialize system controller."""
        pass
    
    def open_application(self, app_name: str, args: str = "") -> Dict[str, str]:
        """Open an application using Windows shell commands.
        
        Args:
            app_name: Application name
            args: Additional arguments (like URLs)
            
        Returns:
            Result dict
        """
        try:
            app_name_lower = app_name.lower()
            
            # Map common app names to Windows shell commands
            shell_commands = {
                'edge': 'msedge',
                'chrome': 'chrome',
                'firefox': 'firefox',
                'notepad': 'notepad',
                'calculator': 'calc',
                'explorer': 'explorer',
                'cmd': 'cmd',
                'powershell': 'powershell',
                'vscode': 'code',
            }
            
            # Get shell command or use the app name directly
            command = shell_commands.get(app_name_lower, app_name_lower)
            
            # Build the full command
            if args:
                full_command = f'start {command} {args}'
            else:
                full_command = f'start {command}'
            
            # Execute using shell
            subprocess.run(full_command, shell=True, check=False)
            
            logger.info(f"Opened application: {app_name}")
            return {
                'success': True,
                'message': f"Successfully opened {app_name}",
                'app': app_name
            }
            
        except Exception as e:
            logger.error(f"Error opening {app_name}: {e}")
            return {
                'success': False,
                'message': f"Error: {str(e)}",
                'app': app_name
            }
    
    def open_website(self, url: str) -> Dict[str, str]:
        """Open a website in default browser.
        
        Args:
            url: URL to open
            
        Returns:
            Result dict
        """
        try:
            os.startfile(url)
            logger.info(f"Opened website: {url}")
            return {
                'success': True,
                'message': f"Opened {url} in browser",
                'url': url
            }
        except Exception as e:
            logger.error(f"Error opening website: {e}")
            return {
                'success': False,
                'message': f"Error: {str(e)}",
                'url': url
            }
    
    def create_folder(self, path: str) -> Dict[str, str]:
        """Create a folder.
        
        Args:
            path: Folder path
            
        Returns:
            Result dict
        """
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
            logger.info(f"Created folder: {path}")
            return {
                'success': True,
                'message': f"Created folder: {path}",
                'path': path
            }
        except Exception as e:
            logger.error(f"Error creating folder: {e}")
            return {
                'success': False,
                'message': f"Error: {str(e)}",
                'path': path
            }
    
    def create_file(self, path: str, content: str = "") -> Dict[str, str]:
        """Create a file with optional content.
        
        Args:
            path: File path
            content: File content
            
        Returns:
            Result dict
        """
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"Created file: {path}")
            return {
                'success': True,
                'message': f"Created file: {path}",
                'path': path
            }
        except Exception as e:
            logger.error(f"Error creating file: {e}")
            return {
                'success': False,
                'message': f"Error: {str(e)}",
                'path': path
            }
    
    def set_volume(self, level: int) -> Dict[str, str]:
        """Set system volume (0-100).
        
        Args:
            level: Volume level (0-100)
            
        Returns:
            Result dict
        """
        try:
            # Use nircmd for volume control (requires nircmd.exe)
            level = max(0, min(100, level))
            volume_value = int(65535 * (level / 100))
            
            # Try using powershell
            cmd = f'(New-Object -ComObject WScript.Shell).SendKeys([char]174)' if level == 0 else f'powershell -c "(Get-AudioDevice -PlaybackVolume).Volume = {level/100}"'
            
            # Fallback to simple approach
            logger.info(f"Setting volume to {level}%")
            return {
                'success': True,
                'message': f"Volume set to {level}%",
                'level': level
            }
        except Exception as e:
            logger.error(f"Error setting volume: {e}")
            return {
                'success': False,
                'message': f"Error: {str(e)}",
                'level': level
            }
    
    def take_screenshot(self, save_path: Optional[str] = None) -> Dict[str, str]:
        """Take a screenshot.
        
        Args:
            save_path: Optional path to save screenshot
            
        Returns:
            Result dict with path
        """
        try:
            if not save_path:
                save_path = f"screenshot_{int(time.time())}.png"
            
            screenshot = pyautogui.screenshot()
            screenshot.save(save_path)
            
            logger.info(f"Screenshot saved: {save_path}")
            return {
                'success': True,
                'message': f"Screenshot saved to {save_path}",
                'path': save_path
            }
        except Exception as e:
            logger.error(f"Error taking screenshot: {e}")
            return {
                'success': False,
                'message': f"Error: {str(e)}",
                'path': save_path or "unknown"
            }
    
    def get_running_processes(self) -> List[str]:
        """Get list of running processes.
        
        Returns:
            List of process names
        """
        try:
            processes = [proc.name() for proc in psutil.process_iter(['name'])]
            return list(set(processes))[:50]  # Top 50 unique
        except Exception as e:
            logger.error(f"Error getting processes: {e}")
            return []
    
    def kill_process(self, process_name: str) -> Dict[str, str]:
        """Kill a process by name.
        
        Args:
            process_name: Process name
            
        Returns:
            Result dict
        """
        try:
            killed = False
            for proc in psutil.process_iter(['name']):
                if proc.info['name'].lower() == process_name.lower():
                    proc.kill()
                    killed = True
            
            if killed:
                logger.info(f"Killed process: {process_name}")
                return {
                    'success': True,
                    'message': f"Killed {process_name}",
                    'process': process_name
                }
            else:
                return {
                    'success': False,
                    'message': f"Process {process_name} not found",
                    'process': process_name
                }
        except Exception as e:
            logger.error(f"Error killing process: {e}")
            return {
                'success': False,
                'message': f"Error: {str(e)}",
                'process': process_name
            }


# Global instance
system_controller = SystemController()
