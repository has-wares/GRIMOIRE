from . import db_funcs


GET_DISPATCH = {
    'id': db_funcs.get_byid,
    'name': db_funcs.get_byname,
    }

RM_DISPATCH = {
    'id': db_funcs.remove_byid,
    'name': db_funcs.remove_byname,
    }

UPDATE_DISPATCH = {
    'id': db_funcs.update_byid,
    'name': db_funcs.update_byname,
    }

RETAG_DISPATCH = {
    'id': db_funcs.retag_byid,
    'name': db_funcs.retag_byname,
    }

RENAME_DISPATCH = {
    'id': db_funcs.rename_byid,
    'name': db_funcs.rename_byname,
    }

LS_DISPATCH = {
    'tags_new': lambda conn, tags: db_funcs.list_bytag_n(conn, tags),
    'tags_all': lambda conn, tags: db_funcs.list_bytag(conn, tags),
    'newest': lambda conn, tags: db_funcs.listemnew(conn),
    'all': lambda conn, tags: db_funcs.listemall(conn),
    'tags_exact': lambda conn, tags : db_funcs.list_exact(conn, tags),
    'tags_exact_new': lambda conn, tags : db_funcs.list_exact_new(conn, tags),
    }
