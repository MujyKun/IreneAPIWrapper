from . import basic_call


class BiasGame:
    def __init__(self):
        ...

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

