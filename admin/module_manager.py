import importlib
import os
import json

MODULES_FILE = os.path.join(os.path.dirname(__file__), 'modules.json')

# Schlüssel für die Beschriftung des Buttons in den Sprachdateien
module_name_key = "module_manager"

def load_modules():
    if os.path.exists(MODULES_FILE):
        with open(MODULES_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {}

def save_modules(modules):
    with open(MODULES_FILE, 'w', encoding='utf-8') as file:
        json.dump(modules, file, ensure_ascii=False, indent=4)

def is_module_enabled(module_name):
    modules = load_modules()
    return modules.get(module_name, {}).get('enabled', False)

def set_module_enabled(module_name, enabled):
    modules = load_modules()
    if module_name not in modules:
        modules[module_name] = {}
    modules[module_name]['enabled'] = enabled
    save_modules(modules)

def get_module_names():
    modules_dir = os.path.join(os.path.dirname(__file__), '..', 'modules')
    return [name for name in os.listdir(modules_dir) if os.path.isdir(os.path.join(modules_dir, name)) and not name.startswith('__')]

def get_module_display_name(module_name, user_lang):
    module = importlib.import_module(f'modules.{module_name}')
    if hasattr(module, 'module_name_key'):
        name_key = getattr(module, 'module_name_key')
        return translate(name_key, user_lang)
    return module_name

def get_module_function(module_name, function_name):
    if not is_module_enabled(module_name):
        return None
    module = importlib.import_module(f'modules.{module_name}')
    return getattr(module, function_name, None)
