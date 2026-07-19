from core import settings
from datetime import timedelta,datetime
from utils.type import TokenType
from pwdlib import PasswordHash
import jwt

class Helper:
    def hash_password(self,password:str)->str:
        password_hash=PasswordHash.recommended()
        return password_hash.hash(password)

    def verify_password(self,password:str,hashed_password:str)->bool:
        password_hash=PasswordHash.recommended()
        return password_hash.verify(password,hashed_password)

    def generate_jwt_token(self,payload:dict,type:TokenType=TokenType.ACCESS)->str:
        to_encode=payload.copy()
        if type==TokenType.ACCESS:
            expires_delta= timedelta(minutes=settings.ACCESS_TOKEN_EXPIRY_IN_MIN)
        else:
            expires_delta= timedelta(minutes=settings.REFRESH_TOKEN_EXPIRY_IN_MIN)
        
        to_encode.update({"exp":datetime.now()+expires_delta,"token_type":type.value})

        if type==TokenType.ACCESS:
            encoded_jwt= jwt.encode(to_encode,settings.ACCESS_TOKEN_SECRET,algorithm=settings.ALGORITHM)
        else:
            encoded_jwt= jwt.encode(to_encode,settings.REFRESH_TOKEN_SECRET,algorithm=settings.ALGORITHM)
            
        return encoded_jwt

    def decode_jwt_token(self,token:str,type:TokenType=TokenType.ACCESS)->dict:
        try:
            if type==TokenType.ACCESS:
                decoded_jwt= jwt.decode(token,settings.ACCESS_TOKEN_SECRET,algorithms=[settings.ALGORITHM])
            else:
                decoded_jwt= jwt.decode(token,settings.REFRESH_TOKEN_SECRET,algorithms=[settings.ALGORITHM])
            return decoded_jwt
        except Exception as e:
            raise e
            