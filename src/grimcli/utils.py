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
    table.add_column('CREATED_AT', style='white')
    table.add_column('UPDATED_AT', style='white')
    #row[0]=id, row[1]=name, row[2]=tags, row[3]=timestamp
    for row in notes:
        num = str(row[0])
        name = row[1]
        tags = row[2] if row[2] else ''
        created_at = row[3] if row[3] else 'N/A'
        created_at = created_at.split(' ')[0] if created_at != 'N/A' else 'N/A'
        updated_at = row[4] if row[4] else 'N/A'
        updated_at = updated_at.split(' ')[0] if updated_at != 'N/A' else 'N/A'
        table.add_row(num, name, tags, created_at, updated_at)

    console.print(table)


def search_table(notes, console):
    table = Table()
    table.add_column('ID', style='white')
    table.add_column('NAME', style='white', no_wrap=False)
    table.add_column('TAGS', style ='white', no_wrap=False)
    table.add_column('CREATED_AT', style='white')
    table.add_column('UPDATED_AT', style='white')
    table.add_column('SNIPET', style='white')
    for row in notes:
        num = str(row[0])
        name = row[1]
        tags = row[2] if row[2] else ''
        created_at = row[3] if row[3] else 'N/A'
        created_at = created_at.split(' ')[0] if created_at != 'N/A' else 'N/A'
        updated_at = row[4] if row[4] else 'N/A'
        updated_at = updated_at.split(' ')[0] if updated_at != 'N/A' else 'N/A'
        snipet = row[5] if row[5] else ''
        table.add_row(num, name, tags, created_at, updated_at, snipet)

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

