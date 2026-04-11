from . import utils
from . import messages as msg

def make(name, tags):
    if not utils.validate_name(name):
        raise ValueError(f'{msg.INVALID_NAME}{msg.NAME_RULES}')

    if not utils.validate_tags(tags):
        raise ValueError(f'{msg.INVALID_TAGS}{msg.TAG_RULES}')

    name = utils.clean_input(name)
    tags = utils.normalize_tags(tags) if tags else ''

    return (name, tags)


def retag(tags):
    if not utils.validate_tags(tags):
        raise ValueError(f'{msg.INVALID_TAGS}{msg.TAG_RULES}')
    tags = utils.normalize_tags(tags) if tags else ''
    return tags


def rename(name):
    if not utils.validate_name(name):
        raise ValueError(f'{msg.INVALID_NAME}{msg.NAME_RULES}')
    name = utils.clean_input(name)
    return name

def content_okay(text):
    if text is None or text.strip(' ') == '':
        raise ValueError(f'{msg.EMPTY}\n{msg.ABORT}')
    return True

def content_found(content):
    if content is None:
        raise ValueError(f'{msg.NOT_FOUND}')
    return True

def content_diff(old, new):
    if new is None:
        raise ValueError(f'{msg.NO_CHANGE}\n{msg.ABORT}')
    old = old.strip()
    new = new.strip()
    if old == new:
        raise ValueError(f'{msg.NO_CHANGE}\n{msg.ABORT}')
    return True

def list_exist(notes):
    if not notes:
        raise ValueError(f'{msg.NOT_FOUND}')
    return True

def name_exist(already):
    if already is not None:
        raise ValueError(f'{msg.NAME_ALREADY}')
    return True

def whatami(what):
    if what.isdigit():
        return (int(what), 'id')
    else:
        return (what, 'name')

def can_delete(confirmed):
    if confirmed: return True
    raise ValueError(f'{msg.ABORT}')


def get_lsmode(has_tags, is_new, is_only):
    dispatch = {
        (True, True, False): 'tags_new',
        (True, False, False): 'tags_all',
        (False, True, False): 'newest',
        (False, False, False): 'all',
        (True, True, True): 'tags_exact_new',
        (True, False, True): 'tags_exact',
        }
    return dispatch.get((has_tags, is_new, is_only), 'all')

def find_okay(results):
    if results is None:
        raise RuntimeError(f'{msg.WENT_WRONG}')
    if not results:
        raise ValueError(f'{msg.NOT_FOUND}')
    return True
