import sys
import socket
import threading
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

from ui.server import Ui_MainWindow

def encrypt_message(key, message):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
    return cipher.iv + ciphertext

def decrypt_message(key, encrypted_message):
    iv = encrypted_message[:AES.block_size]
    ciphertext = encrypted_message[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_message = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted_message.decode()

class ServerThread(QThread):
    log_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_key = RSA.generate(2048)
        self.clients = []
        self.running = True

    def run(self):
        try:
            self.server_socket.bind(('localhost', 12345))
            self.server_socket.listen(5)
            self.log_signal.emit(" Server đang chạy tại localhost:12345...")
 
            while self.running:
                self.server_socket.settimeout(1.0)
                try:
                    client_socket, client_address = self.server_socket.accept()
                    client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
                    client_thread.start()
                except socket.timeout:
                    continue
                except Exception as e:
                    if self.running:
                        self.log_signal.emit(f"Lỗi: {e}")
        except Exception as e:
            self.log_signal.emit(f" Lỗi khởi động server: {e}")

    def handle_client(self, client_socket, client_address):
        addr_str = f"{client_address[0]}:{client_address[1]}"
        self.log_signal.emit(f"[+] Client {addr_str} đã kết nối.")

        try:
            client_socket.send(self.server_key.publickey().export_key(format='PEM'))
            client_received_key = RSA.import_key(client_socket.recv(2048))
            aes_key = get_random_bytes(16)
            cipher_rsa = PKCS1_OAEP.new(client_received_key)
            encrypted_aes_key = cipher_rsa.encrypt(aes_key)
            client_socket.send(encrypted_aes_key)

            self.clients.append((client_socket, aes_key))
            self.log_signal.emit(f"[*] Trao đổi khóa an toàn với {addr_str}.")

            while self.running:
                encrypted_message = client_socket.recv(1024)
                if not encrypted_message:
                    break
                self.log_signal.emit(f" [Mã hóa AES]: {encrypted_message}")
                decrypted_message = decrypt_message(aes_key, encrypted_message)
                self.log_signal.emit(f"[{addr_str}]: {decrypted_message}")

                for client, key in self.clients:
                    if client != client_socket:
                        encrypted = encrypt_message(key, decrypted_message)
                        client.send(encrypted)

        except Exception as e:
            pass
        finally:
            self.clients = [(c, k) for c, k in self.clients if c != client_socket]
            client_socket.close()
            self.log_signal.emit(f"[-] Client {addr_str} đã thoát.")

    def stop_server(self):
        self.running = False
        self.server_socket.close()

class ServerApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Secure Chat - Server")

        self.pushButton.clicked.connect(self.close)

        self.server_thread = ServerThread()
        self.server_thread.log_signal.connect(self.update_log)
        self.server_thread.start()

    def update_log(self, message):
        self.textEdit.append(message) 

    def closeEvent(self, event):
        self.server_thread.stop_server()
        self.server_thread.wait()
        event.accept()
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ServerApp()
    window.show()
    sys.exit(app.exec_())