import http.server
import socketserver
import os
import sys

DIRECTORY = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(DIRECTORY)

# Load configuration from .env if present (zero third-party dependencies)
env_path = os.path.join(PROJECT_ROOT, ".env")
if os.path.exists(env_path):
    try:
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, val = line.split("=", 1)
                    os.environ.setdefault(key.strip(), val.strip())
    except Exception:
        pass

PORT = int(os.environ.get("PORT", 8080))
HOST = os.environ.get("HOST", "")

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        # Serve raw dataset directly if requested
        if self.path.startswith("/data/raw/"):
            rel_path = self.path.lstrip("/")
            file_path = os.path.join(PROJECT_ROOT, rel_path)
            if os.path.exists(file_path):
                self.send_response(200)
                if file_path.endswith(".csv"):
                    self.send_header("Content-Type", "text/csv; charset=utf-8")
                elif file_path.endswith(".json"):
                    self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                with open(file_path, "rb") as f:
                    self.wfile.write(f.read())
                return

        # Fallback to standard handler for web/ static assets
        return super().do_GET()

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()

if __name__ == "__main__":
    os.chdir(DIRECTORY)
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
        print(f"Server started at http://localhost:{PORT}")
        sys.stdout.flush()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")
