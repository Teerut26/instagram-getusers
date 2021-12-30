import json
import time

from JsonToObj import GetUserlike

try:
    import urlparse
    from urllib import urlencode
except:  # For Python 3
    import urllib.parse as urlparse
    from urllib.parse import urlencode
import requests

getUserlikeObj = GetUserlike


class GetUserlike:
    def __init__(self, query_hash, cookie, shortcode, after, include_reel=True, first=12, i=0):
        self.query_hash = query_hash
        self.cookie = cookie
        self.shortcode = shortcode
        self.after = after
        self.include_reel = include_reel
        self.first = first
        self.i = i

    def main(self):
        self.variables = json.dumps({
            "shortcode": self.shortcode,
            "include_reel": self.include_reel,
            "first": self.first,
            "after": self.after
        })
        result = getUserlikeObj.json_res_from_dict(json.loads(self.get_data(self.params_to_url())))
        self.end_cursor = result.data.shortcode_media.edge_liked_by.page_info.end_cursor
        self.has_next_page = result.data.shortcode_media.edge_liked_by.page_info.has_next_page

        for item in result.data.shortcode_media.edge_liked_by.edges:
            print(f"[{self.i + 1}] {item.node.username}")
            self.i += 1

    def get_data(self, url):
        payload = {}
        headers = {
            'cookie': self.cookie
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        return response.text

    def params_to_url(self):
        url = "https://www.instagram.com/graphql/query/"
        params = {'query_hash': self.query_hash, 'variables': self.variables}

        url_parts = list(urlparse.urlparse(url))
        query = dict(urlparse.parse_qsl(url_parts[4]))
        query.update(params)

        url_parts[4] = urlencode(query)

        return urlparse.urlunparse(url_parts)


if __name__ == '__main__':
    query_hash = "d5d763b1e2acf209d62d22d184488e57"
    cookie = open("cookie.txt", "r").read()
    shortcode = "Post ID ex. CYA5er1PfNE"
    after = ""
    i = 0

    while True:
        getUserlike = GetUserlike(query_hash, cookie, shortcode, after, first=50, i=i)
        getUserlike.main()

        if (not getUserlike.has_next_page):
            break

        after = getUserlike.end_cursor
        i = getUserlike.i

        # time.sleep(1)
