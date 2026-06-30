import subprocess
import os
import time
import http.server
import socketserver
import threading
from PIL import Image

# Custom request handler to suppress output log messages
class SilentHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

def run_server(httpd):
    print("Local HTTP server started on port 8000...")
    httpd.serve_forever()

def generate_assets():
    # 1. Start a temporary local HTTP server in a background thread
    PORT = 8000
    # Allow address reuse in socket
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(("", PORT), SilentHTTPRequestHandler)
    
    server_thread = threading.Thread(target=run_server, args=(httpd,))
    server_thread.daemon = True
    server_thread.start()
    
    time.sleep(1) # Wait for server to bind and listen
    
    # 2. Setup screenshot configurations
    pages = [
        ('page-industry', 'page1.png'),
        ('page-performance', 'page2.png'),
        ('page-investors', 'page3.png'),
        ('page-trends', 'page4.png')
    ]
    
    # Locate Chrome on system
    chrome_path = "C:\\Program Files\\Google\Chrome\\Application\\chrome.exe"
    if not os.path.exists(chrome_path):
        chrome_path = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
        
    print(f"Using Chrome path: {chrome_path}")
    
    # Get absolute path for workspace directory
    workspace_dir = os.path.abspath(os.getcwd())
    
    screenshots = []
    for page, filename in pages:
        # Construct absolute screenshot output path
        output_path = os.path.join(workspace_dir, filename)
        url = f"http://localhost:8000/dashboard/index.html?page={page}"
        print(f"Capturing {page} from {url}...")
        
        cmd = [
            chrome_path,
            "--headless=new",
            "--disable-gpu",
            "--window-size=1600,900",
            "--hide-scrollbars",
            f"--screenshot={output_path}",
            url
        ]
        
        # Run process
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Verify if the file was actually created
        if os.path.exists(output_path):
            print(f"Captured {filename} successfully to {output_path}.")
            screenshots.append(output_path)
        else:
            print(f"Error capturing {page}. Chrome output: {result.stdout} | {result.stderr}")
            
        time.sleep(1.5) # Short sleep to let the system finish rendering and writing
        
    # 3. Shutdown local HTTP server
    print("Shutting down local HTTP server...")
    httpd.shutdown()
    httpd.server_close()
    
    # 4. Compile images into a premium landscape PDF report
    if len(screenshots) == 4:
        print("Compiling images into Dashboard.pdf...")
        try:
            pdf_path = os.path.join(workspace_dir, 'Dashboard.pdf')
            img1 = Image.open(screenshots[0]).convert('RGB')
            img2 = Image.open(screenshots[1]).convert('RGB')
            img3 = Image.open(screenshots[2]).convert('RGB')
            img4 = Image.open(screenshots[3]).convert('RGB')
            
            img1.save(pdf_path, format="PDF", save_all=True, append_images=[img2, img3, img4])
            print(f"Dashboard.pdf created successfully at {pdf_path}.")
        except Exception as e:
            print(f"Error compiling PDF: {e}")
    else:
        print(f"Failed to capture all pages (Captured: {len(screenshots)}/4). PDF compilation skipped.")

if __name__ == '__main__':
    generate_assets()
