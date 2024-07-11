from datetime import date, datetime, timezone
from typing import Optional

COMMON_TIMESTAMP_FORMAT = '%a, %d %b %Y %H:%M:%S %Z'


def convert_to_timestamp(date_string: Optional[str]) -> Optional[datetime]:
    """
    Convert a string to a timestamp.

    :param date_string: str
    :return: Optional[date]
    """
    return datetime.strptime(date_string, COMMON_TIMESTAMP_FORMAT) if date_string else None


def convert_to_date(date_string: Optional[str]) -> Optional[date]:
    """
    Convert a string to a date.

    :param date_string: str
    :return: Optional[date]
    """
    timestamp = convert_to_timestamp(date_string)
    if timestamp:
        return timestamp.date()


def convert_to_common_timestring(timestamp: datetime):
    """
    Convert a timestamp to a common format.

    :param timestamp: datetime
    :returns: datetime
    """
    if not timestamp:
        return None

    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)

    return timestamp.strftime(COMMON_TIMESTAMP_FORMAT)


from .access import Access, GOD, OWNER, DEVELOPER, SUPER_PATRON, FRIEND, USER
from .difficulty import get_difficulty, Difficulty, EASY, MEDIUM, HARD
from .callback import CallBack, callbacks
from .base import (
    internal_fetch_all,
    internal_fetch,
    internal_delete,
    internal_insert,
    AbstractModel,
    MediaSource,
    Alias,
    File,
    basic_call,
)
from .statsupdater import StatsUpdater
from .reactionrolemessages import ReactionRoleMessage
from .interactions import Interaction, InteractionType
from .biasgame import BiasGame
from .eightball import EightBallResponse
from .urban import Urban
from .wolfram import Wolfram
from .reminder import Reminder
from .tag import Tag
from .groupalias import GroupAlias
from .personalias import PersonAlias
from .company import Company
from .location import Location
from .automedia import AutoMedia, AffiliationTime
from .position import Position
from .social import Social
from .display import Display
from .fandom import Fandom
from .banphrase import BanPhrase
from .notification import Notification
from .name import Name
from .group import Group
from .person import Person
from .affiliation import Affiliation
from .media import Media
from .user import User
from .guild import Guild
from .channel import Channel
from .language import Language, PackMessage
from .subscription import Subscription
from .tiktokaccount import TikTokAccount
from .twitchaccount import TwitchAccount
from .preloadcache import Preload
from .client import IreneAPIClient
from .guessinggame import GuessingGame
from .unscramblegame import UnscrambleGame
from .userstatus import UserStatus
from .mode import Mode, NORMAL, GROUP
