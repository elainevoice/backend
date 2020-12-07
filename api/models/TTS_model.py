from pydantic import BaseModel


# Model for the taco POST request
class TTS_model(BaseModel):
    text: str
