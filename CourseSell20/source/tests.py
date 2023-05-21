from django.test import TestCase

from requests import post

response = post(
    "https://api.igdb.com/v4/artworks",
    **{
        "headers": {
            "Client-ID": "2m1av7jtmdrwx1ocbrlep22c3s4vtg",
            "Authorization": "s4osmg83f26wwqrryvizowzrtkfuln",
        },
        "data": "fields alpha_channel,animated,checksum,game,height,image_id,url,width;",
    }
)
print("response: %s" % str(response.json()))
