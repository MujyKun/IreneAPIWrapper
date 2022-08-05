from . import basic_call


class BiasGame:
    def __init__(self):
        ...

    @staticmethod
    async def fetch_winners(user_id, limit=15) -> dict:
        """
        Fetch the winners of a user's bias game.

        :param user_id: int
            User ID to return results for.
        :param limit: int
            Number of results should be retrieved in descending order.
        :return: dict
            Dictionary of person IDs to the amount of times they've won.
        """
        callback = await basic_call(request={
            'route': 'biasgame/winners',
            'user_id': user_id,
            'limit': limit,
            'method': 'POST'
        })
        return callback.response.get("results")

    @staticmethod
    async def generate_pvp(first_file_name, second_file_name):
        """
        Generate a PvP image and return an image url.

        :param first_file_name: str
            The first image file name.
        :param second_file_name: str
            The second image file name.
        :return: str
            The PvP image url.
        """
        callback = await basic_call(request={
            'route': 'biasgame/generate_pvp',
            'first_file_name': first_file_name,
            'second_file_name': second_file_name,
            'method': 'POST'
        })
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
        callback = await basic_call(request={
            'route': 'biasgame/generate_bracket',
            'game_info': game_info,
            'method': 'POST'
        })
        return callback.response.get("results")