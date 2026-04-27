import os
from pathlib import Path
from dotenv import load_dotenv

from rich import print as rprint


load_dotenv()

PROJECT_ROOT_DIR = Path(__file__).parent.parent.parent


DEFAULT_MODEL_NAME = os.environ.get("MODEL_NAME")

if __name__ == "__main__":
    from pretty import ALogger

    a_logger = ALogger("[info]")

    a_logger.title("listing")
    rprint(f"{DEFAULT_MODEL_NAME=}")
    rprint(f"{PROJECT_ROOT_DIR=}")
