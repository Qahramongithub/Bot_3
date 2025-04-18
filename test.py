import bcrypt

# Your password as a string
password = b"Qahram0n"  # This needs to be bytes

# Generate a salt
salt = bcrypt.gensalt()

# Hash the password with the salt
hashed_password = bcrypt.hashpw(password, salt)

# Print the hashed password
print(hashed_password)
