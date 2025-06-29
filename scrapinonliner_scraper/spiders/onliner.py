import scrapy
import json

class OnlinerSpider(scrapy.Spider):
    name = "onliner"
    allowed_domains = ["r.onliner.by"]
    start_urls = ["https://r.onliner.by/sdapi/pk.api/search/apartments?page=1"]

    def parse(self, response):
        try:
            data = json.loads(response.text)
        except json.JSONDecodeError:
            self.logger.error("Ошибка при разборе JSON")
            return

        for a in data.get("apartments", []):
            yield {
                "id": a.get("id"),
                "author_id": a.get("author_id"),
                "address": a.get("location", {}).get("address"),
                "user_address": a.get("location", {}).get("user_address"),
                "latitude": a.get("location", {}).get("latitude"),
                "longitude": a.get("location", {}).get("longitude"),
                "price_usd": a.get("price", {}).get("converted", {}).get("USD", {}).get("amount"),
                "price_byn": a.get("price", {}).get("converted", {}).get("BYN", {}).get("amount"),
                "original_price": a.get("price", {}).get("amount"),
                "currency": a.get("price", {}).get("currency"),
                "photo": a.get("photo"),
                "resale": a.get("resale"),
                "rooms": a.get("number_of_rooms"),
                "floor": a.get("floor"),
                "floors_total": a.get("number_of_floors"),
                "area_total": a.get("area", {}).get("total"),
                "area_living": a.get("area", {}).get("living"),
                "seller_type": a.get("seller", {}).get("type"),
                "created_at": a.get("created_at"),
                "last_time_up": a.get("last_time_up"),
                "up_available_in": a.get("up_available_in"),
                "auction_bid_amount": a.get("amount"),
                "auction_bid_currency": a.get("currency"),
                "url": a.get("url")
            }

        # Переход к следующей странице
        current_page = int(response.url.split("page=")[-1])
        last_page = data.get("page", {}).get("last")

        if last_page and current_page < last_page:
            next_page = current_page + 1
            next_url = f"https://r.onliner.by/sdapi/pk.api/search/apartments?page={next_page}"
            yield scrapy.Request(url=next_url, callback=self.parse)