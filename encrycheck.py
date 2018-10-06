from Crypto.Cipher import AES

salt = '!%F=-?Pst970'
key = "{: <32}".format(salt).encode("utf-8")
# key=b'\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x94\x9d(\x9e[EX\xc8\xd5\xbfI{\XA2$\X05(\XD5\X18'
# Encryption
cipher=AES.new(key)

def pad(s):
  return s+((16-len(s)%16)*'{')

def encrypt(plaintext):
  global cipher
  return cipher.encrypt(pad(plaintext))


def decrypt(ciphertext):
  global cipher
  dec=cipher.decrypt(ciphertext).decode('utf-8')
  l=dec.count("{")
  return dec[:len(dec)-1]

message=input("entet rhe value")
en=encrypt(message)
d=decrypt(en)
print("Encrypted",en)
print("decrypted",d)

# encryption_suite = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
# padded=pad('this is my message')
# cipher_text = encryption_suite.encrypt(padded)
# print("the siper text is ")
# print(cipher_text)
#
# # Decryption
# decryption_suite = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456sdfsffsdfsdfsff')
# plain_text = decryption_suite.decrypt(cipher_text)
# print(plain_text)


#
#
# message='this is my message'



