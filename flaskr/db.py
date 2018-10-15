import click
from flask import current_app, g
from flask.cli import with_appcontext
from pymongo import MongoClient


def get_mongo_client():
    if 'client' not in g:
        g.client = MongoClient(current_app.config['MONGODB'])
    return g.client


def close_mongo_client(e=None):
    client = g.pop('client', None)
    if client is not None:
        client.close()


def init_client():
    client = get_mongo_client()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_client()
    click.echo('Initialized MongoClient.')


def init_app(app):
    app.teardown_appcontext(close_mongo_client)
    app.cli.add_command(init_db_command)
