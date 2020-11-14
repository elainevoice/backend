from pydantic import BaseModel


# Model for the taco POST request
class TextData(BaseModel):
    text: str
