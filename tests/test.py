from typing import Dict
from unittest import TestCase, main
import asyncio

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.models import IreneAPIClient, CallBack


"""
Test the routes for IreneAPI.

The requests will be inserted into the queue before the websocket connection is created.
Then, they will all be run at once and have the connection closed.
The CallBack objects are then compared to check for the expected results.
"""

test_requests = {
    'patron_status': [
        {'route': 'user/patron_status', 'user_id': 169401247374376960, 'method': 'GET', 'callback_id': 1},
        {'route': 'user/patron_status', 'user_id': 169401247374376960, 'method': 'POST', 'callback_id': 2},
        {'route': 'user/patron_status', 'user_id': 169401247374376960, 'method': 'GET', 'callback_id': 3},
        {'route': 'user/patron_status', 'user_id': 169401247374376960, 'method': 'DELETE', 'callback_id': 4},
        {'route': 'user/patron_status', 'user_id': 169401247374376960, 'method': 'GET', 'callback_id': 5},
        ],
    'ban_status': [
        {'route': 'user/ban_status', 'user_id': 169401247374376960, 'method': 'GET', 'callback_id': 6},
        {'route': 'user/ban_status', 'user_id': 169401247374376960, 'method': 'POST', 'callback_id': 7},
        {'route': 'user/ban_status', 'user_id': 169401247374376960, 'method': 'GET', 'callback_id': 8},
        {'route': 'user/ban_status', 'user_id': 169401247374376960, 'method': 'DELETE', 'callback_id': 9},
        {'route': 'user/ban_status', 'user_id': 169401247374376960, 'method': 'GET', 'callback_id': 10},
        ],
}

_callbacks: Dict[int, CallBack] = dict()


async def add_tests(client):
    # add all callbacks to the queue
    for key, requests in test_requests.items():
        for request in requests:
            callback = CallBack(request=request)
            _callbacks[callback.id] = callback
            await client.add_to_queue(callback)

async def check_tests():
    for callback in _callbacks.values():
        ...



class Tests(TestCase):
    def test_routes(self):
        loop = asyncio.get_event_loop()
        try:
            t_token = "test"
            t_user_id = 169401247374376960
            test_instance = Tests()
            client = IreneAPIClient(t_token, t_user_id, test=True)
            loop.run_until_complete(add_tests(client))
            self.assertEqual(True, False)
            loop.run_until_complete(client.connect())
        except KeyboardInterrupt:
            ...
            print("interrupt")
            # loop.run_until_complete(self.close())
            # cancel all tasks lingering
        finally:
            loop.close()


if __name__ == '__main__':
    main()
