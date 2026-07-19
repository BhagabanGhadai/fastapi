from pwdlib import PasswordHash

class Helper:
    def hash_password(self,password:str)->str:
        password_hash=PasswordHash.recommended()
        return password_hash.hash(password)

    def verify_password(self,password:str,hashed_password:str)->bool:
        password_hash=PasswordHash.recommended()
        return password_hash.verify(password,hashed_password)