import os
import requests
from typing import Optional
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from .database import get_db
from .models import User

# Load settings from environment
COGNITO_USER_POOL_ID = os.getenv("COGNITO_USER_POOL_ID")
COGNITO_APP_CLIENT_ID = os.getenv("COGNITO_APP_CLIENT_ID")
AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

_jwks_cache = None

def get_jwks():
    global _jwks_cache
    if _jwks_cache is None and COGNITO_USER_POOL_ID:
        url = f"https://cognito-idp.{AWS_REGION}.amazonaws.com/{COGNITO_USER_POOL_ID}/.well-known/jwks.json"
        response = requests.get(url)
        if response.status_code == 200:
            _jwks_cache = response.json().get("keys", [])
    return _jwks_cache or []

def verify_cognito_token(token: str):
    keys = get_jwks()
    headers = jwt.get_unverified_headers(token)
    kid = headers.get("kid")
    
    key = next((k for k in keys if k["kid"] == kid), None)
    if not key:
        raise JWTError("Public key not found in JWKS")
    
    issuer = f"https://cognito-idp.{AWS_REGION}.amazonaws.com/{COGNITO_USER_POOL_ID}"
    
    payload = jwt.decode(
        token,
        key,
        algorithms=["RS256"],
        audience=COGNITO_APP_CLIENT_ID,
        issuer=issuer
    )
    return payload

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        if COGNITO_USER_POOL_ID:
            payload = verify_cognito_token(token)
            email: str = payload.get("email")
        else:
            # Fallback for local testing
            payload = jwt.decode(token, os.getenv("SECRET_KEY", "fallback"), algorithms=["HS256"])
            email: str = payload.get("sub")
            
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

def get_current_user_optional(request: Request, db: Session = Depends(get_db)):
    authorization = request.headers.get("Authorization")
    if not authorization:
        return None
    scheme, token = get_authorization_scheme_param(authorization)
    if authorization is None or scheme.lower() != "bearer":
        return None
    
    try:
        if COGNITO_USER_POOL_ID:
            payload = verify_cognito_token(token)
            email: str = payload.get("email")
        else:
            payload = jwt.decode(token, os.getenv("SECRET_KEY", "fallback"), algorithms=["HS256"])
            email: str = payload.get("sub")
            
        if email is None:
            return None
    except JWTError:
        return None
    
    user = db.query(User).filter(User.email == email).first()
    return user

def get_current_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions. Admin access required."
        )
    return current_user
