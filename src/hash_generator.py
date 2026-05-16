import hashlib

# Admin password
admin_password = "adm1234"
admin_hash = hashlib.sha256(admin_password.encode()).hexdigest()

print("Admin Hash:", admin_hash)
