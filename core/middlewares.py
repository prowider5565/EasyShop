from functools import wraps
from flask import request, jsonify

from core.settings import SessionLocal
from users.models import User
from utils.jwt import verify_access


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid token"}), 401

        token = auth_header.split(" ")[1]
        try:
            user = verify_access(token)
        except Exception as e:
            return jsonify({"error": str(e)}), 401

        # Inject the user into the request context
        request.user = user
        return f(*args, **kwargs)

    return decorated_function


def is_admin_user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            session = SessionLocal()
            user = (
                session.query(User).get(request.user["user_id"])
            )
            print("User >>>>>>>>", user)
            print(not user, user.is_superuser)
            if not user.is_superuser or not user:
                return jsonify({"error": "Admin access required"}), 403
        except Exception as e:
            return jsonify({"error": "Invalid user or token"}), 401

        # User is admin, continue to the view
        return f(*args, **kwargs)

    return decorated_function
