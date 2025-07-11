from functools import wraps
from flask import request, jsonify

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
