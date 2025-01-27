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


p = generate_prime_number(random.randint(1, 2048)) # generate a random prime from 1-2048 bits
q = generate_prime_number(random.randint(1, 2048)) # generate a random prime from 1-2048 bits
n = p * q
e = 65537 

lam = math.lcm(q-1, p-1)

d = modular_inverse(e, lam) # PRIVATE KEY

m1 = 1294028302 # messages
m2 = 67890

s1 = pow(m1, d, n) # signatures
s2 = pow(m2, d, n)

# mallory intercepts messages and signatures

m3 = (m1 * m2) % n
s3 = (s1 * s2) % n

print("This is message 3: ", m3)
print("This is the signature 3: ", s3)

print(pow(s3, e, n) == m3 % n) # return True if correct signature to new message
