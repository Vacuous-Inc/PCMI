'''
Code for creating and managing the database. 

Modified from http://flask.pocoo.org/docs/1.0/tutorial/database/
'''

import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
from sqlite3 import OperationalError as db_error


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            "sqlite_db", detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))

def get_user(user_id):
    db = get_db()
    user = db.execute(
        "SELECT name, email, profile_pic, balance, admin FROM user WHERE id = ?", (user_id,)
    ).fetchone()
    return user

def new_user(id_, name, email, profile_pic):
    db = get_db()
    db.execute(
        "INSERT INTO user (id, name, email, profile_pic, balance, admin) "
        "VALUES (?, ?, ?, ?, ?, ?)", (id_, name, email, profile_pic, 1000, 0)
    )
    db.commit()

def is_admin(user_id):
    db = get_db()
    return bool(db.execute("SELECT admin FROM user WHERE id = ?", (user_id,)).fetchone()[0])

@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)