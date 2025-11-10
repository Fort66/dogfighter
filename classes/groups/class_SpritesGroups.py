from pygame.sprite import Group, GroupSingle


class SpriteGroups:
    __instance = None

    __groups_dict = {
        "player_group": GroupSingle(),
        "enemies_group": Group(),
        "player_rockets_group": Group(),
        "enemies_rockets_group": Group(),
        "explosion_group": Group(),
        "rockets_group": Group(),
    }

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self):
        self.__dict__ = self.__groups_dict

    def sprites(self):
        return list(self.__dict__)

    def clear(self):
        for group in self.__dict__.values():
            group.empty()



groups = SpriteGroups()