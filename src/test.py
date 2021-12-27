import datetime
from asyncio import sleep
from models import CallBack


async def run(client):
    while True:
        current_time = datetime.datetime.now()

        for i in range(1, 10):
            for route, requests in test_requests.items():
                for count, request in enumerate(requests):
                    callback = CallBack(request=request)
                    await client.add_to_queue(callback)
                    await callback.wait_for_completion()
                    assert callback.response.get('error') is None
                    if count in [0, 4]:
                        assert callback.response.get('result') is False
                    elif count in [1, 3]:
                        assert callback.response.get('result') == ''
                    elif count == 2:
                        assert callback.response.get('result')
                    else:
                        assert False is True
                    # print(f"REQUEST: {callback.request}")
                    # print(f"RESPONSE: {callback.response}")
        end_time = datetime.datetime.now()
        print(f"FINISHED IN: {end_time-current_time}")
        await sleep(10)

