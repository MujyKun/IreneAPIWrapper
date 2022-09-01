from dataclasses import dataclass


@dataclass
class Preload:
    r"""
    Represents which attributes are loaded up on client startup.

    Attributes
    ----------
    tags: bool
        Whether to preload all cache for tags (Defaults to True).
    person_aliases: bool
        Whether to preload all cache for person_aliases (Defaults to True).
    group_aliases: bool
        Whether to preload all cache for group_aliases (Defaults to True).
    persons: bool
        Whether to preload all cache for persons (Defaults to True).
    groups: bool
        Whether to preload all cache for groups (Defaults to True).
    twitter_accounts: bool
        Whether to preload all cache for twitter_accounts (Defaults to True).
    users: bool
        Whether to preload all cache for users (Defaults to False).
    guilds: bool
        Whether to preload all cache for guilds (Defaults to False).
    affiliations: bool
        Whether to preload all cache for affiliations (Defaults to True).
    bloodtypes: bool
        Whether to preload all cache for bloodtypes (Defaults to True).
    media: bool
        Whether to preload all cache for media (Defaults to True).
    displays: bool
        Whether to preload all cache for displays (Defaults to True).
    companies: bool
        Whether to preload all cache for companies (Defaults to True).
    dates: bool
        Whether to preload all cache for dates (Defaults to True).
    locations: bool
        Whether to preload all cache for locations (Defaults to True).
    positions: bool
        Whether to preload all cache for positions (Defaults to True).
    socials: bool
        Whether to preload all cache for socials (Defaults to True).
    fandoms: bool
        Whether to preload all cache for fandoms (Defaults to True).
    channels: bool
        Whether to preload all text channels (Defaults to False).
    twitch_subscriptions: bool
        Whether to preload all twitch subscriptions (Defaults to False).
    twitter_subscriptions: bool
        Whether to preload all twitter subscriptions (Defaults to False).
    languages: bool
        Whether to preload all languages (Defaults to True)
    eight_ball_responses: bool
        Whether to preload all 8ball responses (Defaults to True)
    notifications: bool
        Whether to preload all user notifications (Defaults to True)
    """
    tags = True,
    person_aliases = True,
    group_aliases = True,
    persons = True,
    groups = True,
    twitter_accounts = True,
    users = False,
    guilds = False,
    affiliations = True,
    bloodtypes = True,
    media = True,
    displays = True,
    companies = True,
    dates = True,
    locations = True,
    positions = True,
    socials = True,
    fandoms = True,
    channels = False
    twitch_subscriptions = False
    twitter_subscriptions = False
    languages = True
    eight_ball_responses = True
    notifications = True

    def get_evaluation(self):
        from . import (
            Tag,
            PersonAlias,
            GroupAlias,
            Affiliation,
            BloodType,
            Media,
            Display,
            Company,
            Date,
            Location,
            Position,
            Social,
            Person,
            User,
            Channel,
            Group,
            Fandom,
            Guild,
            TwitchAccount,
            TwitterAccount,
            Language,
            EightBallResponse,
            Notification
        )
        eval_dict = {
            Tag: self.tags,
            PersonAlias: self.person_aliases,
            GroupAlias: self.group_aliases,
            Affiliation: self.affiliations,
            BloodType: self.bloodtypes,
            Media: self.media,
            Display: self.displays,
            Company: self.companies,
            Date: self.dates,
            Location: self.locations,
            Position: self.positions,
            Social: self.socials,
            Fandom: self.fandoms,
            Person: self.persons,
            Group: self.groups,
            User: self.users,
            Guild: self.guilds,
            Channel: self.channels,
            TwitchAccount: self.twitch_subscriptions,
            TwitterAccount: self.twitter_accounts,
            Language: self.languages,
            EightBallResponse: self.eight_ball_responses,
            Notification: self.notifications
        }
        return eval_dict

    def all_false(self):
        self.tags = False
        self.person_aliases = False
        self.group_aliases = False
        self.persons = False
        self.groups = False
        self.twitter_accounts = False
        self.users = False
        self.guilds = False
        self.affiliations = False
        self.bloodtypes = False
        self.media = False
        self.displays = False
        self.companies = False
        self.dates = False
        self.locations = False
        self.positions = False
        self.socials = False
        self.fandoms = False
        self.channels = False
        self.twitch_subscriptions = False
        self.twitter_subscriptions = False
        self.languages = False
        self.eight_ball_responses = False
        self.notifications = False

