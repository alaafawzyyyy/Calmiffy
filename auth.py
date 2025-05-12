from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta

# Constants
SECRET_KEY = "secretkeyhere"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expiration time (in minutes)

# Security context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Dummy user database (Replace with real database in production)
users_db = {}

# Helper functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify if plain password matches the hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str):
    """Authenticate user by checking credentials."""
    user = users_db.get(username)
    if not user or not verify_password(password, user["password"]):
        return False
    return username

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """Create an access token with an optional expiration time."""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({"exp": expire})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    """Retrieve the current user from the JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None or username not in users_db:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
