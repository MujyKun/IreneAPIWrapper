from . import basic_call


class Wolfram:
    """
    A model for sending requests to WolframAlpha.
    """

    @staticmethod
    async def query(query):
        """Query a request to Wolfram."""
        callback = await basic_call(
            request={"route": "wolfram/", "query": query, "method": "POST"}
        )
        return callback.response.get("results")
