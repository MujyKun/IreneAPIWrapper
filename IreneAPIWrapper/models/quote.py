from . import basic_call


class Quote:
    def __init__(self, quote, author):
        self.quote = quote
        self.author = author

    @staticmethod
    async def get_quote_of_day():
        callback = await basic_call(
            request={
                "route": "bot/dailystatus",
                "method": "GET",
            }
        )
        results = callback.response.get("results") or {}
        quote = results.get("quote")
        author = results.get("author")
        return Quote(quote, author)
