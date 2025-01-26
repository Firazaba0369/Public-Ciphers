from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from hashlib import sha256
import random

def main():
    #selcect the prime number and the base
    q = int("B10B8F96A080E01DDE92DE5EAE5D54EC52C99FBCFB06A3C69A6A9DCA52D23B616073E28675A23D189838EF1E2EE652C013ECB4AEA906112324975C3CD49B83BFACCBDD7D90C4BD7098488E9C219A73724EFFD6FAE5644738FAA31A4FF55BCCC0A151AF5F0DC8B4BD45BF37DF365C1A65E68CFDA76D4DA708DF1FB2BC2E4A4371", 16)
    a = int("A4D1CBD5C3FD34126765A442EFB99905F8104DD258AC507FD6406CFF14266D31266FEA1E5C41564B777E690F5504F213160217B4B01B886A5E91547F9E2749F4D7FBD7D3B9A92EE1909D0D2263F80A76A6A24C087A091F531DBF0A0169B6A28AD662A4D18E73AFA32D779D5918D08BC8858F4DCEF97C2A24855E6EEB22B3B2E5", 16)

    #generate private and public keys for Alice
    Xa = random.randint(1, q - 1)
    Ya = pow(a, Xa ,q)

    #generate private and publics keys for Bob
    Xb = random.randint(1, q - 1)
    Yb = pow(a, Xb, q)

    #message is intercepted by Mallory
    Ya = q
    Yb = q

    #print the private and public keys
    print("Alice's private key: ", Xa)
    print("Alice's public key: ", Ya)
    print("Bob's private key: ", Xb)
    print("Bob's public key:", Yb)

    #calculate Alice and Bob's shared secret
    Sa = pow(a, Yb, q)
    Sb = pow(a, Ya, q)

    #calculate Alice, Bob, and Mallory's symmetric key
    Ka = sha256(str(Sa).encode()).digest()[:16]
    Kb = sha256(str(Sb).encode()).digest()[:16]
    Km = sha256(str(Sa).encode()).digest()[:16]

    #messages to be sent
    m0 = "Hi Bob!"
    m1 = "Hi Alice!"

    #print the message before encryption
    print("Alice's message before encryption: ", m0)
    print("Bob's message before encryption: ", m1)

    #encrypt the data
    iv0 = get_random_bytes(AES.block_size)
    iv1 = get_random_bytes(AES.block_size)

    #create encryption ciphers
    cipher_a = AES.new(Ka, AES.MODE_CBC, iv0)
    cipher_b = AES.new(Kb, AES.MODE_CBC, iv1)

    #encrypt Alice and Bob's messages
    c0 = cipher_a.encrypt(pad(m0.encode(), AES.block_size))
    c1 = cipher_b.encrypt(pad(m1.encode(), AES.block_size))

    #decrypt Alice, Bob, Mallory's messages
    cipher_m_decrypt = AES.new(Km, AES.MODE_CBC, iv0)
    cipher_a_decrypt= AES.new(Km, AES.MODE_CBC, iv0)
    cipher_b_decrypt = AES.new(Kb, AES.MODE_CBC, iv1)

    #unpad the messages
    unpadded_m0 = unpad(cipher_a_decrypt.decrypt(c0), AES.block_size)
    unpadded_m1 = unpad(cipher_b_decrypt.decrypt(c1), AES.block_size)
    unpadded_m2 = unpad(cipher_m_decrypt.decrypt(c0), AES.block_size)

    #print the messages after decryption
    print("Alice's message after decryption: ", unpadded_m0.decode())
    print("Bob's message after decryption: ", unpadded_m1.decode())
    print("Mallory's intercepted message after decryption:", unpadded_m2.decode())

if __name__ == '__main__':
    main()