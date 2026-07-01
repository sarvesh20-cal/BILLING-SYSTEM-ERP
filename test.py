import bcrypt

stored_hash = "$2b$12$LtT38L9UwETkdgH3K5C4UOYUzwbng7PqyHNvw8OBduQ6cddO0BQv6"

print(
    bcrypt.checkpw(
        "admin123".encode(),
        stored_hash.encode()
    )
)
