from pydantic import BaseModel
from dotenv import load_dotenv
from datetime import datetime

load_dotenv(override=True)

class GetDateInput(BaseModel):
    format: str

    def get_current_date(self) -> str:
        current_date = datetime.now()
        formatted_date = current_date.strftime(self.format)
        return formatted_date