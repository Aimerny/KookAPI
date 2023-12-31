from enum import Enum


class Event:
    author_id:str = None
    nickname: str = None
    username:str = None
    channel_type:str = None
    type:int = None
    content:str = None
    channel_name:str = None
    raw_content:str = None
    channel_id:str = None

    def __str__(self):
        return f"Event(author_id={self.author_id}, nickname={self.nickname}, " \
               f"channel_type={self.channel_type}, type={self.type}, " \
               f"content={self.content}, channel_name={self.channel_name}, " \
               f"raw_content={self.raw_content}, channel_id={self.channel_id}," \
               f"username={self.username})"

class ChannelType(Enum):
    GROUP = "GROUP"
    PERSON = "PERSON"
    BROADCAST = "BROADCAST"

class MessageType(Enum):
    TEXT = 1
    PICTURE = 2
    VIDEO = 3
    FILE = 4
    AUDIO = 8
    K_MARKDOWN = 9
    CARD = 10
    SYSTEM = 255

