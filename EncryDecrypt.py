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
