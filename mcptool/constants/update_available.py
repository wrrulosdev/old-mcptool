# Check if an update is available
from ..update.updater import Updater

UPDATE_AVAILABLE: bool = Updater.update_available()
