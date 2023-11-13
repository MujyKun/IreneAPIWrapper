from typing import Dict, Type


class Preload:
    force: bool = True
    tags = person_aliases = group_aliases = persons = groups = \
        affiliations = bloodtypes = media = displays = companies = dates = locations = \
        positions = socials = fandoms = languages = eight_ball_responses = notifications = \
        interactions = names = auto_media = reminders = reaction_role_messages = banned_phrases = True

    users = guilds = channels = twitch_subscriptions = \
        tiktok_subscriptions = False

    def get_evaluation(self) -> Dict[Type, bool]:
        from . import (
            Tag, PersonAlias, GroupAlias, Affiliation, BloodType, Media, Display, Company, Date, Location, Position,
            Social, Person, User, Channel, Group, Fandom, Guild, TwitchAccount, Language,
            EightBallResponse, Notification, Interaction, Name, AutoMedia, Reminder, ReactionRoleMessage, TikTokAccount,
            BanPhrase
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
            Language: self.languages,
            EightBallResponse: self.eight_ball_responses,
            Notification: self.notifications,
            Interaction: self.interactions,
            Name: self.names,
            AutoMedia: self.auto_media,
            Reminder: self.reminders,
            ReactionRoleMessage: self.reaction_role_messages,
            TikTokAccount: self.tiktok_subscriptions,
            BanPhrase: self.banned_phrases
        }

        return {key: val for key, val in eval_dict.items() if key}

    def all_false(self) -> None:
        for attr in self.__annotations__:
            if attr == 'force':
                continue
            setattr(self, attr, False)
