TORTOISE_ORM = {
    "connections": {"default": "sqlite://db.sqlite3"},
    "apps": {
        "models": {
            "models": ["users.models"],
            "default_connection": "default",
        }
    }
}
