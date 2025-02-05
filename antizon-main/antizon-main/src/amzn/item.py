import requests
from .schemes import amznProduct

class AMZN:
    def __init__(self, rainforest_api_key: str):
        self.params = {
            "api_key": rainforest_api_key,
            "type": "offers",
            "amazon_domain": "amazon.com",
            "output": "json",
            "include_html": "false",
            "language": "en_US"
        }

    def get_item(self, asin: str) -> amznProduct:
        """Returns item metadata from ASIN"""
        self.params.update({"asin": asin})
        with requests.get("https://api.rainforestapi.com/request", self.params, stream=True) as res:
            self.params.pop("asin")
            content = res.json()
            info = content["request_info"]
            # print(content)
            if info["success"] == True:
                product = content["product"]
                offers = content["offers"]
                return amznProduct(product["title"], offers[0]["price"]["value"], asin)
            else:
                return {"message": info["message"]}

