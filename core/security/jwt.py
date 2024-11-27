import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import HTTPException, status

class JWTToken:
    def __init__(self, secret_key: str, algorithm: str = "HS256", access_token_expire_minutes: int = 30):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        """
        Generate an access token with an expiration time.

        :param data: The payload (claims) for the JWT.
        :param expires_delta: Expiration time (optional).
        :return: The encoded JWT token as a string.
        """
        if expires_delta:
            expiration = datetime.utcnow() + expires_delta
        else:
            expiration = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        
        to_encode = data.copy()
        to_encode.update({"exp": expiration})
        
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def verify_token(self, token: str):
        """
        Verify the JWT token and decode it.

        :param token: The JWT token string to be verified.
        :return: Decoded payload if the token is valid.
        :raises HTTPException: If the token is invalid or expired.
        """
        try:
            decoded_token = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return decoded_token
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
            )
        except jwt.JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )

# Example Usage
if __name__ == "__main__":
    secret_key = "your_secret_key_here"
    jwt_handler = JWTToken(secret_key)

    # Example user data to encode
    user_data = {"sub": "user123", "role": "admin"}

    # Create access token
    access_token = jwt_handler.create_access_token(data=user_data)
    print("Generated Access Token:", access_token)

    # Verify the token
    try:
        decoded_data = jwt_handler.verify_token(access_token)
        print("Decoded Token Data:", decoded_data)
    except HTTPException as e:
        print(e.detail)


class JWTToken:
    def __init__(self,secret_key, algorithm, expiry_delta):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expiry_delta = expiry_delta

    def jwt_encode(self,payload,expiry_delta: Optional[timedelta]= None):
        if expiry_delta:
            expiry = datetime.now(timezone.utc) + expiry_delta
        else:
            expiry = datetime.now(timezone.utc) + self.expiry_delta
        encode  = payload.copy()
        encode.update({"exp": expiry})
        token = jwt.encode(encode, self.secret_key, algorithm=self.algorithm)
        return token

    def jwt_decode(self, token):
        try:
            decode = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return decode
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")