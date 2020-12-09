import click
from flask.cli import FlaskGroup
from api.utils.models import ROLE_ADMIN

from api.app import create_app


def create_api(info):
    return create_app(cli=True)


@click.group(cls=FlaskGroup, create_app=create_api)
def cli():
    """Main entry point"""


@cli.command("init")
def init():
    """Create a new admin user"""
    from api.extensions import db
    from api.models import User
    from api.utils.models import save_to_db

    click.echo("create user")
    admin_user = User(
        username="admin",
        email="admin@lori.com",
        password="admin",
        role=ROLE_ADMIN,
        active=True)
    save_to_db(db, admin_user)
    click.echo("created user admin")


if __name__ == "__main__":
    cli()
