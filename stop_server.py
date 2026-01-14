"""Stop server running on port 8000"""
import subprocess
import sys
import os

def stop_server_on_port(port=8000):
    """Stop any process using the specified port."""
    try:
        # Find process using port 8000
        result = subprocess.run(
            ['netstat', '-ano'],
            capture_output=True,
            text=True,
            shell=True
        )
        
        pid = None
        for line in result.stdout.split('\n'):
            if f':{port}' in line and 'LISTENING' in line:
                parts = line.split()
                if len(parts) >= 5:
                    pid = parts[-1]
                    break
        
        if pid:
            print(f"Found process {pid} using port {port}")
            print(f"Attempting to stop process {pid}...")
            
            # Kill the process
            subprocess.run(['taskkill', '/PID', pid, '/F'], shell=True)
            print(f"Process {pid} stopped.")
            return True
        else:
            print(f"No process found listening on port {port}")
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Stopping server on port 8000...")
    print("=" * 60)
    
    if stop_server_on_port(8000):
        print("\n[OK] Server stopped successfully!")
    else:
        print("\n[INFO] No server found running on port 8000")
    
    print("\nYou can now start the server with:")
    print("  uvicorn app.main:app --reload")
