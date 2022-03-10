#! /usr/bin/env python3
import pyjoycon
from http.server import HTTPServer, BaseHTTPRequestHandler
import concurrent.futures

port = 8080

class GetJoyCon(BaseHTTPRequestHandler):
    def do_GET(self):

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        path = self.path
        if path == "/reset":
            joycon.reset_orientation()

        out = f"{{x: {joycon.rotation[0]},y: {joycon.rotation[1]},z: {joycon.rotation[2]}}}"
        self.wfile.write(bytes(out.encode('utf-8')))

class MyJoyCon(
        pyjoycon.GyroTrackingJoyCon,
        pyjoycon.ButtonEventJoyCon,
        pyjoycon.JoyCon
    ): pass

def webserver():
    # LED 点滅
    for _ in range(10):
        joycon._write_output_report(b'\x01', b'\x30', b'\xf0')
    webServer = HTTPServer(('', port), GetJoyCon)
    print("Server started.")
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    # LED 点灯
    for _ in range(10):
        joycon._write_output_report(b'\x01', b'\x30', b'\x0f')
    print("Server stopped.")
    exit(0)

def button_events():
    while True:
        for event_type, status in joycon.events():
            print(event_type, status)
            joycon.reset_orientation()

if __name__ == "__main__":
    joycon_id = pyjoycon.get_L_id()
    joycon = MyJoyCon(*joycon_id)

    executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
    executor.submit(webserver)
    executor.submit(button_events)
