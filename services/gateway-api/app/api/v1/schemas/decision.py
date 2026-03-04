from pydantic import BaseModel

class DecisionCreate(BaseModel):
    personal_number: str
    amount: float
    # TODO: add the rest of the fields
