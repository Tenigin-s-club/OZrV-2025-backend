from pydantic import BaseModel
from datetime import date


class SStatistics(BaseModel):
    date: date
    requests_avg_time: float
    requests_count: int
