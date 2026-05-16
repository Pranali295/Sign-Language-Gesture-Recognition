import hashlib

print(hashlib.sha256("admin1234".encode()).hexdigest())
print(hashlib.sha256("user1234".encode()).hexdigest())
