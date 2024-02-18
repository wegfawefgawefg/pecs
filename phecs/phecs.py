from enum import Enum
import os


################    SETTING THE STAGE   ################
class AssetPath:
    def __init__(self, base_path):
        self.base_path = base_path

    def full_path(self, filename):
        return os.path.join(
            self.base_path, filename
        )  # Using os.path.join for compatibility


def loader(load_func, path: str | None = None):
    def decorator(cls):
        if not issubclass(cls, Enum):
            yellow = "\033[93m"  # ANSI escape sequence for yellow
            blue = "\033[94m"  # ANSI escape sequence for blue
            green = "\033[92m"  # ANSI escape sequence for green
            red = "\033[91m"  # ANSI escape sequence for red
            endc = "\033[0m"  # ANSI escape sequence to end coloring

            error_path = f", path='{path}'" if path else ""
            error_msg = (
                f"{red}Your asset class '{cls.__name__}' should derive from Enum.{endc}\n\n"
                f"{green}Correct usage:{endc}\n\n"
                f"\t@loader({load_func.__name__}{error_path})\n"
                f"\t{blue}class{endc} {cls.__name__}({yellow}Enum{endc}): {yellow}<- Make sure to derive from Enum{endc}\n"
                "\t\t# ... your assets here ..."
            )
            raise TypeError(error_msg.strip())

        cls.load = staticmethod(load_func)
        cls.get_base_path = classmethod(lambda c: AssetPath(path or ""))
        cls.paths = classmethod(
            lambda c: {
                member: cls.get_base_path().full_path(member.value) for member in cls
            }
        )
        return cls

    return decorator


################    THE CACHE    ################
class AssetCache:
    def __init__(self):
        self.cache = {}

    def get(self, asset_enum):
        if asset_enum in self.cache:
            return self.cache[asset_enum]

        # fetch loader
        asset_type = type(asset_enum)
        loader = asset_type.load
        if loader is None:
            raise TypeError(f"No load function defined for asset {asset_enum}")

        # construct full path and load asset
        base_path = asset_type.get_base_path()
        full_path = base_path.full_path(asset_enum.value)
        if not os.path.exists(full_path):
            raise ValueError(f"File not found: {full_path}")
        self.cache[asset_enum] = loader(full_path)
        return self.cache[asset_enum]

    def remove(self, asset_enum):
        if asset_enum in self.cache:
            del self.cache[asset_enum]

    def preload(self, assets):
        for asset in assets:
            self.get(asset)

    def clear_cache(self):
        self.cache.clear()
