TORTOISE_ORM = {
    "connections": {"default": "sqlite://db.sqlite3"},
    "apps": {
        "users": {
            "models": ["users.models"],
            "default_connection": "default",
        },
        "products": {
            "models": ["products.models", "category.models"],  # IKKALASINI BIR QATORGA QO‘SH
            "default_connection": "default",
        },
    },
}


JWT_SETTINGS = {
    "secret_key": "strongKey",
    "algorithm": "HS256",
    "access_exp_minutes": 180,
    "refresh_exp_days": 7,
}
