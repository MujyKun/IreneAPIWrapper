import asyncio
from typing import List

from IreneAPIWrapper.models import DEVELOPER, IreneAPIClient


class Example:
    def __init__(self):
        self.client = IreneAPIClient(token="test", user_id=169401247374376960)

    async def run(self):
        asyncio.run_coroutine_threadsafe(self.client.connect(), loop)

        while not self.client.connected:
            await asyncio.sleep(0)

        print("Connected to IreneAPI")
        await self.test()

    async def test(self):
        from IreneAPIWrapper.models import TwitterAccount, Channel, Person, Group, GroupAlias

        # persons = await Person.get(1)
        await asyncio.sleep(10)
        groups: List[Group] = await Group.get_all()
        group: Group = await Group.get(1)
        group.affiliations


        print("HERE")

        """
        pham = await User.get(429779375072870400)
        await pham.add_token("test", DEVELOPER)
        print("here")
        """

        while True:
            await asyncio.sleep(60)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Example().run())

