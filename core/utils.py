from enum import Enum, IntEnum


class AnimalSize(Enum):
    LARGE = "large"
    MEDIUM = "medium"
    SMALL = "small"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class AnimalSex(Enum):
    MALE = "male"
    FEMALE = "female"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class AnimalType(Enum):
    DOG = "dog"
    CAT = "cat"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class AnimalStatus(IntEnum):
    AVALIABLE = 0
    RESERVED = 1
    ADOPTED = 3

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
