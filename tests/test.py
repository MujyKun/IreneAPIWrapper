from typing import Dict
from unittest import TestCase, main
import asyncio

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from IreneAPIWrapper.models import IreneAPIClient, CallBack

"""
Test the routes for IreneAPI.

The requests will be inserted into the queue before the websocket connection is created.
Then, they will all be run at once and have the connection closed.
The CallBack objects are then compared to check for the expected results.
"""

m_false = 5
m_none = 9
m_true = 4
m_invalid_cases = [m_false * m_none, m_false * m_true, m_none * m_true]
_callbacks: Dict[int, CallBack] = dict()
_existing_keys = []


def get_test_callback_id(expectation: bool = None) -> int:
    """
    Get a test call back name where the name does not already exist
    and is not a multiple of the below expectation values.

    False = Multiple of 5
    None = Multiple of 9
    True = Multiple of 4

    :param expectation: True/False/None
    :return: (int) The callback name to use for a test.
    """
    callback_id = 0

    while True:
        callback_id += m_true if expectation else m_false if expectation is False else m_none

        if callback_id in _existing_keys:
            continue

        invalid = False
        for case in m_invalid_cases:
            if callback_id % case == 0:
                invalid = True

        if invalid:
            continue

        _existing_keys.append(callback_id)
        return callback_id


test_user_id = 000000000000000000


test_requests = {'requests': [
    # call back ids are multiples of a=5, b=9, or c=4 depending on each scenario.
    # callback_id should not be a multiple of several.
    # check = Check if a case exists.
    # add = add a user for a specific reason or to somewhere specific
    # remove = undo the add.


    # manage a user (check,add,check)
    {'route': 'user/', 'user_id': test_user_id, 'method': 'GET', 'callback_id': get_test_callback_id(None)},
    {'route': 'user/', 'user_id': test_user_id, 'method': 'POST', 'callback_id': get_test_callback_id(True)},
    {'route': 'user/', 'user_id': test_user_id, 'method': 'GET', 'callback_id': get_test_callback_id(True)},

    # manage that user as a patron (check,add,check,delete,check)
    {'route': 'user/patron_status', 'user_id': test_user_id, 'method': 'GET',
     'callback_id': get_test_callback_id(False)},
    {'route': 'user/patron_status', 'user_id': test_user_id, 'method': 'POST',
     'callback_id': get_test_callback_id(True)},
    {'route': 'user/patron_status', 'user_id': test_user_id, 'method': 'GET',
     'callback_id': get_test_callback_id(True)},
    {'route': 'user/patron_status', 'user_id': test_user_id, 'method': 'DELETE',
     'callback_id': get_test_callback_id(True)},
    {'route': 'user/patron_status', 'user_id': test_user_id, 'method': 'GET',
     'callback_id': get_test_callback_id(False)},

    # manage the user's ban status.
    {'route': 'user/ban_status', 'user_id': test_user_id, 'method': 'GET', 'callback_id': get_test_callback_id(False)},
    {'route': 'user/ban_status', 'user_id': test_user_id, 'method': 'POST', 'callback_id': get_test_callback_id(True)},
    {'route': 'user/ban_status', 'user_id': test_user_id, 'method': 'GET', 'callback_id': get_test_callback_id(True)},
    {'route': 'user/ban_status', 'user_id': test_user_id, 'method': 'DELETE',
     'callback_id': get_test_callback_id(True)},
    {'route': 'user/ban_status', 'user_id': test_user_id, 'method': 'GET', 'callback_id': get_test_callback_id(False)},

    # delete the user and make sure they are deleted.
    {'route': 'user/', 'user_id': test_user_id, 'method': 'DELETE', 'callback_id': get_test_callback_id(True)},
    {'route': 'user/', 'user_id': test_user_id, 'method': 'GET', 'callback_id': get_test_callback_id(None)},

]}


async def add_tests(client):
    # add all callbacks to the queue
    for request in test_requests['requests']:
        callback = CallBack(request=request)
        _callbacks[callback.id] = callback
        await client.add_to_queue(callback)


class Tests(TestCase):
    def test_routes(self):
        loop = asyncio.get_event_loop()
        try:
            t_token = "test"
            t_user_id = 169401247374376960
            test_instance = Tests()
            client = IreneAPIClient(t_token, t_user_id, test=True)
            loop.run_until_complete(add_tests(client))
            loop.run_until_complete(client.connect())

            loop.run_until_complete(self.check_for_errors())
            loop.run_until_complete(self.check_for_validity())
        except KeyboardInterrupt:
            ...
            print("interrupt")
            # loop.run_until_complete(self.close())
            # cancel all tasks lingering
        finally:
            loop.close()

    async def check_for_errors(self):
        """Check that the callbacks do not have any error from the API."""
        for callback in _callbacks.values():
            with self.subTest():
                self.assertIsNone(callback.response.get('error'))

    async def check_for_validity(self):
        """Check that the callbacks have an expected response"""
        for callback in _callbacks.values():
            with self.subTest():
                # breakpoint()
                result = callback.response.get('results')
                success = None if result is None else result.get('success')
                if callback.id % m_none == 0:
                    self.assertIsNone(result)
                elif callback.id % m_false == 0:
                    if isinstance(result, dict):
                        for var in result.values():
                            self.assertFalse(bool(var))
                    else:
                        self.assertFalse(bool(var))

                elif callback.id % m_true == 0:
                    self.assertTrue(result if success is None else success)
                else:
                    self.assertEqual(True, False)  # a test was not created properly.


if __name__ == '__main__':
    main()
