from flask import Flask, render_template, request, json
from cipher.caesar import CaesarCipher
from cipher.vigenere import VigenereCipher
from cipher.railfence.railfence_cipher import RailFenceCipher
from cipher.playfair.playfair_cipher import PlayfairCipher
from cipher.transposition.transposition_cipher import TranspositionCipher
app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/caesar")
def caesar():
    return render_template('caesar.html')
@app.route("/vigenere")
def vigenere():
    return render_template('vigenere.html')

@app.route("/railfence")
def railfence():
    return render_template('railfence.html')

@app.route("/playfair")
def playfair():
    return render_template('playfair.html')

@app.route("/transposition")
def transposition():
    return render_template('transposition.html')
# Caesar Cipher
@app.route("/encrypt", methods=['POST'])
def caesar_encrypt():
    text = request.form['inputPlainText']
    key = int(request.form['inputKeyPlain'])
    Caesar = CaesarCipher()
    encrypted_text = Caesar.encrypt_text(text, key)
    return f"text: {text}<br/>key: {key}<br/>encrypted text: {encrypted_text}"

@app.route("/decrypt", methods=['POST'])
def caesar_decrypt():
    text = request.form['inputCipherText']
    key = int(request.form['inputKeyCipher'])
    Caesar = CaesarCipher()
    decrypted_text = Caesar.decrypt_text(text, key)
    return f"text: {text}<br/>key: {key}<br/>decrypted text: {decrypted_text}"

# Vigenere Cipher
@app.route("/vigenere_encrypt", methods=['POST'])
def vigenere_encrypt():
    text = request.form['inputPlainText']
    key = request.form['inputKeyPlain']
    cipher = VigenereCipher()
    res = cipher.vigenere_encrypt(text, key)
    return f"text: {text}<br/>key: {key}<br/>encrypted text: {res}"

@app.route("/vigenere_decrypt", methods=['POST'])
def vigenere_decrypt():
    text = request.form['inputCipherText']
    key = request.form['inputKeyCipher']
    cipher = VigenereCipher()
    res = cipher.vigenere_decrypt(text, key)
    return f"text: {text}<br/>key: {key}<br/>decrypted text: {res}"
# Rail Fence Cipher
@app.route("/railfence_encrypt", methods=['POST'])
def railfence_encrypt():
    text = request.form['inputPlainText']
    key = int(request.form['inputKeyPlain'])
    cipher = RailFenceCipher()
    res = cipher.rail_fence_encrypt(text, key)
    return f"text: {text}<br/>key: {key}<br/>encrypted text: {res}"

@app.route("/railfence_decrypt", methods=['POST'])
def railfence_decrypt():
    text = request.form['inputCipherText']
    key = int(request.form['inputKeyCipher'])
    cipher = RailFenceCipher()
    res = cipher.rail_fence_decrypt(text, key)
    return f"text: {text}<br/>key: {key}<br/>decrypted text: {res}"
# Playfair Cipher
@app.route("/playfair_encrypt", methods=['POST'])
def playfair_encrypt():
    text = request.form['inputPlainText']
    key = request.form['inputKeyPlain']
    cipher = PlayfairCipher()
    matrix = cipher.create_playfair_matrix(key)
    res = cipher.playfair_encrypt(text, matrix)
    return f"text: {text}<br/>key: {key}<br/>encrypted text: {res}"

@app.route("/playfair_decrypt", methods=['POST'])
def playfair_decrypt():
    text = request.form['inputCipherText']
    key = request.form['inputKeyCipher']
    cipher = PlayfairCipher()
    matrix = cipher.create_playfair_matrix(key)
    res = cipher.playfair_decrypt(text, matrix)
    return f"text: {text}<br/>key: {key}<br/>decrypted text: {res}"

@app.route("/playfair_matrix", methods=['POST'])
def playfair_matrix():
    key = request.form.get('inputKeyPlain') 
    cipher = PlayfairCipher()
    matrix = cipher.create_playfair_matrix(key)
    
    matrix_str = ""
    for row in matrix:
        matrix_str += " &nbsp; ".join(row) + "<br/>"
        
    return f"Key dùng để tạo bảng: {key}<br/><br/><b>Bảng Playfair 5x5:</b><br/>{matrix_str}"
# Transposition Cipher
@app.route("/transposition_encrypt", methods=['POST'])
def transposition_encrypt():
    text = request.form['inputPlainText']
    key = int(request.form['inputKeyPlain'])
    cipher = TranspositionCipher()
    res = cipher.encrypt(text, key)
    return f"text: {text}<br/>key: {key}<br/>encrypted text: {res}"

@app.route("/transposition_decrypt", methods=['POST'])
def transposition_decrypt():
    text = request.form['inputCipherText']
    key = int(request.form['inputKeyCipher'])
    cipher = TranspositionCipher()
    res = cipher.decrypt(text, key)
    return f"text: {text}<br/>key: {key}<br/>decrypted text: {res}"
#main function
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)