import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Bot Shopee is running safely on Render!")

def run_server():
    # Render sẽ cấp tự động một biến môi trường PORT cho ứng dụng (Web Service).
    # Chúng ta phải bind và lắng nghe port này trong vòng 60 giây, nếu không Render sẽ báo lỗi deploy.
    port = int(os.environ.get("PORT", 8080))
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f"[KeepAlive] Bật Web Server phụ để báo danh với Render tại port {port}")
    httpd.serve_forever()

def keep_alive():
    """Khởi chạy máy chủ ảo trong một luồng riêng biệt để chạy song song với Bot Telegram"""
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
