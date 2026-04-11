"""
PROJECT CEL : PERSONAL KNOWLEDGE COLLECTOR
    """
import click
import sqlite3
from . import db_funcs, utils, config, commands

@click.group()
@click.pass_context
def cli(ctx):
    db_path = utils.get_path()
    conn = sqlite3.connect(db_path)
    db_funcs.init_db(conn)
    cfg = config.load_config()
    export_path = config.get_export_path()
    ctx.obj = {'conn':conn, 'path':db_path, 'config':cfg, 'export':export_path}
    ctx.call_on_close(lambda: conn.close())
        

cli.add_command(commands.make_note)
cli.add_command(commands.edit_note)
cli.add_command(commands.list_notes)
cli.add_command(commands.show_note)
cli.add_command(commands.delete_note)
cli.add_command(commands.retag_note)
cli.add_command(commands.rename_note)
cli.add_command(commands.find)
cli.add_command(commands.export)
cli.add_command(commands.show_cfg)
cli.add_command(commands.set_editor)



