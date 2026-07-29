import threading
import time
import webview
from server import run_server

t = threading.Thread(target=run_server)
t.daemon = True
t.start()

time.sleep(5)   

webview.create_window(
    "Accounting Software",
    "http://127.0.0.1:8000"
)

webview.start()