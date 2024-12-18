import json
import os

GROUPS_FILE = os.path.join(os.path.dirname(__file__), 'groups.json')

def load_groups():
    if os.path.exists(GROUPS_FILE):
        with open(GROUPS_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {}

def save_groups(groups):
    with open(GROUPS_FILE, 'w', encoding='utf-8') as file:
        json.dump(groups, file, ensure_ascii=False, indent=4)

def add_group(chat_id, chat_title):
    groups = load_groups()
    groups[str(chat_id)] = chat_title
    save_groups(groups)

def remove_group(chat_id):
    groups = load_groups()
    if str(chat_id) in groups:
        del groups[str(chat_id)]
        save_groups(groups)

def get_groups():
    return load_groups()

def is_group_active(chat_id):
    groups = load_groups()
    return str(chat_id) in groups
