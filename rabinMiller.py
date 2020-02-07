import random
import primeSieve


def rabinMiller(num):
    # 快速幂
    s = num - 1
    t = 0
    while s % 2 == 0:
        s = s // 2
        t += 1
    # 最小费马定理
    for trials in range(5):
        a = random.randrange(2, num - 1)
        v = pow(a, s, num)
        if v != 1:
            i = 0
            while v != (num - 1):
                if i == t - 1:
                    return False
                else:
                    i = i + 1
                    v = (v ** 2) % num
    return True


def isPrime(num):
    if num < 2:
        return False
    # prime.txt是存放素数表的文件
    lowPrimes = primeSieve.in()
    if num in lowPrimes:
        return True
    for prime in lowPrimes:
        if num % prime == 0:
            return False
    return rabinMiller(num)


# generateLargePrime函数返回素数。它选出一个大的随机数保存到num
# 再将num传到isPrime和rabinMiller进行判断是不是素数
# 先isPrime后rabinMiller是因为复杂度先简后繁
def generateLargePrime(keysize=1024):
    while True:
        num = random.randrange(2 ** (keysize - 1), 2 ** keysize)
        if isPrime(num):
            return num


