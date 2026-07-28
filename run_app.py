import subprocess
import webbrowser
import time
import sys
import os

def main():
    print("Starting BIS LIS Compliance Lookup System...")
    
    # Get the absolute path of the project root
    project_root = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(project_root, "backend")
    frontend_dir = os.path.join(project_root, "frontend")
    
    # Path to virtual env python/uvicorn
    venv_uvicorn = os.path.join(project_root, ".venv", "bin", "uvicorn")
    if not os.path.exists(venv_uvicorn):
        # Fallback to system uvicorn
        venv_uvicorn = "uvicorn"
        
    print(f"Project root: {project_root}")
    print(f"Starting backend from: {backend_dir}")
    print(f"Starting frontend from: {frontend_dir}")
    
    # 1. Start Backend FastAPI Server from 'backend' directory
    backend = subprocess.Popen(
        [venv_uvicorn, "api.index:app", "--host", "127.0.0.1", "--port", "8000"],
        cwd=backend_dir,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    # 2. Start Frontend Static Server from 'frontend' directory
    frontend = subprocess.Popen(
        [sys.executable, "-m", "http.server", "3000"],
        cwd=frontend_dir,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    # 3. Give servers a brief moment to boot
    time.sleep(1.5)
    
    # 4. Launch login screen
    login_url = "http://localhost:3000/src/pages/login.html"
    print(f"Launching web interface at: {login_url}")
    webbrowser.open(login_url)
    
    print("\n--- System Status: RUNNING ---")
    print("Press Ctrl+C in this terminal window to stop the servers.")
    
    try:
        # Keep main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        backend.terminate()
        frontend.terminate()
        backend.wait()
        frontend.wait()
        print("System stopped.")

if __name__ == "__main__":
    main()
