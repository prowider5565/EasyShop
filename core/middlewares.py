from functools import wraps
from flask import request, jsonify

from users.models import User
from utils.jwt import verify_access


def login_required(f):
    @wraps(f)
    async def decorated_function(*args, **kwargs):
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
        return await f(*args, **kwargs)

    return decorated_function


def is_admin_user(f):
    @wraps(f)
    async def decorated_function(*args, **kwargs):
        try:
            user = await User.get(id=request.user["user_id"])
            if not user.is_superuser:
                return jsonify({"error": "Admin access required"}), 403
        except Exception as e:
            return jsonify({"error": "Invalid user or token"}), 401

        # User is admin, continue to the view
        return await f(*args, **kwargs)

    return decorated_function
