import importlib
import pkgutil
import logging

# Logger konfigurieren
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

# Statische Liste der Module und ihrer Menü-Funktionen
MODULES = {}

def load_modules():
    package = 'admin'
    for _, module_name, _ in pkgutil.iter_modules([package]):
        try:
            module = importlib.import_module(f'{package}.{module_name}')
            if hasattr(module, 'module_name_key'):
                menu_function_name = f'{module_name}_menu'
                if hasattr(module, menu_function_name):
                    MODULES[module_name] = getattr(module, menu_function_name)
                    logger.debug(f"Module {module_name} mit Funktion {menu_function_name} geladen.")
                else:
                    logger.debug(f"Menu function {menu_function_name} nicht in module {module_name} gefunden.")
            else:
                logger.debug(f"module_name_key nicht in module {module_name} gefunden.")
        except ModuleNotFoundError as e:
            logger.error(f"Module {module_name} konnte nicht geladen werden: {e}")

# Module beim Start laden
load_modules()
