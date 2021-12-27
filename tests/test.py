from unittest import TestCase, main
import asyncio

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.models import IreneAPIClient, CallBack


async def add_tests(client):
    ...


class Tests(TestCase):
    def run_tests(self):
        loop = asyncio.get_event_loop()
        try:
            t_token = "test"
            t_user_id = 169401247374376960
            test_instance = Tests()
            client = IreneAPIClient(t_token, t_user_id, test=test_instance)
            loop.run_until_complete(add_tests(client))
            loop.run_until_complete(client.connect())
        except KeyboardInterrupt:
            ...
            print("interrupt")
            # loop.run_until_complete(self.close())
            # cancel all tasks lingering
        finally:
            loop.close()


"""
class UserTests(unittest.TestCase):

    async def add_to_queue(self):
    def test_patron_status(self):
        self.assertEqual(True, False)
"""


test_requests = {
    'patron_status': [
        {'route': 'user/patron_status', 'user_id': 169401247374376960, 'method': 'GET', 'callback_id': 1},
        {'route': 'user/patron_status', 'user_id': 169401247374376960, 'method': 'POST', 'callback_id': 1},
        {'route': 'user/patron_status', 'user_id': 169401247374376960, 'method': 'GET', 'callback_id': 1},
        {'route': 'user/patron_status', 'user_id': 169401247374376960, 'method': 'DELETE', 'callback_id': 1},
        {'route': 'user/patron_status', 'user_id': 169401247374376960, 'method': 'GET', 'callback_id': 1},
        ],
    'ban_status': [
        {'route': 'user/ban_status', 'user_id': 169401247374376960, 'method': 'GET', 'callback_id': 1},
        {'route': 'user/ban_status', 'user_id': 169401247374376960, 'method': 'POST', 'callback_id': 1},
        {'route': 'user/ban_status', 'user_id': 169401247374376960, 'method': 'GET', 'callback_id': 1},
        {'route': 'user/ban_status', 'user_id': 169401247374376960, 'method': 'DELETE', 'callback_id': 1},
        {'route': 'user/ban_status', 'user_id': 169401247374376960, 'method': 'GET', 'callback_id': 1},
        ],
}


if __name__ == '__main__':
    main()
