from pydantic import BaseModel


# Model for the taco POST request
class TTSModel(BaseModel):
    text: str
