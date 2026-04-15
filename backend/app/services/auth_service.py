from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional
import os
import bcrypt

# Configure bcrypt with proper rounds
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12
)

class AuthService:
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    
    @staticmethod
    def hash_password(password: str) -> str:
        try:
            # Truncate password to 72 bytes for bcrypt compatibility
            truncated_password = password[:72]
            return pwd_context.hash(truncated_password)
        except Exception as e:
            # Fallback to direct bcrypt
            truncated_password = password[:72].encode('utf-8')
            salt = bcrypt.gensalt(rounds=12)
            hashed = bcrypt.hashpw(truncated_password, salt)
            return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        try:
            truncated_password = plain_password[:72]
            return pwd_context.verify(truncated_password, hashed_password)
        except Exception as e:
            # Fallback to direct bcrypt
            try:
                truncated_password = plain_password[:72].encode('utf-8')
                hashed_bytes = hashed_password.encode('utf-8') if isinstance(hashed_password, str) else hashed_password
                return bcrypt.checkpw(truncated_password, hashed_bytes)
            except:
                return False
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=AuthService.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, AuthService.SECRET_KEY, algorithm=AuthService.ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def decode_token(token: str) -> Optional[dict]:
        try:
            payload = jwt.decode(token, AuthService.SECRET_KEY, algorithms=[AuthService.ALGORITHM])
            return payload
        except JWTError:
            return None
