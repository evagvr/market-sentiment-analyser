from datetime import datetime, timedelta
import requests
import pandas as pd
from config import NEWSAPI_KEY, NEWSAPI_BASE_URL
class NewsScraper:
    def __init__(self, ticker: str, company_name: str):
        self.ticker = ticker
        self.company_name = company_name
        self.api_key = NEWSAPI_KEY
        self.base_url = NEWSAPI_BASE_URL
    def fetch_headlines(self, days_back: int):
        from_date = (datetime.now() - timedelta(days_back)).strftime('%Y-%m-%d')
        to_date = datetime.now().strftime('%Y-%m-%d')
        params = {
            "q": f'"{self.company_name}" AND (stock OR shares OR earnings OR market OR investor)',
            "language": "en",
            "sortBy": "publishedAt",
            "from": from_date,
            "to": to_date,
            "pageSize": 100,
            "apiKey": self.api_key
        }
        try:
            response = requests.get(self.base_url, params=params)
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Failed to reach NewsAPI: {e}")
        if response.status_code != 200:
            raise ValueError(f"NewsAPI returned status {response.status_code}")
        data = response.json()
        if data['status'] == "error":
            raise ValueError(f"NewsAPI error: {data['message']}")
        articles = data['articles']
        return self._clean_response(articles)
    def _clean_response(self, articles: list):
        df = pd.DataFrame(articles)
        df = df[["title", "publishedAt", "source"]]
        df['source'] = df['source'].apply(lambda x: x['name'])
        df = df.rename(columns={
            'title': 'headline',
            'publishedAt': 'date'
        })
        df = df[df['headline'].notna()]
        df = df[df['headline'] != "[Removed]"]
        df['date'] = pd.to_datetime(df['date']).dt.date
        df = df.reset_index(drop=True)
        return df
if __name__ == '__main__':
    scraper = NewsScraper(ticker='AAPL', company_name='Apple')
    df = scraper.fetch_headlines(days_back=7)
    print(df.head(10))
    print(df.shape)
    print(df.dtypes)