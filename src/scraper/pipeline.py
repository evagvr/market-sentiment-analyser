import pandas as pd
from base import BaseScraper
from datetime import datetime

class ScraperPipeline:
    def __init__(self, ticker: str, company_name: str):
        self.ticker = ticker
        self.company_name = company_name
        self.sources = []
    def add_source(self, scraper: BaseScraper):
        self.sources.append(scraper)
    def fetch_all(self, days_back: int) -> pd.DataFrame:
        all_dfs = []
        for scraper in self.sources:
            try:
                df = scraper.fetch_headlines(days_back)
                all_dfs.append(df)
            except Exception as e:
                print(f"Warning scraper: {scraper.__class__.__name__} failed: {e}")
                continue
        if not all_dfs:
            raise RuntimeError("All scrapers failed, no data collected.")
        combined = pd.concat(all_dfs, ignore_index=True)
        combined = combined.drop_duplicates(subset=["headline"])
        combined = combined.sort_values("date", ascending=False)
        combined = combined.reset_index(drop=True)
        return combined
    def save_raw(self, df: pd.DataFrame):
        filename = f"data/raw/{self.ticker}_{datetime.now().strftime('%Y%m%d')}.csv"
        df.to_csv(filename, index=False)
        print(f"Saved to {filename}")


if __name__ == "__main__":
    from rss_scraper import RssScraper

    pipeline = ScraperPipeline(ticker="AAPL", company_name="Apple")

    pipeline.add_source(RssScraper(
        ticker="AAPL",
        company_name="Apple",
        feed_url="https://feeds.finance.yahoo.com/rss/2.0/headline?s=AAPL"
    ))
    pipeline.add_source(RssScraper(
        ticker="AAPL",
        company_name="Apple",
        feed_url="https://feeds.reuters.com/reuters/businessNews"
    ))

    df = pipeline.fetch_all(days_back=7)
    print(df.to_string())
    print(f"\nShape: {df.shape}")