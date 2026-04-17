from abc import ABC, abstractmethod
import pandas as pd
from datetime import datetime, timedelta

class BaseScraper(ABC):
    def __init__(self, ticker: str, company_name: str):
        self.ticker = ticker
        self.company_name = company_name
    @abstractmethod
    def fetch_headlines(self, days_back: int):
       pass

    @abstractmethod
    def _clean_response(self, raw_data, days_back: int) -> pd.DataFrame:
        pass

    def _is_within_date_range(self, date, days_back: int) -> bool:
        cutoff = datetime.now().date() - timedelta(days_back)
        return date >= cutoff
