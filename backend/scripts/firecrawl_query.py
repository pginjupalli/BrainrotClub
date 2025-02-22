from firecrawl import FirecrawlApp
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("FIRECRAWL_API_KEY")

app = FirecrawlApp(api_key=api_key)

# Crawl a website:
crawl_status = app.crawl_url(
  'https://firecrawl.dev', 
  params={
    'limit': 100, 
    'scrapeOptions': {'formats': ['markdown', 'html']}
  },
  poll_interval=1
)
print(crawl_status)
