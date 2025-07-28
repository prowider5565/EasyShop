from pydantic import BaseModel


class CreateAddressSchema(BaseModel):
    street: str
    city: str
    state: str
    postal_code: str
    country: str


class ReadAddressSchema(CreateAddressSchema):
    id: int
    user_id: int

    class Config:
        from_attributes = True
