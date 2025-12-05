import sys
from pathlib import Path

# Ensure project root is on sys.path so imports work whether run as module or script
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.loader.dataset_loader import DatasetLoader
from src.controller.swipe_manager import SwipeManager
from src.view.tk_view import TkView


def main():
    dataset_path = ROOT_DIR / "data" / "dataset.json"
    loader = DatasetLoader(str(dataset_path))
    countries = loader.load()

    controller = SwipeManager(countries)

    view = TkView(controller)

    view.run()


if __name__ == "__main__":
    main()
