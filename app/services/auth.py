from functools import wraps
import jwt
from flask import request
from app.services.config import CONFIG
from app.data.repositories import UsersRepository

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        
        try:
            data=jwt.decode(token, CONFIG['jwt']['secret'], algorithms=["HS256"])
            users_table = UsersRepository()
            current_user = users_table.get_by_id(data["user_id"])
            if current_user is None:
                return {
                "message": "Invalid Authentication token!",
                "data": None,
                "error": "Unauthorized"
            }, 401

        except jwt.InvalidSignatureError as e:
            return {
                "message": "Invalid Authentication token!",
                "data": e,
                "error": "Unauthorized"
            }, 401
        except Exception as e:
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 500

        return f(current_user, *args, **kwargs)
    return decorated
