from dataclasses import dataclass


@dataclass
class Preload:
    r"""
    Represents which attributes are loaded up on client startup.

    Attributes
    ----------
    force: bool
        Whether to make sure all cache is preloaded. (Defaults to True)
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
    names: bool
        Whether to preload all cache for names (Defaults to True).
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
    interactions: bool
        Whether to preload all interactions (Defaults to True)
    auto_media: bool
        Whether to preload all auto media (Defaults to True)
    """
    tags = person_aliases = group_aliases = persons = groups = twitter_accounts = \
        affiliations = bloodtypes = media = displays = companies = dates = locations = \
        positions = socials = fandoms = languages = eight_ball_responses = notifications = interactions = names = \
        auto_media = reminders = True
    users = guilds = channels = twitch_subscriptions = twitter_subscriptions = False

    force: bool = True

    def get_evaluation(self):
        from . import (
            Tag, PersonAlias, GroupAlias, Affiliation, BloodType, Media, Display, Company, Date, Location, Position,
            Social, Person, User, Channel, Group, Fandom, Guild, TwitchAccount, TwitterAccount, Language,
            EightBallResponse, Notification, Interaction, Name, AutoMedia, Reminder
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
            Notification: self.notifications,
            Interaction: self.interactions,
            Name: self.names,
            AutoMedia: self.auto_media,
            Reminder: self.reminders
        }

        eval_dict_only_true = {key: val for key, val in eval_dict.items() if key}
        return eval_dict_only_true

    def all_false(self):
        self.tags = self.person_aliases = self.group_aliases = self.persons = self.groups = self.twitter_accounts = \
            self.users = self.guilds = self.affiliations = self.bloodtypes = self.media = self.displays = \
            self.companies = self.dates = self.locations = self.positions = self.socials = self.fandoms = \
            self.channels = self.twitch_subscriptions = self.twitter_subscriptions = self.languages = \
            self.eight_ball_responses = self.notifications = self.interactions = self.names = self.auto_media = \
            self.reminders = False
