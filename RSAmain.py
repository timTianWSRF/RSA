import sys
DEFAULT_BLOCK_SIZE = 128  # 默认区块大小128bytes
BYTE_SIZE = 256  # 默认1byte有256种不同的值


def main():
    filename = 'encrypted_file.txt'
    mode = input('输入E为加密，输入D为解密：').lower()
    if mode == 'e':
        try:
            message = open(filename).read()
        except IOError:
            print('文件打开失败。')
        else:
            print("加密前明文内容：", end='')
            print(message)
            pubKeyFilename = 'al_sweigart_pubkey.txt'
            print('加密......')
            encryptedText = encryptAndWriteToFile(filename, pubKeyFilename, message)
            print('加密后密文内容：')
            print(encryptedText)
    elif mode == 'd':
        privKeyFilename = 'al_sweigart_privkey.txt'
        print('解密......')
        try:
            print('密文内容：', end='')
            print(open(filename).read())
            decryptedText = readFromFileAndDecrypt(filename, privKeyFilename)
        except IOError:
            print('文件打开失败。')
        else:
            print('解密文件明文内容：')
            print(decryptedText)


# getBlocksFromText()函数接受message返回一个表示它的列表，其元素为区块
def getBlocksFromText(message, blockSize=DEFAULT_BLOCK_SIZE):
    messageBytes = message.encode('ascii')  # 转为ASCII码对应的数字
    blockInts = []
    # for循环创建大整数，最终保存到blockInt里
    for blockStart in range(0, len(messageBytes), blockSize):
        blockInt = 0
        for i in range(blockStart, min(blockStart + blockSize, len(messageBytes))):
            blockInt += messageBytes[i] * (BYTE_SIZE ** (i % blockSize))
        blockInts.append(blockInt)
    # 返回的是blockInts列表而不是blockInt大数
    return blockInts


# 将区块列表转化为原始字符串
def getTextFromBlocks(blockInts, messageLength, blockSize=DEFAULT_BLOCK_SIZE):
    message = []
    for blockInt in blockInts:
        blockMessage = []
        for i in range(blockSize - 1, -1, -1):
            if len(message) + i < messageLength:
                asciiNumber = blockInt // (BYTE_SIZE ** i)
                blockInt = blockInt % (BYTE_SIZE ** i)
                blockMessage.insert(0, chr(asciiNumber))
        message.extend(blockMessage)
    return ''.join(message)


def encryptMessage(message, key, blockSize=DEFAULT_BLOCK_SIZE):
    encryptedBlocks = []
    n, e = key
    for block in getBlocksFromText(message, blockSize):
        # 下面的运算是block^e mod n
        encryptedBlocks.append(pow(block, e, n))
    return encryptedBlocks


# dexryptMessage保存解密的整数区块列表，key则通过多重赋值给n和d
def decryptMessage(encryptedBlocks, messageLength, key, blockSize=DEFAULT_BLOCK_SIZE):
    decryptedBlocks = []
    n, d = key
    for block in encryptedBlocks:
        # 对之前的block^e mod n运算解密
        decryptedBlocks.append(pow(block, d, n))
        return getTextFromBlocks(decryptedBlocks, messageLength, blockSize)


# 从密钥文件读取公钥和私钥
# 格式：密钥大小整数，n的大整数，e或d的大整数
# split()根据逗号分割，以字符串格式保存到content变量里
def readKeyFile(keyFilename):
    fo = open(keyFilename)
    content = fo.read()
    fo.close()
    keySize, n, EorD = content.split(',')
    return (int(keySize), int(n), int(EorD))


# 函数接受三个参数，分别是写入加密消息的文件名，需要的公钥文件名，和钥加密的消息
def encryptAndWriteToFile(messageFilename, keyFilename, message, blockSize=DEFAULT_BLOCK_SIZE):
    # 读取公钥和私钥
    keySize, n, e = readKeyFile(keyFilename)
    # 确认大小无误
    if keySize < blockSize * 8:  # 一个区块8比特
        sys.exit(
            'ERROR: Block size is %s bits and key size is %s bits. The RSA cipher requires the block size to be equal to or greater than the key size. Either decrease the block size or use different keys.' % (
                blockSize * 8, keySize))
    # 加密过程
    encryptedBlocks = encryptMessage(message, (n, e), blockSize)
    # 将大数字转为字符串
    for i in range(len(encryptedBlocks)):
        encryptedBlocks[i] = str(encryptedBlocks[i])
    encryptedContent = ','.join(encryptedBlocks)
    # 写入txt文件
    encryptedContent = '%s_%s_%s' % (len(message), blockSize, encryptedContent)
    fo = open(messageFilename, 'w')
    fo.write(encryptedContent)
    fo.close()
    # 并返回加密内容至屏幕
    return encryptedContent


# 函数两个参数分别是密文文件和密钥信息
def readFromFileAndDecrypt(messageFilename, keyFilename):
    keySize, n, d = readKeyFile(keyFilename)
    # 解密过程
    fo = open(messageFilename)
    content = fo.read()
    messageLength, blockSize, encryptedMessage = content.split('_')
    messageLength = int(messageLength)
    blockSize = int(blockSize)
    # Check that key size is greater than block size.
    if keySize < blockSize * 8:  # * 8 to convert bytes to bits
        sys.exit(
            'ERROR: Block size is %s bits and key size is %s bits. The RSA cipher requires the block size to be equal to or greater than the key size. Did you specify the correct key file and encrypted file?' % (
                blockSize * 8, keySize))
    # 将密文转为大数字
    encryptedBlocks = []
    for block in encryptedMessage.split(','):
        encryptedBlocks.append(int(block))
    # 返回解密结果
    decryptedContent = decryptMessage(encryptedBlocks, messageLength, (n, d), blockSize)
    fo = open(messageFilename, 'w')
    fo.write(decryptedContent)
    fo.close()
    return decryptedContent


if __name__ == '__main__':
    main()
