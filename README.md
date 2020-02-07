# RSA加密解密法模拟
1. 首先运行makeRSAkey.py文件来生成加密解密必要的密钥文件。 
2. al_sweigart_privkey.txt是公钥文件；al_sweigart_pubkey.txt是私钥文件。
3. 在encrypted_file.txt文件中写入要加密的明文，必须是英文。
4. 运行RSAmain.py文件，键入E加密，键入D解密，此时键入E进行加密。
5. 打开encrypted_file.txt文件可以看到已经是加密后的一堆乱码。
6. 再运行RSAmain.py文件，键入E加密，键入D解密，此时键入D进行解密。
7. 这时打开encrypted_file.txt文件可以看到原来的明文，解密成功。
