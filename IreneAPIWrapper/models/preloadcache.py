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
            TwitterAccount,
            User,
            Channel,
            Group,
            Fandom,
            Guild,
            TwitchAccount
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
            TwitterAccount: self.twitter_accounts,
            User: self.users,
            Guild: self.guilds,
            Channel: self.channels,
            TwitchAccount: self.twitch_subscriptions
        }
        return eval_dict