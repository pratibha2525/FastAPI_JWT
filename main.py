from fastapi import FastAPI, Depends,HTTPException,status
from pydantic import BaseModel
from typing import List
from fastapi_jwt_auth import AuthJWT


app=FastAPI()

class Settings(BaseModel):
    authjwt_secret_key:str='d1ef9b7d36d6fce56880edbf90c8d6949961db163e4e573984d9675a639e6a8c'

@AuthJWT.load_config
def get_config():
    return Settings()


# User class
class User(BaseModel):
    username:str
    email:str 
    password:str 

    class Config:
        schema_extra={
            "example":{
                "username":"jack",
                "email":"jack@gmail.com",
                "password":"password"
            }
        }

# User login class
class Userlogin(BaseModel):
    username:str 
    password:str 

    class Config:
        schema_extra={
            "example":{
                "username":"jack",
                "password":"password"
            }
        }

users=[]

@app.get("/")
def index():
    return {"message":"Hello"}

#create a user
@app.post('/signup',status_code=201)
def create_user(user:User):
    new_user={
        "username":user.username,
        "email":user.email,
        "password":user.password
    }

    users.append(new_user)

    return new_user

#getting all users
@app.get('/users',response_model=List[User])
def get_users():
    return users

# User_login [Create_token]
@app.post('/login')
def login(user:Userlogin,Authorize:AuthJWT=Depends()):
    for u in users:
        if (u["username"]==user.username) and (u["password"]==user.password):
            access_token=Authorize.create_access_token(subject=user.username)
            refresh_token=Authorize.create_refresh_token(subject=user.username) # refresh_token

            return {"access_token":access_token,"refresh_token":refresh_token}

        raise HTTPException(status_code='401',detail="Invalid username or password")


# perticuler user token identy [add token and get user name]
@app.get('/protected')
def get_logged_in_user(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")

    current_user=Authorize.get_jwt_subject()

    return {"current_user":current_user}

# Old User is craete New_token
@app.get('/new_token')
def create_new_token(Authorize:AuthJWT=Depends()):

    try:
        Authorize.jwt_refresh_token_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")

    current_user=Authorize.get_jwt_subject()

    access_token=Authorize.create_access_token(subject=current_user)

    return {"new_access_token":access_token}

# Fresh login (After create new token)
@app.post('/fresh_login')
def fresh_login(user:Userlogin,Authorize:AuthJWT=Depends()):
    for u in users:
        if (u["username"]==user.username) and (u["password"]==user.password):
            fresh_token=Authorize.create_access_token(subject=user.username,fresh=True)

            return {"Fresh_token":fresh_token}
        
        raise HTTPException(status=status.HTTP_401_UNAUTHORIZED,detail="Invalid Username or Password")

# get Fresh token
@app.get('/fresh_url')
def get_users(Authorize:AuthJWT=Depends()):
    try:
        Authorize.fresh_jwt_required()
    except Exception as e:
        raise HTTPException(status=HTTP_401_UNAUTHORIZED,detail="Invalid Token")

    current_user=Authorize.get_jwt_subject()

    return {"current_user":current_user}