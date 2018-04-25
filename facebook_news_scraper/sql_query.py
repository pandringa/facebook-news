all_posts_query = '''
  SELECT "facebook_news_scraper_post"."id" AS fb_id,
  "facebook_news_scraper_page"."slug" AS page,
  "facebook_news_scraper_post"."share_count" AS share_count,
  "facebook_news_scraper_post"."like_count" AS like_count,
  "facebook_news_scraper_post"."love_count" AS love_count,
  "facebook_news_scraper_post"."wow_count" AS wow_count,
  "facebook_news_scraper_post"."haha_count" AS haha_count,
  "facebook_news_scraper_post"."sad_count" AS sad_count,
  "facebook_news_scraper_post"."angry_count" AS angry_count,
  "facebook_news_scraper_post"."comment_count" AS comment_count,
  "facebook_news_scraper_post"."posted_at" AS date,
  "facebook_news_scraper_article"."resolved_url" AS url,
  "facebook_news_scraper_article"."category" AS category

  FROM "facebook_news_scraper_post"

  INNER JOIN "facebook_news_scraper_article" ON ("facebook_news_scraper_post"."article_id" = "facebook_news_scraper_article"."id")

  INNER JOIN "facebook_news_scraper_page" ON ("facebook_news_scraper_post"."page_id" = "facebook_news_scraper_page"."id")

  WHERE (NOT ("facebook_news_scraper_post"."page_id" IN ('21898300328', '228735667216', '97212224368', '10513336322', '273864989376427'))
  AND NOT ("facebook_news_scraper_article"."category" IS NULL)
  AND NOT ("facebook_news_scraper_article"."category" = 'local'
  AND "facebook_news_scraper_article"."category" IS NOT NULL))
  AND "facebook_news_scraper_post"."posted_at" >= '2018-03-01 00:00:00+00:00'
  ORDER BY date ASC
'''

def stream_csv(columns, cursor):
  yield ",".join(columns)+"\n"
  while True:
    row = cursor.fetchone()
    if row:
      yield ",".join([str(r) for r in row])+"\n"
    else:
      break
  cursor.close()


march_april_query = all_posts_query + '''AND "facebook_news_scraper_post"."posted_at" <= '2018-05-01 00:00:00+00:00')'''