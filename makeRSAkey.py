import random, sys, os, cryptomath
import rabinMiller


def main():
    print('生成密钥对.....')
    # 把字符串al_sweigart'和整数1024传给makeKeyFiles()调用
    # 公钥私钥保存在al_sweigart-pubkey.txt和al_sweigart-privkey.txt
    makeKeyFiles('al_sweigart', 1024)
    print('密钥对制作完成')


def generateKey(keysize):
    print('生成随机大质数p......')
    p = rabinMiller.generateLargePrime(keysize)
    print('生成随机大质数q......')
    q = rabinMiller.generateLargePrime(keysize)
    # 生成公钥和私钥的公有部分n
    n = q * p
    # 创建随机数e，它与q-1和p-1的积互质
    print('创建随机数e......')
    while True:
        # 创建随机数e
        e = random.randrange(2 ** (keysize - 1), 2 ** (keysize))
        # 检测e与q - 1和p - 1的积是否互质
        # 不互质则继续循环，反之则跳出
        if cryptomath.gcd(e, (p - 1) * (q - 1)) == 1: break
    print('计算e的逆模d......')
    d = cryptomath.findModInverse(e, (p - 1) * (q - 1))
    # 以元组形式进行保存公钥和私钥对
    publicKey = (n, e)
    privateKey = (n, d)
    # 打印操作
    print('显示公钥内容：', publicKey)
    print('显示私钥内容：', privateKey)
    return (publicKey, privateKey)


# 将公钥私钥保存到txt文件
def makeKeyFiles(name, keySize):
    # 如有同名的密钥文件存在，则发出更改名称的警告
    if os.path.exists('%s_pubkey.txt' % name) or os.path.exists('%s_privkey.txt' % name):
        sys.exit('警告！有重名文件')
    # 返回一个元组，他包含两个元组，都一样保存在publicKey和privateKey中
    publicKey, privateKey = generateKey(keySize)
    # 密钥文件格式：密钥大小整数，n整数，e/d整数
    # 公钥信息
    print()
    print('公钥对长度：n的长度： %s位 ，e的长度 %s 位。' % (len(str(publicKey[0])), len(str(publicKey[1]))))
    print('公钥文件名： %s_pubkey.txt...' % (name))
    fo = open('%s_pubkey.txt' % (name), 'w')
    fo.write('%s,%s,%s' % (keySize, publicKey[0], publicKey[1]))
    fo.close()
    # 私钥信息
    print()
    print('私钥对长度：n的长度： %s位 ，d的长度 %s 位。' % (len(str(publicKey[0])), len(str(publicKey[1]))))
    print('私钥文件名： %s_pubkey.txt...' % (name))
    fo = open('%s_privkey.txt' % (name), 'w')
    fo.write('%s,%s,%s' % (keySize, privateKey[0], privateKey[1]))
    fo.close()


if __name__ == '__main__':
    main()
