from . import (
    basic_call
)


class StatsUpdater:
    """
    Class that handles the update of statistics to the API.

    """
    @staticmethod
    async def update(key, value):
        """Update a stat value in the API."""
        await basic_call(
            request={
                "route": "bot/updatestats",
                "key": key,
                "value": value,
                "method": "PUT"
            }
        )

