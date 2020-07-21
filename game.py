
import pyautogui
import socket
import json

class Game():

    def __init__(self , host , port):
        self.host = host  # The server's hostname or IP address
        self.port = port

    def get_game_info(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            data = s.recv(1024)
            info = json.loads(data.decode('ISO-8859-1')[2:])
        
        return info

    def press_key(self , key):
        pyautogui.press(key , interval=0.1)

    def press_key_down(self , key):
        pyautogui.keyDown(key)
        pyautogui.keyUp(key)