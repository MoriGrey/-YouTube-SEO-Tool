"""
Process Manager for Continuous Learning
Manages the continuous learning process as a separate Python process.
"""

import os
import sys
import subprocess
import json
import psutil
from pathlib import Path
from typing import Optional, Dict, Any

PROCESS_LOCK_FILE = "data/continuous_learning_process.json"


class ProcessManager:
    """Manages continuous learning as a separate process."""
    
    def __init__(self):
        self._ensure_data_dir()
    
    def _ensure_data_dir(self):
        """Ensure data directory exists."""
        os.makedirs(os.path.dirname(PROCESS_LOCK_FILE), exist_ok=True)
    
    def _load_process_info(self) -> Optional[Dict[str, Any]]:
        """Load process information from lock file."""
        if os.path.exists(PROCESS_LOCK_FILE):
            try:
                with open(PROCESS_LOCK_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return None
    
    def _save_process_info(self, pid: int, channel_handle: str):
        """Save process information to lock file."""
        info = {
            "pid": pid,
            "channel_handle": channel_handle,
            "started_at": str(Path(__file__).parent.parent.parent / "start_continuous_learning.py")
        }
        try:
            with open(PROCESS_LOCK_FILE, 'w', encoding='utf-8') as f:
                json.dump(info, f, indent=2)
        except Exception as e:
            print(f"Error saving process info: {e}")
    
    def _delete_process_info(self):
        """Delete process information file."""
        if os.path.exists(PROCESS_LOCK_FILE):
            try:
                os.remove(PROCESS_LOCK_FILE)
            except Exception:
                pass
    
    def is_process_running(self) -> bool:
        """Check if continuous learning process is running."""
        info = self._load_process_info()
        if not info:
            return False
        
        pid = info.get("pid")
        if not pid:
            return False
        
        try:
            # Check if process exists
            process = psutil.Process(pid)
            # Check if it's still the same process (not reused PID)
            if process.is_running():
                # Verify it's our script
                cmdline = process.cmdline()
                if any("start_continuous_learning.py" in str(arg) for arg in cmdline):
                    return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # Process doesn't exist or we can't access it
            self._delete_process_info()
            return False
        
        return False
    
    def start_process(self, channel_handle: str) -> Dict[str, Any]:
        """
        Start continuous learning as a separate process.
        
        Args:
            channel_handle: Channel to monitor
            
        Returns:
            Status dictionary
        """
        # Check if already running
        if self.is_process_running():
            return {
                "status": "already_running",
                "message": "Continuous learning process is already running"
            }
        
        # Get script path
        script_path = Path(__file__).parent.parent.parent / "start_continuous_learning.py"
        
        if not script_path.exists():
            return {
                "status": "error",
                "message": f"Script not found: {script_path}"
            }
        
        try:
            # Set environment variable for channel handle
            env = os.environ.copy()
            env["TARGET_CHANNEL_HANDLE"] = channel_handle
            
            # Start process
            if sys.platform == "win32":
                # Windows: use CREATE_NEW_PROCESS_GROUP to allow proper termination
                process = subprocess.Popen(
                    [sys.executable, str(script_path)],
                    env=env,
                    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            else:
                # Unix-like systems
                process = subprocess.Popen(
                    [sys.executable, str(script_path)],
                    env=env,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    start_new_session=True
                )
            
            # Save process info
            self._save_process_info(process.pid, channel_handle)
            
            return {
                "status": "started",
                "message": "Continuous learning process started",
                "pid": process.pid,
                "channel_handle": channel_handle
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to start process: {str(e)}"
            }
    
    def stop_process(self) -> Dict[str, Any]:
        """
        Stop the continuous learning process.
        
        Returns:
            Status dictionary
        """
        info = self._load_process_info()
        if not info:
            return {
                "status": "not_running",
                "message": "No continuous learning process found"
            }
        
        pid = info.get("pid")
        if not pid:
            self._delete_process_info()
            return {
                "status": "not_running",
                "message": "No process ID found"
            }
        
        try:
            process = psutil.Process(pid)
            
            # Terminate process and its children
            try:
                # Try graceful termination first
                if sys.platform == "win32":
                    # Windows: terminate the process
                    process.terminate()
                else:
                    process.terminate()
                
                # Wait for process to terminate
                try:
                    process.wait(timeout=5)
                except psutil.TimeoutExpired:
                    # Force kill if it doesn't terminate
                    process.kill()
                    process.wait(timeout=2)
            except psutil.NoSuchProcess:
                # Process already terminated
                pass
            
            self._delete_process_info()
            
            return {
                "status": "stopped",
                "message": "Continuous learning process stopped successfully"
            }
            
        except psutil.NoSuchProcess:
            # Process doesn't exist
            self._delete_process_info()
            return {
                "status": "not_running",
                "message": "Process was not running"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error stopping process: {str(e)}"
            }
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get current process status.
        
        Returns:
            Status dictionary
        """
        info = self._load_process_info()
        is_running = self.is_process_running()
        
        if not info:
            return {
                "running": False,
                "pid": None,
                "channel_handle": None,
                "message": "No process information found"
            }
        
        return {
            "running": is_running,
            "pid": info.get("pid") if is_running else None,
            "channel_handle": info.get("channel_handle"),
            "message": "Process is running" if is_running else "Process is not running"
        }

