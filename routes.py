from fastapi import FastAPI

from utilities import generate_token

users = {}
login_tokens = []

router = FastAPI(
    title="SSO Application",
    description="Simple application demo on how SSO works"
)


@router.post("/new/")
async def new_user(user: dict):
    user_id = len(users) + 1
    users[user_id] = user

    return {
        "message": "User data successfully added"
    }


@router.post("/sso")
async def get_sso_link(user_id: int):
    if users[user_id]:
        token = await generate_token(user_id)
        login_tokens.append(token)
        return token
    return {
        "error": "User with supplied ID doesn't exist"
    }


@router.get("/sso/")
async def sign_in(token: str):
    if token in login_tokens:
        return {
            "message": "User logged in successfully."
        }

    return {
        "error": "Invalid token passed"
    }