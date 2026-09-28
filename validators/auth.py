import hashlib

ADMIN_USER = "admin"
ADMIN_PASS = "admin123"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_estudiante(credentials, student_code):
    if student_code in credentials:
        stored_hash = credentials[student_code]["password_hash"]
        return stored_hash
    return None

def login_admin(username, password):
    if username == ADMIN_USER and password == ADMIN_PASS:
        return True
    return False