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

def generate_valid_s(n):
    while True:
        # Randomly select an integer in the range [1, n-1]
        s = random.randint(1, n-1)
        # Check if gcd(s, n) == 1 (coprime condition)
        if math.gcd(s, n) == 1:
            return s
        
########################## TASK 2 ######################


p = generate_prime_number(random.randint(1, 2048)) # generate a random prime from 1-2048 bits
q = generate_prime_number(random.randint(1, 2048)) # generate a random prime from 1-2048 bits
n = p * q
e = 65537 

lam = math.lcm(q-1, p-1)

d = modular_inverse(e, lam) # PRIVATE KEY

bob_s = generate_valid_s(n)

bob_c = pow(bob_s, e, n)

cprime = (bob_c * pow(2,e, n)) % n

s = pow(cprime, d, n) # Alice calculates s using cprime

mod_inverse_2 = modular_inverse(2, n)  # mallory computes the original s
recovered_s = (s * mod_inverse_2) % n

print("Original s from Bob:", bob_s)
print("Recovered s by Mallory:", recovered_s)

print(recovered_s == bob_s)
