import click

import aramaki
import aramaki.system


@click.group()
@click.option("--database", default="sqlite:///aramaki.sqlite")
@click.option("--application-url", default="http://localhost:6543")
@click.pass_context
def main(ctx, database, application_url):
    ctx.obj = aramaki.app.configure(
        db_uri=database, application_url=application_url
    )


@main.group()
def system():
    pass


@system.command("add")
@click.argument("name")
@click.pass_context
def add_system(ctx, name):
    click.echo(f"Adding system {name}")
    with ctx.obj:
        aramaki.system.System.create(name)


@system.command("list")
@click.pass_context
def list_systems(ctx):
    with ctx.obj:
        for system in aramaki.system.System.list():
            click.echo(f"{system}")
