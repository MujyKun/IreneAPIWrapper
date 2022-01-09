import asyncio
from IreneAPIWrapper.models import DEVELOPER, IreneAPIClient


class Example:
    def __init__(self):
        self.client = IreneAPIClient(token="test", user_id=169401247374376960)

    async def run(self):
        asyncio.run_coroutine_threadsafe(self.client.connect(), loop)

        while not self.client.connected:
            print(0)
            await asyncio.sleep(0)
        print(1)

        print("Connected to IreneAPI")
        await self.test()

    async def test(self):
        from IreneAPIWrapper.models import TwitterAccount, Channel, Person

        # twitter_accs = await TwitterAccount.fetch_all_accounts()
        person = await Person.get(1)

        # twitter_acc: TwitterAccount = await TwitterAccount.get("mujykun")
        # accounts = await TwitterAccount.fetch_all_accounts()
        print('here')
        # channel = await Channel.get(689684459083137092)
        # await twitter_acc.subscribe(channel=channel)



        """
        pham = await User.get(429779375072870400)
        await pham.add_token("test", DEVELOPER)
        print("here")
        """


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Example().run())

