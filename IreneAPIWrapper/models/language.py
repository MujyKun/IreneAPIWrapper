from typing import List, Dict, Optional

from . import AbstractModel
from . import internal_fetch_all
from IreneAPIWrapper.exceptions import IncorrectNumberOfItems
from json import loads


class PackMessage:
    """
    Refers to a message in a language.

    Parameters
    ----------
    language_id: int
        The :ref:`Language` ID that the message belongs to.
    label: str
        The key that identifies the message.
    message: str
        The message that may have custom input.
    num_inputs: int
        The number of custom inputs.

    Attributes
    ----------
    language_id: int
        The :ref:`Language` ID that the message belongs to.
    label: str
        The key that identifies the message.
    message: str
        The message that may have custom input.
    num_inputs: int
        The number of custom inputs.
    """

    def __init__(self, language_id, label, message, num_inputs):
        self.language_id = language_id
        self.label = label
        self.message = message
        self.num_inputs: int = num_inputs

    @staticmethod
    async def create(dict_info):
        language_id = dict_info["languageid"]
        label = dict_info["label"]
        message = dict_info["message"]
        num_inputs = await PackMessage.get_input_count(message)
        return PackMessage(language_id, label, message, num_inputs)

    def get(self, *args) -> str:
        """Get the message formatted with custom input.

        Pass in as many strings as inputs are required.
        """
        if len(args) < self.num_inputs:
            raise IncorrectNumberOfItems(
                f"There are not enough arguments passed in to {self.language_id}.{self.label}"
            )
        elif len(args) > self.num_inputs:
            raise IncorrectNumberOfItems(
                f"There are too many arguments passed in to {self.language_id}.{self.label}"
            )

        msg = self.message
        for idx, arg in enumerate(args, start=1):
            arg_as_string = f"{arg}"
            start_input = msg.find(f":{idx}$")
            end_input = msg.find(f"${idx}:") + len(f"{idx}") + 2
            msg_list = [char for char in msg]
            msg = (
                "".join(msg_list[0:start_input])
                + arg_as_string
                + "".join(msg_list[end_input::])
            )
        return msg

    @staticmethod
    async def get_input_count(msg: str) -> int:
        """
        Get the amount of inputs in a message.

        :param msg: str
            The message to check.
        :return: int
            The number of inputs in the input message.
        """
        i = 1
        while True:
            # start of input
            if msg.find(f":{i}$") == -1:
                i -= 1
                break
            # end of input
            if msg.find(f"${i}:") == -1:
                i -= 1
                break
            i += 1
        return i


class Language(AbstractModel):
    """
    Refers to a language.

    A Language object inherits from :ref:`AbstractModel`.

    Parameters
    ----------
    language_id: int
        The language's unique ID.
    short_name: str
        The shorthand version of the language's name.
    name: str
        The official name of the language.
    pack: List[:ref:`PackMessage`]
        A list of PackMessages that belong to the language.

    Attributes
    ----------
    short_name:
    """

    def __init__(self, language_id, short_name, name, pack: List[PackMessage]):
        super(Language, self).__init__(language_id)
        self.short_name = short_name.lower()
        self.name = name
        self._pack: List[PackMessage] = pack

        # organized pack
        self._organized_pack: Dict[str, PackMessage] = {
            _pack.label: _pack for _pack in self._pack
        }

        lang = _langs.get(self.id)
        if not lang:
            _langs_by_short_name[self.short_name] = self
            _langs[self.id] = self

    @staticmethod
    async def create(*args, **kwargs):
        language_id = kwargs.get("languageid")
        short_name = kwargs.get("shortname")
        name = kwargs.get("name")
        _pack = kwargs.get("pack")
        raw_pack: List[dict] = list(loads(_pack)) if _pack else []
        pack = [await PackMessage.create(dict_info) for dict_info in raw_pack]
        Language(language_id, short_name, name, pack)
        return _langs[language_id]

    def __getitem__(self, key) -> Optional[PackMessage]:
        return self._organized_pack.get(key)

    @staticmethod
    def get_english():
        """
        Get the English Language Pack.

        :return: :ref:`Language`
        """
        return _langs_by_short_name["en-us"]

    @staticmethod
    async def fetch_all():
        return await internal_fetch_all(
            Language, request={"route": "language/", "method": "GET"}
        )

    @staticmethod
    def get_lang(short_name: str):
        """
        Get a language by the short name.

        :param short_name: str
            The short name of a language.
        :return: Optional[:ref:`Language`]
            The language object.
        """
        return _langs_by_short_name.get(short_name.lower())

    @staticmethod
    def get_lang_by_id(language_id):
        """
        Get a language by the ID.

        :param language_id: int
            The ID of the language.
        :return: Optional[:ref:`Language`]
            The language object.
        """
        return _langs.get(language_id)


_langs: Dict[int, Language] = dict()
_langs_by_short_name: Dict[str, Language] = dict()
