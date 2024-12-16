import random
from Crypto.Util.number import getPrime, inverse, bytes_to_long, long_to_bytes
from sympy import isprime, mod_inverse, primitive_root





p = 48255049447579953872723127434597408212016751651937128914271692923
print("p = ", p)

alpha = primitive_root(p)
print("alpha: ", alpha)


a = 12
print("a: ", a)

beta = pow(alpha, a, p)
print("Giá trị β: ", beta)

def text_to_int(text):
    return int.from_bytes(text.encode(), 'big')

def encrypt(p, alpha, beta, x, k):
    a = pow(alpha, k, p)
    b = (x * pow(beta, k, p)) % p
    return a, b

name = "Nguyen Thi Huyen Thuong"
x = text_to_int(name)
print("x: ", x)

k = 3
print("k: ", k)

ciphertext = encrypt(p, alpha, beta, x, k)
print(f"Bản mã: {ciphertext}")



def decrypt(p, a, b, secret_key):
    s = pow(a, secret_key, p)
    plaintext = (b * mod_inverse(s, p)) % p
    return plaintext

decrypted_text = decrypt(p, ciphertext[0], ciphertext[1], a)
decrypted_name = decrypted_text.to_bytes((decrypted_text.bit_length() + 7) // 8, 'big').decode()
print("kết quả sau khi giải mã: ", decrypted_text, " - ", decrypted_name)