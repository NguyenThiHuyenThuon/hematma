from sympy import mod_inverse
from Crypto.Util.number import getPrime, inverse, bytes_to_long, long_to_bytes
# Define the elliptic curve parameters
a = 43
b = 454
p = 12117335770605158578213482751869252558756339185315245332376301981368004066948306933123294852213740979771812017189037709738028434579933062830669969836072223989621313794013558762195956329640844486937788745542898627962509787688201609609001073553989843389382018557644063757195695048524797946743995257767373066191206030092578872213246516667179526499258888265344210839363362932581081354548020537895533202068873274873969666505815663867167478025828716096377031984527487991624726883772829871131216935815562267011819624370411852831753242335746906347142142422638282732800653769824995246784157163286983803579633288709175185247164442066346233229019700344623056836000809915604823713506174482354236228820204764055809863853869497640504792413996412264074825949715128169789048303340305892448745240946147794032702247919241800970813740010091249431880243490257330175634307848086791637601897634775609905413547893401680140513906087167211558962391416928616041504019863765711489944437921848218877975924308255560678287673848532852610669242994550067929433799226567257399268885110417943689181365747371247226081922503162602094195549069151746770528238026363556273913183043894430488375357300328719308714778961625894077317666171431316753
print("a: ", a)
print("b: ", b)
print("p: ", p)
# Define the point P on the curve
def is_quadratic_residue(n, p):
    return pow(n, (p - 1) // 2, p) == 1

# Function to find a point on the elliptic curve
def find_point_on_curve(a, b, p):
    for x in range(p):
        rhs = (x**3 + a*x + b) % p
        if is_quadratic_residue(rhs, p):
            y = pow(rhs, (p + 1) // 4, p)
            return (x, y)
    return None

# Find a point P on the curve
P = find_point_on_curve(a, b, p)
print("Điểm P: ", P)

 
s = 311
print("s: ", s)

k = 209
print("k: ", k) 

def text_to_int(text):
    return int.from_bytes(text.encode(), 'big')

text = "nguyenthihuyenthuong"
print("text: ", text)
x = text_to_int(text)

def point_addition(P, Q, a, p):
    if P == Q:
        lam = (3 * P[0]**2 + a) * mod_inverse(2 * P[1], p) % p
    else:
        lam = (Q[1] - P[1]) * mod_inverse(Q[0] - P[0], p) % p
    
    x_r = (lam**2 - P[0] - Q[0]) % p
    y_r = (lam * (P[0] - x_r) - P[1]) % p
    
    return (x_r, y_r)

def point_multiplication(P, n, a, p):
    R = P
    for _ in range(n - 1):
        R = point_addition(R, P, a, p)
    return R

# B = sP
B = point_multiplication(P, s, a, p)

# Public key
public_key = (a, b, p, P, B)
print("khóa công khai:", public_key)

# Choose point M with x-coordinate containing x
M = (x, (x**3 + a*x + b) % p)

# Encrypt the message
C1 = point_multiplication(P, k, a, p)
C2 = point_addition(M, point_multiplication(B, k, a, p), a, p)
ciphertext = (C1, C2)
print("bản mã:", ciphertext)

# Decrypt the message
sC1 = point_multiplication(C1, s, a, p)
M_decrypted = point_addition(C2, (-sC1[0], -sC1[1]), a, p)
print("Thông điệp đã được giải mã: ", M_decrypted)
