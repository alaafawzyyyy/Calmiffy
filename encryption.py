from cryptography.fernet import Fernet

# Key cache to store user-specific keys
key_cache = {}

def generate_key() -> bytes:
    """Generate a random key for encryption (do NOT use in production)."""
    return Fernet.generate_key()

def get_fernet(user: str) -> Fernet:
    """Get or generate a Fernet instance for the user, caching the key."""
    if user not in key_cache:
        key_cache[user] = generate_key()
    return Fernet(key_cache[user])

def encrypt(message: str, user: str) -> str:
    """Encrypt a message using the user's key."""
    fernet = get_fernet(user)
    return fernet.encrypt(message.encode()).decode()

def decrypt(token: str, user: str) -> str:
    """Decrypt a message using the user's key."""
    fernet = get_fernet(user)
    return fernet.decrypt(token.encode()).decode()
