# server.py
from http.server import HTTPServer, BaseHTTPRequestHandler
import socketserver
from datetime import datetime
import os
import json
import requests
from email.utils import formatdate

PORT = 8000
LOG_FILE = "access.log"
DISCORD_WEBHOOK = ("https://discord.com/api/webhooks/1462609347061350504/HfLF6sVXs0YVwHKR7u0MI872H3iwuaGYzJfYtmlNbdk7sUqtKnhMEWQwxChA1_G3pbbX")  # Add your Discord webhook URL here
PIXEL_PATH = "/tracking_pixel.gif"
PIXEL_DATA = b'data:image/jpeg;base64,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;'

class TrackingHandler(BaseHTTPRequestHandler):
    def log_access(self):
        client_ip = self.client_address[0]
        user_agent = self.headers.get('User-Agent', 'Unknown')
        referer = self.headers.get('Referer', 'Direct')
        timestamp = formatdate(timeval=None, localtime=True, usegmt=True)
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'ip': client_ip,
            'user_agent': user_agent,
            'method': self.command,
            'path': self.path,
            'referer': referer
        }
        
        print(f"[{timestamp}] {client_ip} - {user_agent[:50]}...")
        
        with open(LOG_FILE, "a") as log:
            log.write(json.dumps(log_entry) + "\n")
        
        if PIXEL_PATH in self.path and DISCORD_WEBHOOK:
            self.send_discord_alert(client_ip, user_agent, referer)
    
    def send_discord_alert(self, ip, ua, referer):
        embed = {
            "title": "📌 Tracking Pixel Triggered!",
            "color": 5814783,
            "fields": [
                {"name": "Visitor IP", "value": ip, "inline": True},
                {"name": "User Agent", "value": f"```{ua[:1000]}```", "inline": False},
                {"name": "Referer", "value": referer, "inline": True}
            ],
            "footer": {"text": f"Logged at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"}
        }
        
        try:
            requests.post(DISCORD_WEBHOOK, json={"embeds": [embed]}, timeout=5)
        except Exception as e:
            print(f"Discord notification failed: {e}")
    
    def do_GET(self):
        self.log_access()
        
        if self.path == PIXEL_PATH:
            self.send_response(200)
            self.send_header('Content-type', 'image/gif')
            self.send_header('Cache-Control', 'no-store, must-revalidate')
            self.send_header('Expires', '0')
            self.end_headers()
            self.wfile.write(PIXEL_DATA)
            return
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Tracking Server</title>
            <style>
                body {{ font-family: sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
                .container {{ background: #f8f9fa; padding: 30px; border-radius: 10px; }}
                .info {{ background: white; padding: 15px; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🛜 HTTP Tracking Server</h1>
                <div class="info">
                    <p>✅ Server is operational</p>
                    <p>🕒 Time: {datetime.now().strftime('%c')}</p>
                    <p>📍 Your IP: {self.client_address[0]}</p>
                    <p>🖥️ User Agent: {self.headers.get('User-Agent', 'Unknown')[:80]}</p>
                </div>
                <p>This page contains a tracking pixel that logs accesses.</p>
                <img src="{PIXEL_PATH}" alt="tracking pixel">
            </div>
        </body>
        </html>
        """
        self.wfile.write(html_content.encode('utf-8'))

if __name__ == "__main__":
    print(f"🚀 Starting tracking server on port {PORT}")
    print(f"📝 Access log: {os.path.abspath(LOG_FILE)}")
    print(f"📌 Tracking pixel URL: http://localhost:{PORT}{PIXEL_PATH}")
    print("🛑 Press CTRL+C to stop the server")
    
    with HTTPServer(("", PORT), TrackingHandler) as server:
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped by user")
