import signal  
import sys  
import asyncio  
import aiohttp  
import json
from django_cron import CronJobBase, Schedule


class LoadPosts(CronJobBase):
  schedule = Schedule(run_every_mins=720) # every 12 hours
  code = 'facebook_news_scraper.load_posts'

  async def fetch(session, url):
    async with async_timeout.timeout(10):
      async with session.get(url) as response:
        return await response.text()

  async def main():
    async with aiohttp.ClientSession() as session:
      html = await fetch(session, 'http://python.org')
      print(html)

  def do(self):
    # Algorithm: 
      # For each page -> THREADED
        # Load posts, following pagination until we hit one already loaded
      # For each post without likes -> THREADED
      # For each post without comments -> THREADED

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    