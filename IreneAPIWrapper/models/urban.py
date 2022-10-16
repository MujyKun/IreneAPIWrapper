from . import basic_call


class Urban:
    """
    A model for sending requests to UrbanDictionary.
    """

    @staticmethod
    async def query(phrase):
        """
        Query a request to UrbanDictionary.

        :param phrase: str
            The phrase to query UrbanDictionary with
        :return:
        """
        callback = await basic_call(
            request={"route": "misc/urban", "phrase": phrase, "method": "POST"}
        )
        return callback.response.get("results")
