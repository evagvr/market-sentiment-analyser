import feedparser
import pandas as pd
from urllib.parse import urlparse
from datetime import date

from base import BaseScraper
class RssScraper(BaseScraper):
    def __init__(self, ticker: str, company_name: str, feed_url):
        super().__init__(ticker, company_name)
        self.feed_url = feed_url
    def fetch_headlines(self, days_back: int) -> pd.DataFrame:
        feed = feedparser.parse(self.feed_url)
        return self._clean_response(feed.entries, days_back)
    def _clean_response(self, raw_data, days_back: int) -> pd.DataFrame:
        rows = []
        for entry in raw_data:
            headline = entry.title
            date_obj = date(
                entry.published_parsed.tm_year,
                entry.published_parsed.tm_mon,
                entry.published_parsed.tm_mday
            )
            source = urlparse(entry.link).netloc.replace("www.", "")
            if self._is_within_date_range(date_obj, days_back):
                rows.append({"date": date_obj, "headline": headline, "source": source})
        return pd.DataFrame(rows)

if __name__ == "__main__":
    scraper = RssScraper(
        ticker="AAPL",
        company_name="Apple",
        feed_url="https://feeds.finance.yahoo.com/rss/2.0/headline?s=AAPL"
    )
    df = scraper.fetch_headlines(days_back=7)
    print(df)
    print(f"\nShape: {df.shape}")