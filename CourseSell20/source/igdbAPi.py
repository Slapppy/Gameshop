from datetime import datetime

import requests
from django.core.files.base import ContentFile
from source.models import Game


class IGDBAPI:
    def __init__(self):
        self.api_key = "2m1av7jtmdrwx1ocbrlep22c3s4vtg"
        self.base_url = "https://api.igdb.com/v4"

    def search_games(self, query):
        url = f"{self.base_url}/games"
        headers = {
            "Client-ID": self.api_key,
            "Authorization": f"Bearer dpgydk6q3pao2cn953h0ez1fl2p1t2",
        }
        data = f'fields name,genres.name,rating,summary,release_dates.date,cover.url; search "{query}"; limit 10;'
        response = requests.post(url, headers=headers, data=data)
        games = response.json()
        return games

    def add_game_to_database(self, game_id, price):
        url = f"{self.base_url}/games"
        headers = {
            "Client-ID": "2m1av7jtmdrwx1ocbrlep22c3s4vtg",
            "Authorization": f"Bearer dpgydk6q3pao2cn953h0ez1fl2p1t2",
        }
        data = f"fields name,genres.name,rating,summary,release_dates.date,cover.url; where id = {game_id}; limit 1;"
        response = requests.post(url, headers=headers, data=data)
        game_data = response.json()[0]
        release_date_str = game_data.get("release_dates", "")[0]["date"]
        print(game_data)
        print(release_date_str)
        release_date = datetime.fromtimestamp(release_date_str).date()
        game = Game(
            title=game_data.get("name", ""),
            genre=game_data.get("genres")[0].get("name", "")
            if game_data.get("genres")
            else "",
            rating=game_data.get("rating", 0),
            description=game_data.get("summary", ""),
            release_date=release_date,
            price=price,
        )

        # Сохранение картинки
        cover_url = game_data.get("cover", {}).get("url")
        if cover_url:
            if not cover_url.startswith("https://"):
                cover_url = f"https:{cover_url}"
            response = requests.get(cover_url)
            if response.status_code == 200:
                image_content = ContentFile(response.content)
                game.image.save(f"{game_id}.jpg", image_content, save=False)

        game.save()
