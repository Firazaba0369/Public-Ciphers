import sympy
import random
import math

def generate_prime_number(bits: int) ->int:
    return sympy.randprime(2**(bits-1), 2**bits-1)

def extended_gcd(a, b): 
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y

def modular_inverse(e, lambda_n):
    gcd, x, _ = extended_gcd(e, lambda_n)
    return x % lambda_n


################# Key Generation ########################
e = 65537 # preset number

p = generate_prime_number(random.randint(1, 2048)) # generate a random prime from 1-2048 bits
q = generate_prime_number(random.randint(1, 2048)) # generate a random prime from 1-2048 bits
print("This is the value p: ", p)
print("This is the value q: ", q)

n = p*q 
print("This is the value n: ", n)

lam = math.lcm(q-1, p-1)

d = modular_inverse(e, lam) # PRIVATE KEY

################ Encoding and Decoding Message ################# 

secret_message = "hello bob!"
print("This is the secret message: ", secret_message)

hex_secret = secret_message.encode().hex()
print("This is the secret message in hex: ", hex_secret)

encrypted_message = pow(int(hex_secret, 16), e, n) # encrypt the message using e, public key

print("This is the encrypted message: ", encrypted_message)

decrypted_message = pow(encrypted_message, d, n)   # decrypt the message using d 

decrypted_hex = hex(decrypted_message)[2:] # skip the first 0x part

print("This is the decrypted hex: ", decrypted_hex)

decoded_message = bytes.fromhex(decrypted_hex).decode('utf-8')
print("This is the decoded secret message: ", decoded_message)
