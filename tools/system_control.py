import subprocess
import shlex
import time
import pyautogui
import psutil
from typing import List, Dict, Optional
from pathlib import Path
from core.logger import logger
from commands.ai_chat import GeminiClient

class SystemController:
    """Control Windows system operations."""
    
    def __init__(self):
        # Initialize Gemini AI client
        self.gemini_client = GeminiClient()
    
    def open_application_dynamic(self, user_task: str) -> Dict[str, str]:
        """Dynamically generate and execute shell command to open application."""
        shell_command = self.generate_shell_command_suggestions(user_task)
        if shell_command == "N/A":
            return {'success': False, 'message': 'No valid shell command found for this request.'}
        result = self.execute_shell_command(shell_command)
        return {'success': True, 'message': result, 'command': shell_command}
    
    def generate_shell_command_suggestions(self, user_task: str) -> str:
        prompt = (
            "You are a helpful assistant that suggests Windows command-line (CMD/PowerShell) commands.\n"
            "Given a user's task description, provide ONLY the exact shell command(s) needed.\n"
            "NO explanatory text, markdown, or extra output.\n"
            f"User task: {user_task}\nCommand:"
        )
        return self.gemini_client.generate_text(prompt).strip()
    
    def execute_shell_command(self, command: str) -> str:
        try:
            cmd_parts = shlex.split(command)
            result = subprocess.run(cmd_parts, capture_output=True, text=True, check=False)
            if result.returncode == 0:
                return result.stdout.strip() or "Command executed successfully (no output)."
            else:
                return (f"Error:\n{result.stderr.strip()}\nOutput:\n{result.stdout.strip()}")
        except Exception as e:
            return f"Error: {str(e)}"
    
    def open_website(self, url: str) -> Dict[str, str]:
        try:
            os.startfile(url)
            logger.info(f"Opened website: {url}")
            return {'success': True,'message': f"Opened {url} in browser",'url': url}
        except Exception as e:
            logger.error(f"Error opening website: {e}")
            return {'success': False,'message': f"Error: {str(e)}",'url': url}
    
    def create_folder(self, path: str) -> Dict[str, str]:
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
            logger.info(f"Created folder: {path}")
            return {'success': True,'message': f"Created folder: {path}", 'path': path}
        except Exception as e:
            logger.error(f"Error creating folder: {e}")
            return {'success': False,'message': f"Error: {str(e)}",'path': path}
    
    def create_file(self, path: str, content: str = "") -> Dict[str, str]:
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"Created file: {path}")
            return {'success': True,'message': f"Created file: {path}",'path': path}
        except Exception as e:
            logger.error(f"Error creating file: {e}")
            return {'success': False,'message': f"Error: {str(e)}",'path': path}
    
    def set_volume(self, level: int) -> Dict[str, str]:
        try:
            level = max(0, min(100, level))
            volume_value = int(65535 * (level / 100))
            logger.info(f"Setting volume to {level}%")
            return {'success': True,'message': f"Volume set to {level}%",'level': level}
        except Exception as e:
            logger.error(f"Error setting volume: {e}")
            return {'success': False,'message': f"Error: {str(e)}",'level': level}
    
    def take_screenshot(self, save_path: Optional[str] = None) -> Dict[str, str]:
        try:
            if not save_path:
                save_path = f"screenshot_{int(time.time())}.png"
            screenshot = pyautogui.screenshot()
            screenshot.save(save_path)
            logger.info(f"Screenshot saved: {save_path}")
            return {'success': True,'message': f"Screenshot saved to {save_path}",'path': save_path}
        except Exception as e:
            logger.error(f"Error taking screenshot: {e}")
            return {'success': False,'message': f"Error: {str(e)}",'path': save_path or "unknown"}
    
    def get_running_processes(self) -> List[str]:
        try:
            processes = [proc.name() for proc in psutil.process_iter(['name'])]
            return list(set(processes))[:50]
        except Exception as e:
            logger.error(f"Error getting processes: {e}")
            return []
    
    def kill_process(self, process_name: str) -> Dict[str, str]:
        try:
            killed = False
            for proc in psutil.process_iter(['name']):
                if proc.info['name'].lower() == process_name.lower():
                    proc.kill()
                    killed = True
            if killed:
                logger.info(f"Killed process: {process_name}")
                return {'success': True,'message': f"Killed {process_name}",'process': process_name}
            else:
                return {'success': False,'message': f"Process {process_name} not found",'process': process_name}
        except Exception as e:
            logger.error(f"Error killing process: {e}")
            return {'success': False,'message': f"Error: {str(e)}",'process': process_name}

system_controller = SystemController()
