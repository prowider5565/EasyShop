<<<<<<< HEAD
from tortoise import Tortoise
from core.settings import TORTOISE_ORM



async def init_db():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas(safe=True)
=======
import hashlib


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()
>>>>>>> 7ea9ee8998efba622606bc9777671321efdba423
