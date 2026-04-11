import os
import json
from pathlib import Path
import copy

APP_NAME = 'GRIM'
CONFIG_FILE = 'config.json'
OUTPUT_DIR = 'GRIM_EXPORTS'

EDITOR_MAP = {
    'default':None,
    'vscode':'code --wait',
    'sublime': 'subl',
    'vim': 'vim',
    'nano': 'nano'
    }

DEFAULT_CONFIG = {
    'auto_edit': True,
    'editor': 'default',
    'extension': 'md',}



def get_config_path():
    app_data = os.getenv('APPDATA')
    base_dir = Path(app_data) / APP_NAME if app_data else Path.home() / f'.{APP_NAME.lower()}'
    base_dir.mkdir(parents=True, exist_ok=True)
    return base_dir / CONFIG_FILE

def get_export_path():
    export_dir = Path.home() / OUTPUT_DIR
    if export_dir.exists() and export_dir.is_symlink():
        raise PermissionError("Alert: Export directory is tampered")
    export_dir.mkdir(parents=True, exist_ok=True)
    return export_dir
 
def save_config(cfg_dict):
    cfg_path = get_config_path()
    with open(cfg_path, 'w') as f:
        json.dump(cfg_dict, f, indent=4)


def load_config():
    path =  get_config_path()
    if not path.exists():
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG
    try:
        with open(path, 'r', encoding='utf-8') as f:
            cfg = json.load(f)
    except (json.JSONDecodeError, IOError):
        return DEFAULT_CONFIG

    if cfg['editor'] not in EDITOR_MAP:
        save_config(DEFAULT_CONFIG)
 
    cfg = {**DEFAULT_CONFIG, **cfg}
    return cfg


def resolve_editor(editor_key: str):
    if not editor_key or editor_key == 'default':
        return None
    return EDITOR_MAP.get(editor_key, None)
