import sys
import random
import hashlib
import collections

# Khởi tạo EllipticCurve với các tham số của đường cong
EllipticCurve = collections.namedtuple('EllipticCurve', 'p a b g n h')

p1 = 2**256 - 2**224 + 2**192 + 2**96 - 1


curve = EllipticCurve(
    p=p1,
    a=-3,
    b=41058363725152142129326129780047268409114441015993725554835256314039467401291,
    g=(48439561293906451759052585252797914202762949526041747995844080717082404635286,
       36134250956749795798585127919587881956611106672985015071877198253568414405109),
    # Bậc của nhóm con.
    n=0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551,
    # Hệ số kết hợp của nhóm con.
    h=1,
)

print("Số p: ", curve.p)
print("a = ", curve.a)
print("b = ", curve.b)

# Tính số nghịch đảo theo mô-đun
def inverse_mod(k, p):
    if k == 0:
        raise ZeroDivisionError('division by zero')

    if k < 0:
        # k ** -1 = p - (-k) ** -1  (mod p)
        return p - inverse_mod(-k, p)

    # Euclid mở rộng.
    s, old_s = 0, 1
    t, old_t = 1, 0
    r, old_r = p, k

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    gcd, x, y = old_r, old_s, old_t

    assert gcd == 1
    assert (k * x) % p == 1

    return x % p

# Kiểm tra điểm thuộc đường cong hay không
def is_on_curve(point):
    # Điểm ở vô cực.
    if point is None:
        return True
    x, y = point
    return (y * y - x * x * x - curve.a * x - curve.b) % curve.p == 0 

# Cộng điểm
def point_add(point1, point2):
    assert is_on_curve(point1)
    assert is_on_curve(point2)

    if point1 is None:
        # 0 + point2 = point2
        return point2
    if point2 is None:
        # point1 + 0 = point1
        return point1

    x1, y1 = point1
    x2, y2 = point2

    if x1 == x2 and y1 != y2:
        # point1 + (-point1) = 0
        return None

    if x1 == x2:
        # Trường hợp điểm trùng nhau
        m = (3 * x1 * x1 + curve.a) * inverse_mod(2 * y1, curve.p)
    else:
        # Trường hợp điểm khác nhau
        m = (y1 - y2) * inverse_mod(x1 - x2, curve.p)
    x3 = m * m - x1 - x2
    y3 = y1 + m * (x3 - x1)
    result = (x3 % curve.p, -y3 % curve.p)
    assert is_on_curve(result)
    return result

# Nhân điểm
def scalar_mult(k, point):
    assert is_on_curve(point)
    if k % curve.n == 0 or point is None:
        return None
    if k < 0:
        # k * point = -k * (-point)
        return scalar_mult(-k, point_neg(point))
    result = None
    addend = point
    while k:
        if k & 1:
            result = point_add(result, addend)
        addend = point_add(addend, addend)
        k >>= 1
    assert is_on_curve(result)
    return result

def point_neg(point):
    assert is_on_curve(point)
    if point is None:
        # -0 = 0
        return None
    x, y = point
    result = (x, -y % curve.p)
    assert is_on_curve(result)
    return result


# Thông điệp
message = "nguyenthihuyenthuong"  

if len(sys.argv) > 1:
    msg = sys.argv[1]

# Khóa riêng
privatekey = random.randint(0, curve.n - 1) 

# Khóa công khai
publickey = scalar_mult(privatekey, curve.g)   

# Băm thông điệp
h = int(hashlib.sha256(message.encode()).hexdigest(), 16)  

# Tạo số ngẫu nhiên k
k = random.randint(0, curve.n - 1)  

# Tính điểm r từ k và điểm cơ sở g
rpoint = scalar_mult(k, curve.g)
r = rpoint[0] % curve.n

# Tính s với h, r và dA
inv_k = inverse_mod(k, curve.n)
s = (inv_k * (h + r * privatekey)) % curve.n

print("Thông điệp: ", message)
print("Khóa riêng = ", privatekey)
print("Khóa công khai = ", publickey )
print("k = ", k)
print("(r,s) = ", (r,s))

# Kiểm tra chữ ký
inv_s = inverse_mod(s, curve.n)
u1 = (h * inv_s) % curve.n
u2 = (r * inv_s) % curve.n

# Tính toán điểm P để kiểm tra chữ ký
P = point_add(scalar_mult(u1, curve.g), scalar_mult(u2, publickey))

# Giá trị x của P theo mod n
res = P[0] % curve.n  

if res == r:
    print("Xác minh chữ ký: Hợp lệ")
else:
    print("Xác minh chữ ký: Không hợp lệ")