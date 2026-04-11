
INVALID_NAME = 'INVALID_NAME'
INVALID_TAGS = 'INVALID_TAGS'
UNEXPECTED = 'UNEXPECTED_ERROR'
NOT_FOUND = 'NOT FOUND'
EMPTY = 'EMPTY CONTENT'
ABORT = 'OPERATION ABORTED'
NO_CHANGE = 'NO CHANGES'
NAME_ALREADY = 'NAME ALREADY USED'
WENT_WRONG = 'SOMETHING WENT WRONG'
SAVED = 'SAVED SUCCESFULLY'
UPDATED = 'UPDATED SUCCESFULLY'
DELETED = 'DELETED SUCCESFULLY'
RETAGED = 'RETAGED SUCCESFULLY'
RENAMED = 'RENAMED SUCCESFULLY'
EXPORTED = 'EXPORTED SUCCESFULLY'


NAME_RULES = """
only letters, numbers, underscores, spaces, and hyphens!
a name cannot contain only numbers!
Max 20 characters!
"""

TAG_RULES = """
Tags can contain letters, numbers, spaces, commas, dots, and hyphens!
Max 100 characters total!
"""


MAKE_HELP = """
Create a new note. Opens the system editor.
"""

EDIT_HELP = """
Edit an existing note's content by Name or ID.
"""

LS_HELP = """
List all notes. Supports filtering by tags and sorting.
"""

SHOW_HELP = """
Display a note's content rendered as Markdown.
"""

RM_HELP = """
Remove a note from the database permanently.
"""

RETAG_HELP = """
Update the tags of a note without changing its content.
"""

RENAME_HELP = """
Change the title of an existing note.
"""

CFG_HELP = """
Display current configuration.
"""

FIND_HELP = """
Search for keyword(s) in notes using Full-Text Search (FTS5).
""" 

EXPORT_HELP = """
Export a note as a standalone .md file to the export path.
"""

def raise_unexpected(click, e):
    return click.secho(f'{UNEXPECTED}: {e}')

def make_success(click, name):
    return click.secho(f'NOTE {name} {SAVED}')

def delete_success(click, what):
    return click.secho(f'NOTE {what} {DELETED}')

def update_success(click, what):
    return click.secho(f'NOTE {what} {UPDATED}')

def retag_success(click, what):
    return click.secho(f'NOTE {what} {RETAGED}')

def rename_success(click, what):
    return click.secho(f'NOTE {what} {RENAMED}')

def export_success(click, num, directory, name):
    return click.secho(f'NOTE {EXPORTED} in {directory} as {name}.md')
