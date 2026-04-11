import re
import os
from pathlib import Path
from rich.table import Table
import shutil


def get_path(name='GRIM'):
    app_data = os.getenv('APPDATA')
    if app_data:
        base_dir = Path(app_data) / name
    else: base_dir = Path.home() / f'{name.lower()}'
    base_dir.mkdir(parents=True, exist_ok=True)
    return base_dir / 'grim.db'


def display_table(notes, console):
    table = Table()
    table.add_column('ID', style='white')
    table.add_column('NAME', style='white', no_wrap=False)
    table.add_column('TAGS', style ='white', no_wrap=False)
    table.add_column('TIMESTAMP', style='white')
    #row[0]=id, row[1]=name, row[2]=tags, row[3]=timestamp
    for row in notes:
        num = str(row[0])
        name = row[1]
        tags = row[2] if row[2] else ''
        date = row[3] if row[3] else 'N/A'
        date_str = date.split(' ')[0]
        table.add_row(num, name, tags, date_str)

    console.print(table)

def validate_name(name):
    if not name or not name.strip():
        return False
    if name.isdigit():
        return False
    if len(name) > 50:
        return False
    #Allow letters, numbers, spaces, underscores and hyphens
    return bool(re.match(r'^[\w\s-]+$', name))

def clean_input(text):
    if not text:
        return ''
    text = re.sub(r'\s+', ' ', text)
    return text.strip().strip('-_')

def validate_tags(tags):
    if not tags:
        return True
    if len(tags) > 100:
        return False
    #Allow letters, numbers, spaces and commas
    return bool(re.match(r'^[\w\s,.-]+$', tags))


def taglist(tags):
    if not tags:
        return []
    return [t.strip().lower() for t in tags.split(',') if t.strip()]

def normalize_tags(tagstr):
    if not tagstr:
        return

    taglist = [t.strip().lower() for t in tagstr.split(',') if t.strip()]
    return ','.join(sorted((taglist)))


def write_md(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

        
def raise_unexpected(click, e):
    return click.secho(f'{UNEXPECTED}: {e}')

