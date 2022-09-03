from . import basic_call


class BiasGame:
    def __init__(self):
        ...

    @staticmethod
    async def upsert_win(user_id, person_id) -> None:
        """
        Upsert a win for a user's BiasGame.

        :param user_id: int
            User ID of the bias game player.
        :param person_id: int
            Person ID that won the bias game.
        :return: None
        """
        await basic_call(
            request={
                "route": "biasgame/winners",
                "user_id": user_id,
                "person_id": person_id,
                "method": "PUT",
            }
        )

    @staticmethod
    async def fetch_winners(user_id, limit=15) -> dict:
        """
        Fetch the winners of a user's bias game in DESC order.

        :param user_id: int
            User ID to return results for.
        :param limit: int
            Number of results should be retrieved in descending order.
        :return: dict
            Dictionary of person IDs to the amount of times they've won.
        """
        callback = await basic_call(
            request={
                "route": "biasgame/winners",
                "user_id": user_id,
                "limit": limit,
                "method": "POST",
            }
        )
        return callback.response.get("results")

    @staticmethod
    async def generate_pvp(first_image_url, second_image_url):
        """
        Generate a PvP image and return an image url.

        :param first_image_url: str
            The first image url.
        :param second_image_url: str
            The second image url.
        :return: str
            The PvP image url.
        """
        callback = await basic_call(
            request={
                "route": "biasgame/generate_pvp",
                "first_image_url": first_image_url,
                "second_image_url": second_image_url,
                "method": "POST",
            }
        )
        return callback.response.get("results")

    @staticmethod
    async def generate_bracket(game_info):
        """
        Generate a PvP bracket and return an image url.

        :param game_info: dict
            All BiasGame round(s) information.
        :return: str
            The BiasGame bracket image url.
        """
        callback = await basic_call(
            request={
                "route": "biasgame/generate_bracket",
                "game_info": game_info,
                "method": "POST",
            }
        )
        return callback.response.get("results")
