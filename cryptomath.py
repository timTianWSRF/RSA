# 返回a与b的最大公约数
def gcd(a, b):
    while a != 0:
        a, b = b % a, a
    return b


# 返回a与b的逆模（当a*x % b = 1时x称为a和b的逆模）
def findModInverse(a, m):
    # 先判断是否互质
    if gcd(a, m) != 1:
        return None
    # 计算逆模
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m
