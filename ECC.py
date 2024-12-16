import random
from Crypto.Util.number import getPrime, inverse, bytes_to_long, long_to_bytes

def is_quadratic_residue(n, p):
    return pow(n, (p - 1) // 2, p) == 1

def elliptic_curve_points(p, a, b):
    points = []
    for x in range(p):
        y2 = (x**3 + a*x + b) % p
        if is_quadratic_residue(y2, p):
            for y in range(p):
                if (y * y) % p == y2:
                    points.append((x, y))
    return points

a = 43
b = 454
p = 10007

points = elliptic_curve_points(p, a, b)
print("điểm trên đường cong elliptic là:")
with open('E:/mmvatttcode/resultsECC.docx', 'w') as fobj:
    for i in range(len(points)):
        s = str(points[i])
        fobj.write(s)
        fobj.write("\n")
        print(points[i])
    
fobj.close()
print("", len(points)+1)
print("p =", p)
class EllipticCurve:
    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p

    def add(self, P, Q):
        if P == Q:
            lam = (3 * P[0]**2 + self.a) * pow(2 * P[1], -1, self.p) % self.p
           
        else:
            lam = (Q[1] - P[1]) * pow(Q[0] - P[0], -1, self.p) % self.p
        x = (lam**2 - P[0] - Q[0]) % self.p
        y = (lam * (P[0] - x) - P[1]) % self.p
        
        return (x, y)

    def multiply(self, P, n):
        Q = P
        R = None
        while n:
            if n & 1:
                R = Q if R is None else self.add(R, Q)
            Q = self.add(Q, Q)
            n >>= 1
        return R
    
    def is_on_curve(self, x, y):
        return (y**2 - x**3 - self.a * x - self.b) % self.p == 0

    def randompoint(self):
        while True:
            x = random.randint(0, self.p - 1)
            y = random.randint(0, self.p - 1)
            if self.is_on_curve(x, y):
                return (x, y)


# Đường cong Elliptic E: y^2 = x^3 + ax + b (mod p)

curve = EllipticCurve(a, b, p)


    
# Điểm P trên đường cong
P = curve.randompoint()
Q = curve.randompoint()
print("P = ", P)
print("Q = ", Q)

# Tính sP
print("nhập s:")
s = int(input())
sP = curve.multiply(P, s)
r = curve.add(P, Q)

print("sP = ", sP)
print("P + Q = ", r)