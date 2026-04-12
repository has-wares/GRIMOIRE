import click
from . import db_funcs
from . import utils
from . import config
from rich.console import Console
from rich.markdown import Markdown
import sqlite3
from pathlib import Path
from . import core
from . import messages as msg
from .dispatch import (GET_DISPATCH, RM_DISPATCH, UPDATE_DISPATCH,
                      RETAG_DISPATCH, RENAME_DISPATCH, LS_DISPATCH)


@click.command(name='make', help=msg.MAKE_HELP)
@click.argument('name')
@click.option('--tags', '-t', default='')
@click.pass_context
def make_note(ctx, name, tags):
    conn = ctx.obj['conn']    
    cfg = ctx.obj['config']
    
    try:
        name, tags = core.make(name, tags)
        name_already = db_funcs.get_byname(conn, name)
        core.name_exist(name_already)
        editor = config.resolve_editor(cfg.get('editor'))
        content = click.edit(text='', extension=cfg.get('extension', '.md'), editor=editor)
        core.content_okay(content)
        db_funcs.make_note(conn, name, content, tags)
        msg.make_success(click, name)
    except ValueError as e:
        click.secho(f'{e}')
    except Exception as e:
        msg.raise_unexpected(click, e)
        
        
@click.command(name='edit', help=msg.EDIT_HELP)
@click.argument('what')
@click.pass_context
def edit_note(ctx, what):
    conn = ctx.obj['conn']
    cfg = ctx.obj['config']
    ext = cfg.get('extension', '.md')
    
    try:
        what, mode = core.whatami(what)
        curr_cont = GET_DISPATCH[mode](conn, what)
        core.content_found(curr_cont)
        editor = config.resolve_editor(cfg.get('editor'))
        new_cont = click.edit(text=curr_cont, extension=ext, editor=editor)
        core.content_diff(curr_cont, new_cont)
        UPDATE_DISPATCH[mode](conn, what, new_cont)
        msg.update_success(click, what)
    except ValueError as e:
        click.secho(f'{e}')
    except Exception as e:
        msg.raise_unexpected(click, e)

        

@click.command(name='ls', help=msg.LS_HELP)
@click.option('--tags', '-t', default=None)
@click.option('--new', '-n', is_flag=True)
@click.option('--only', '-o', is_flag=True)
@click.pass_context
def list_notes(ctx, new, tags, only):
    conn = ctx.obj['conn']
    console = Console()

    try:
        tags = utils.taglist(tags)
        mode =  core.get_lsmode(bool(tags), new, only)
        notes = LS_DISPATCH[mode](conn, tags)
        core.list_exist(notes)
        utils.display_table(notes, console)
    except ValueError as e:
        click.secho(f'{e}')
    except Exception as e:
        msg.raise_unexpected(click, e)


@click.command(name='show', help=msg.SHOW_HELP)
@click.argument('what')
@click.pass_context
def show_note(ctx, what):
    conn = ctx.obj['conn']
    console = Console()
    
    try:
        what, mode =  core.whatami(what)
        content = GET_DISPATCH[mode](conn, what)
        core.content_found(content)
        core.content_okay(content)
        md = Markdown(content)
        console.print(md)
    except ValueError as e:
        click.secho(f'{e}')
    except Exception as e:
        msg.raise_unexpected(click, e)


@click.command(name='rm', help=msg.RM_HELP)
@click.argument('what')
@click.option('--yes', '-y', is_flag=True, default=False)
@click.pass_context
def delete_note(ctx, what, yes):
    conn = ctx.obj['conn']

    try:
        what, mode = core.whatami(what)
        content = GET_DISPATCH[mode](conn, what)
        core.content_found(content)
        confirm = yes or click.confirm(f'delete {what}?')
        core.can_delete(confirm)
        RM_DISPATCH[mode](conn, what)
        msg.delete_success(click, what)
    except ValueError as e:
        click.secho(f'{e}')
    except Exception as e:
        msg.raise_unexpected(click, e)

                
@click.command(name='retag', help=msg.RETAG_HELP)
@click.argument('what')
@click.argument('tags', default='')
@click.pass_context
def retag_note(ctx, what, tags):
    conn = ctx.obj['conn']

    try:
        tags = core.retag(tags)
        what, mode = core.whatami(what)
        RETAG_DISPATCH[mode](conn, what, tags)
        msg.retag_success(click, what)
    except ValueError as e:
        click.secho(f'{e}')
    except Exception as e:
        msg.raise_unexpected(click, e)


@click.command(name='rename', help=msg.RENAME_HELP)
@click.argument('what')
@click.argument('name')
@click.pass_context
def rename_note(ctx, what, name):
    conn = ctx.obj['conn']
    try:
        name = core.rename(name)
        name_already = db_funcs.get_byname(conn, name)
        core.name_exist(name_already)
        what, mode = core.whatami(what)
        RENAME_DISPATCH[mode](conn, what, name)
        msg.rename_success(click, what)
    except ValueError as e:
        click.secho(f'{e}')
    except Exception as e:
        msg.raise_unexpected(click, e)
    


@click.command(name='cfg', help=msg.CFG_HELP)
@click.pass_context
def show_cfg(ctx):
    cfg = ctx.obj['config']
    for k, v in cfg.items():
        click.secho(f'key: {str(k).rjust(10)} | value: {str(v).ljust(15)}')

    
@click.command(name='find', help=msg.FIND_HELP)
@click.argument('query', nargs=-1)
@click.pass_context
def find(ctx, query):
    conn = ctx.obj['conn']
    console = Console()
    query = " ".join(query)
    try:
        results = db_funcs.search(conn, query)
        core.find_okay(results)
        utils.search_table(results, console)
    except ValueError as e:
        click.secho(f'{e}')
    except Exception as e:
        msg.raise_unexpected(click, e)

    

@click.command(name='export', help=msg.EXPORT_HELP)
@click.argument('nid', type=int)
@click.pass_context
def export(ctx, nid):
    conn = ctx.obj['conn']
    export_dir = config.get_export_path()
    
    try:
        content = db_funcs.get_byid(conn, nid)
        core.content_found(content)
        core.content_okay(content)
        name = db_funcs.get_namebyid(conn, nid)
        path = export_dir / f"{name}.md"
        utils.write_md(path, content)
        msg.export_success(click, nid, export_dir, name)
    except ValueError as e:
        click.secho(f'{e}')
    except Exception as e:
        msg.raise_unexpected(click, e)
 

@click.command(name="seted")
@click.argument("editor")
@click.pass_context
def set_editor(ctx, editor):
    cfg = ctx.obj["config"]

    try:
        if editor not in config.EDITOR_MAP:
            click.secho("Unsupported editor")
            return

        cfg["editor"] = editor
        config.save_config(cfg)
        click.secho(f"Editor set to {editor}")
    except Exception as e:
        print(msg.WENT_WRONG)

    
