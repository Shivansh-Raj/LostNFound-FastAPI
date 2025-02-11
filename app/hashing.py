from passlib.context import CryptContext


pwd_cxt = CryptContext(deprecated = "auto", schemes=["bcrypt"])

class Hash():
    def bcrypt(password):
        Hashed_Password = pwd_cxt.hash(password)
        return Hashed_Password
    
    def verify(plain_password, hashed_password):
        return pwd_cxt.verify(plain_password, hashed_password)