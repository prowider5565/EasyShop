# Mijoz registratsiyasi bolsin - done
# Administrator registratsiya bolsin - done
# Login - done
# Get-info - uzimni malumotlarimni olish uchun api - done 
# Get-users !!!! faqatgina administrator kora olsin - done 

from flask import Blueprint, request, jsonify
from users.models import User
from core.utils import hash_password
import hashlib

user_bp = Blueprint("user", __name__)



@user_bp.route("/register", methods=["POST"])
async def register():
    data = request.form
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    is_superuser = data.get("is_superuser")

    if is_superuser is None or is_superuser == "":
        is_superuser = False
    else:
        is_superuser = str(is_superuser).lower() == "true"


    if not username or not email or not password:
        return jsonify({"error": "All fields are required"}), 400
    hashed_pw = hash_password(password)

    try:
        await User.create(username=username, email=email, password=hashed_pw,is_superuser=is_superuser)
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route("/login", methods=["POST"])
async def login():
    data = request.form
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
            return jsonify({"error": "Username va password kerak"}), 400

    try:
        user = await User.get(username=username)
    except:
        return jsonify({"error": "Username noto'g'ri"}), 404

    input_hash = hashlib.sha256(password.encode()).hexdigest()

    if user.password != input_hash:
        return jsonify({"error": "Parol noto'g'ri"}), 401
    
    return jsonify({"message": f"Xush kelibsiz, {user.username}! Sizning ma'lumotlaringiz: Username - {user.username}, Email - {user.email}, Tizimga kirgan vaqt - {user.created_at}"})


@user_bp.route("/get", methods=["POST"])
async def get_user():
    data = request.form

    current_user_id = data.get("current_user_id")  # Kim so‘rov yuboryapti
    target_user_id = data.get("id")                # Qaysi foydalanuvchini ko‘rmoqchi

    if not current_user_id or not target_user_id:
        return jsonify({"error": "ID lar kerak"}), 400

    current_user = await User.get(id=int(current_user_id))

    if current_user.is_superuser:
        target_user = await User.get(id=int(target_user_id))
        return jsonify({
            "id": target_user.id,
            "username": target_user.username,
            "email": target_user.email
        })
    else:
        return jsonify({"error": "Siz admin emassiz"}), 403
    