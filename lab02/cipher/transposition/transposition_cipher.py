class TranspositionCipher:
    def __init__(self):
        pass

    def encrypt(self, text, key):
        encrypted_text = ''
        for col in range(key):
            pointer = col
            while pointer < len(text):
                encrypted_text += text[pointer]
                pointer += key
        return encrypted_text
    
    def decrypt(self, text, key):
        length = len(text)
        num_rows = (length + key - 1) // key
        full_cols = length % key

        if full_cols == 0: full_cols = key
        res = [''] * num_rows
        idx = 0 

        for c in range(key):
            col_len = num_rows if c < full_cols else num_rows - 1
            for r in range(col_len):
                res[r] += text[idx]
                idx += 1       
        return "".join(res)
