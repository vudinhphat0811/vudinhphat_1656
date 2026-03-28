import sys
import socket
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad

from ui.client import Ui_MainWindow

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

class ReceiveThread(QThread):
    message_received = pyqtSignal(str)

    def __init__(self, sock, aes_key):
        super().__init__()
        self.sock = sock
        self.aes_key = aes_key
        self.running = True

    def run(self):
        while self.running:
            try:
                encrypted_message = self.sock.recv(1024)
                if not encrypted_message:
                    break
                decrypted_message = decrypt_message(self.aes_key, encrypted_message)
                self.message_received.emit(f"Người lạ: {decrypted_message}")
            except:
                break

class ClientApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Secure Chat - Client")

        self.client_socket = None
        self.aes_key = None
        self.receive_thread = None

        self.btn_connect.clicked.connect(self.connect_to_server)
        self.txt_send.clicked.connect(self.send_message) 
        self.txt_send.setEnabled(False)

    def connect_to_server(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect(('localhost', 12345))

            client_key = RSA.generate(2048)
            server_public_key = RSA.import_key(self.client_socket.recv(2048))
            self.client_socket.send(client_key.publickey().export_key(format='PEM'))
            
            encrypted_aes_key = self.client_socket.recv(2048)
            cipher_rsa = PKCS1_OAEP.new(client_key)
            self.aes_key = cipher_rsa.decrypt(encrypted_aes_key)
            
            self.update_history("Hệ thống: Đã kết nối tới Server!")
            self.btn_connect.setEnabled(False)
            self.txt_send.setEnabled(True)

            self.receive_thread = ReceiveThread(self.client_socket, self.aes_key)
            self.receive_thread.message_received.connect(self.update_history)
            self.receive_thread.start()
        except Exception as e:
            self.update_history(f"Hệ thống: Lỗi kết nối ({e})")

    def send_message(self):
        message = self.txt_chat.toPlainText().strip() 
        if message and self.aes_key:
            try:
                encrypted_message = encrypt_message(self.aes_key, message)
                self.client_socket.send(encrypted_message)
                self.update_history(f"Bạn: {message}")
                self.txt_chat.clear() 
            except Exception as e:
                self.update_history(f"Lỗi gửi tin: {e}")

    def update_history(self, message):
        self.txt_history.append(message)

    def closeEvent(self, event):
        if self.receive_thread:
            self.receive_thread.running = False
        if self.client_socket:
            self.client_socket.close()
        event.accept()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ClientApp()
    window.show()
    sys.exit(app.exec_())