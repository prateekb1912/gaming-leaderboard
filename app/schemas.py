from pydantic import BaseModel

class ScoreSubmissionInput(BaseModel):
    user_id: int
    score: int