from typing import List
import openai
import httpx
from agents import Runner


class RagPlug(object):
    def __init__(self,
                 endpoint_url: str,
                 api_key: str):
        super().__init__()
        self.endpoint_url = endpoint_url
        self.api_key = api_key

    def search(self, messages):
        pass

    async def asearch(self, messages):
        pass

    def add(self, messages: List[dict]):
        pass

    async def aadd(self, messages: List[dict]):
        pass
