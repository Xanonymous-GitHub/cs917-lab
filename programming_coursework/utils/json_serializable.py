from abc import ABCMeta
from dataclasses import asdict, dataclass
from json import JSONEncoder, dumps

__all__ = ["JsonSerializable"]


@dataclass(frozen=True)
class JsonSerializable(JSONEncoder, metaclass=ABCMeta):
    """
    This class provides a blueprint for objects that can be serialized to JSON.
    It inherits from the JSONEncoder class and uses the Abstract Base Class (ABCMeta).
    """

    @property
    def __dict__(self) -> dict:
        """
        Converts the instance's attributes into a dictionary.
        This dictionary can then be used for further operations like JSON serialization.
        """
        return asdict(self)

    @property
    def __json__(self) -> str:
        """
        Converts the instance's attributes into a JSON string.
        This method leverages the instance's __dict__ property to achieve this.
        """
        return dumps(self.__dict__)

    @property
    def serializable_dict(self) -> dict:
        """
        Provides a dictionary representation of the instance's attributes.
        This method can be utilized for making the object serializable to JSON.
        """
        return self.__dict__

    def default(self, o):
        """
        Provides a fallback method to return the dictionary representation of an object,
        which is then used to serialize the object to JSON. It's used in the superclass JSONEncoder.
        """
        return o.__dict__

    def __str__(self) -> str:
        """
        Returns a string representation of the object, in this case, a JSON string.
        This is the method that's invoked when str() is called on an instance of this class.
        """
        return self.__json__

    __slots__ = ()
    """
    This attribute is an optimization that provides space for instance attributes 
    in a space-efficient way without the overhead of a dictionary.
    In this case, it's set to an empty tuple since there are no additional attributes 
    beyond those provided by dataclass.
    """
