from flask import Blueprint, request, jsonify
from core.database import SessionLocal
from core.middlewares import login_required
from identity.schemas import CreateAddressSchema, ReadAddressSchema
from models.identity import Address

addr_router = Blueprint("address", __name__)


@addr_router.route("/create", methods=["POST"])
@login_required
def create_address():
    try:
        data = request.get_json()
        user_id = request.user["user_id"]
        serialized_data = CreateAddressSchema(**data)
        db = SessionLocal()
        address = Address(user_id=user_id, **serialized_data.model_dump())
        db.add(address)
        db.commit()
        db.refresh(address)
        return jsonify(ReadAddressSchema.from_orm(address).model_dump()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@addr_router.route("/", methods=["GET"])
@login_required
def list_addresses():
    try:
        user_id = request.user["user_id"]
        db = SessionLocal()
        addresses = db.query(Address).filter_by(user_id=user_id).all()
        return jsonify(
            [ReadAddressSchema.from_orm(addr).model_dump() for addr in addresses]
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@addr_router.route("/<int:address_id>", methods=["GET"])
@login_required
def get_address(address_id):
    try:
        user_id = request.user["user_id"]
        db = SessionLocal()
        address = db.query(Address).filter_by(id=address_id, user_id=user_id).first()
        if not address:
            return jsonify({"error": "Address not found"}), 404
        return jsonify(ReadAddressSchema.from_orm(address).model_dump())
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@addr_router.route("/<int:address_id>", methods=["PUT"])
@login_required
def update_address(address_id):
    try:
        data = request.get_json()
        user_id = request.user["user_id"]
        serialized_data = CreateAddressSchema(**data)

        db = SessionLocal()
        address = db.query(Address).filter_by(id=address_id, user_id=user_id).first()
        if not address:
            return jsonify({"error": "Address not found"}), 404

        for field, value in serialized_data.model_dump().items():
            setattr(address, field, value)

        db.commit()
        db.refresh(address)
        return jsonify(ReadAddressSchema.from_orm(address).model_dump())
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@addr_router.route("/<int:address_id>", methods=["DELETE"])
@login_required
def delete_address(address_id):
    try:
        user_id = request.user["user_id"]
        db = SessionLocal()
        address = db.query(Address).filter_by(id=address_id, user_id=user_id).first()
        if not address:
            return jsonify({"error": "Address not found"}), 404

        db.delete(address)
        db.commit()
        return jsonify({"message": "Address deleted"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
