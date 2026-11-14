from src.api import APIAdapter
from src.json_storage import JSONStorage
from src.user_interface import menu


def main() -> None:
    """Собирает компоненты и запускает программу."""
    adapter = APIAdapter()
    storage = JSONStorage("data/aeroplanes.json")
    storage.connect()
    try:
        menu(adapter, storage)
    finally:
        storage.close()


if __name__ == "__main__":
    main()
