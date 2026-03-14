from flask import Flask, render_template, request
from cipher.caesar import CaesarCipher
from cipher.vigenere import VigenereCipher
from cipher.railfence.railfence_cipher import RailFenceCipher
from cipher.playfair.playfair_cipher import PlayfairCipher
from cipher.transposition.transposition_cipher import TranspositionCipher

app = Flask(__name__)

@app.route("/")
def home(): return render_template('index.html')

@app.route("/caesar")
def caesar(): return render_template('caesar.html')

@app.route("/vigenere")
def vigenere(): return render_template('vigenere.html')

@app.route("/railfence")
def railfence(): return render_template('railfence.html')

@app.route("/playfair")
def playfair(): return render_template('playfair.html')

@app.route("/transposition")
def transposition(): return render_template('transposition.html')


#CAESAR
@app.route("/encrypt", methods=['POST'])
def caesar_encrypt():
    text = request.form['inputPlainText']; key = int(request.form['inputKeyPlain'])
    res = CaesarCipher().encrypt_text(text, key)
    return render_template('caesar.html', res_en=res, old_txt_en=text, old_key_en=key)

@app.route("/decrypt", methods=['POST'])
def caesar_decrypt():
    text = request.form['inputCipherText']; key = int(request.form['inputKeyCipher'])
    res = CaesarCipher().decrypt_text(text, key)
    return render_template('caesar.html', res_de=res, old_txt_de=text, old_key_de=key)

#VIGENERE
@app.route("/vigenere_encrypt", methods=['POST'])
def vigenere_encrypt():
    text = request.form['inputPlainText']; key = request.form['inputKeyPlain']
    res = VigenereCipher().vigenere_encrypt(text, key)
    return render_template('vigenere.html', res_en=res, old_txt_en=text, old_key_en=key)

@app.route("/vigenere_decrypt", methods=['POST'])
def vigenere_decrypt():
    text = request.form['inputCipherText']; key = request.form['inputKeyCipher']
    res = VigenereCipher().vigenere_decrypt(text, key)
    return render_template('vigenere.html', res_de=res, old_txt_de=text, old_key_de=key)


#RAIL FENCE
@app.route("/railfence_encrypt", methods=['POST'])
def railfence_encrypt():
    text = request.form['inputPlainText']; key = int(request.form['inputKeyPlain'])
    res = RailFenceCipher().rail_fence_encrypt(text, key)
    return render_template('railfence.html', res_en=res, old_txt_en=text, old_key_en=key)

@app.route("/railfence_decrypt", methods=['POST'])
def railfence_decrypt():
    text = request.form['inputCipherText']; key = int(request.form['inputKeyCipher'])
    res = RailFenceCipher().rail_fence_decrypt(text, key)
    return render_template('railfence.html', res_de=res, old_txt_de=text, old_key_de=key)


#PLAYFAIR
@app.route("/playfair_encrypt", methods=['POST'])
def playfair_encrypt():
    text = request.form['inputPlainText']; key = request.form['inputKeyPlain']
    cipher = PlayfairCipher()
    res = cipher.playfair_encrypt(text, cipher.create_playfair_matrix(key))
    return render_template('playfair.html', res_en=res, old_txt_en=text, old_key_en=key)

@app.route("/playfair_decrypt", methods=['POST'])
def playfair_decrypt():
    text = request.form['inputCipherText']; key = request.form['inputKeyCipher']
    cipher = PlayfairCipher()
    res = cipher.playfair_decrypt(text, cipher.create_playfair_matrix(key))
    return render_template('playfair.html', res_de=res, old_txt_de=text, old_key_de=key)

@app.route("/playfair_matrix", methods=['POST'])
def playfair_matrix():
    key = request.form.get('inputKeyPlain')
    matrix = PlayfairCipher().create_playfair_matrix(key)
    matrix_str = "".join([" &nbsp; ".join(row) + "<br/>" for row in matrix])
    return render_template('playfair.html', matrix_str=matrix_str, old_key_en=key)


#TRANSPOSITION
@app.route("/transposition_encrypt", methods=['POST'])
def transposition_encrypt():
    text = request.form['inputPlainText']; key = int(request.form['inputKeyPlain'])
    res = TranspositionCipher().encrypt(text, key)
    return render_template('transposition.html', res_en=res, old_txt_en=text, old_key_en=key)

@app.route("/transposition_decrypt", methods=['POST'])
def transposition_decrypt():
    text = request.form['inputCipherText']; key = int(request.form['inputKeyCipher'])
    res = TranspositionCipher().decrypt(text, key)
    return render_template('transposition.html', res_de=res, old_txt_de=text, old_key_de=key)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)