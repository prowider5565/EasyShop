from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from core.database import get_db
from core.middlewares import login_required
from models import variants  # sening Session generatoring
from . import schemas

variants_bp = Blueprint('variants', __name__, url_prefix='/variants')

@variants_bp.route('/create', methods=['POST'])
@login_required
def create_variant():
    db: Session = next(get_db())
    data = request.json
    variant_in = schemas.VariantCreate(**data)
    variant = variants.Variant(**variant_in.dict())
    db.add(variant)
    db.commit()
    db.refresh(variant)
    return jsonify(schemas.VariantOut.from_orm(variant).dict())

@variants_bp.route('/', methods=['GET'])
def list_variants():
    db: Session = next(get_db())
    variants = db.query(variants.Variant).all()
    return jsonify([schemas.VariantOut.from_orm(v).dict() for v in variants])

@variants_bp.route('/<int:variant_id>', methods=['PATCH'])
@login_required
# @is_owner
def update_variant(variant_id):
    db: Session = next(get_db())
    data = request.json
    variant = db.query(variants.Variant).filter(variants.Variant.id == variant_id).first()
    if not variant:
        return jsonify({'detail': 'Variant not found'}), 404
    update_data = schemas.VariantUpdate(**data).dict(exclude_unset=True)
    for key, value in update_data.items():
        # [(key, value), (key, value)]
        setattr(variant, key, value)
    db.commit()
    db.refresh(variant)
    return jsonify(schemas.VariantOut.from_orm(variant).dict())

@variants_bp.route('/<int:variant_id>', methods=['DELETE'])
def delete_variant(variant_id):
    db: Session = next(get_db())
    deleted = db.query(variants.Variant).filter(variants.Variant.id == variant_id).delete()
    db.commit()
    if not deleted:
        return jsonify({'detail': 'Variant not found'}), 404
    return jsonify({'detail': 'Variant deleted'})

@variants_bp.route('/<int:variant_id>/status', methods=['PATCH'])
def update_variant_status(variant_id):
    db: Session = next(get_db())
    is_active = request.json.get('is_active')
    variant = db.query(variants.Variant).filter(variants.Variant.id == variant_id).first()
    if not variant:
        return jsonify({'detail': 'Variant not found'}), 404
    variant.is_active = is_active
    db.commit()
    db.refresh(variant)
    return jsonify(schemas.VariantOut.from_orm(variant).dict())
