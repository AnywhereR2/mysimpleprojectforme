# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2
from datetime import datetime
from scrapy.utils.project import get_project_settings


class ScrapinonlinerScraperPipeline:

    def open_spider(self, spider):
        settings = get_project_settings()
        self.conn = psycopg2.connect(settings["POSTGRES_URI"])
        self.cur  = self.conn.cursor()

        # ── создаём таблицу, если её ещё нет ──────────────────────────────
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS onliner_flats (
                flat_id          BIGINT,
                author_id        BIGINT,
                address          TEXT,
                user_address     TEXT,
                latitude         DOUBLE PRECISION,
                longitude        DOUBLE PRECISION,
                price_usd        NUMERIC,
                price_byn        NUMERIC,
                original_price   NUMERIC,
                currency         TEXT,
                resale           BOOLEAN,
                rooms            INT,
                floor            INT,
                floors_total     INT,
                area_total       NUMERIC,
                area_living      NUMERIC,
                seller_type      TEXT,
                created_at       TIMESTAMPTZ,
                last_time_up     TIMESTAMPTZ,
                up_available_in  INT,
                auction_bid_amount    NUMERIC,
                auction_bid_currency  TEXT,
                url              TEXT,
                run_ts           TIMESTAMPTZ NOT NULL
            );
            """
        )
        self.conn.commit()

        # фиксируем единое время запуска паука
        self.run_ts = datetime.utcnow()

    def process_item(self, item, spider):
        # вставляем строку без каких-либо ограничений уникальности
        self.cur.execute(
            """
            INSERT INTO onliner_flats (
                flat_id, author_id, address, user_address, latitude, longitude,
                price_usd, price_byn, original_price, currency,
                resale, rooms, floor, floors_total, area_total, area_living,
                seller_type, created_at, last_time_up, up_available_in,
                auction_bid_amount, auction_bid_currency, url, run_ts
            ) VALUES (
                %(id)s, %(author_id)s, %(address)s, %(user_address)s,
                %(latitude)s, %(longitude)s, %(price_usd)s, %(price_byn)s,
                %(original_price)s, %(currency)s, %(resale)s,
                %(rooms)s, %(floor)s, %(floors_total)s, %(area_total)s,
                %(area_living)s, %(seller_type)s, %(created_at)s,
                %(last_time_up)s, %(up_available_in)s,
                %(auction_bid_amount)s, %(auction_bid_currency)s, %(url)s,
                %(run_ts)s
            );
            """,
            {**item, "run_ts": self.run_ts},
        )
        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()