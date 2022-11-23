import json
from textwrap import indent
import click
import api
import os
from helpers import get_resource, error


@click.group()
def cli():
    pass


@cli.command(name="incomes", help="Incomes")
@click.option(
    "--start", default=0, help="Start index of pagination results", type=click.INT
)
@click.option(
    "--end", default=-1, help="End index of pagination results", type=click.INT
)
def incomes(start=0, end=-1):
    get_resource(
        name="Incomes", call=api.getIncomes, paginate=True, start=start, end=end
    )


@cli.command(name="outcomes", help="Outcomes")
@click.option(
    "--start", default=0, help="Start index of pagination results", type=click.INT
)
@click.option(
    "--end", default=-1, help="End index of pagination results", type=click.INT
)
def outcomes(start=0, end=-1):
    get_resource(
        name="Outcomes", call=api.getOutcomes, paginate=True, start=start, end=end
    )


@cli.command(name="transactions", help="Get Transactions")
@click.option(
    "--start", default=0, help="Start index of pagination results", type=click.INT
)
@click.option(
    "--end", default=-1, help="End index of pagination results", type=click.INT
)
def transactions(start=0, end=-1):
    get_resource(
        name="Transactions",
        call=api.getTransactions,
        paginate=True,
        start=start,
        end=end,
    )


@cli.command(name="nodes", help="Get all Nodes")
@click.option(
    "--start", default=0, help="Start index of pagination results", type=click.INT
)
@click.option(
    "--end", default=-1, help="End index of pagination results", type=click.INT
)
def nodes(start=0, end=-1):
    get_resource(name="Nodes", call=api.getNodes, paginate=True, start=start, end=end)


@cli.command(name="profile", help="Get Profile Info")
def profile():
    get_resource(
        name="Profile",
        call=api.getProfileInfo,
        paginate=False,
    )


@cli.command(name="balance", help="Get Balance")
def balance():
    get_resource(
        name="Balance",
        call=api.getBalance,
        paginate=False,
    )


@cli.command(name="transaction", help="Complete a transaction")
@click.option(
    "--id",
    prompt="Index of the receiving node",
    help="The id of the receiving node",
    type=click.STRING,
)
@click.option(
    "--amount",
    prompt="Amount NBC",
    help="The amount in NBCs of the transaction",
    type=click.INT,
)
def transaction(id, amount):
    if amount <= 0:
        error("Invalid amount")
    api.postTransaction(id, amount)
    click.echo("Transaction posted successfully")


@cli.command(name="connect", help="Select node you want to connect")
@click.option("--node", prompt="Node port")
def choose_port(node):
    home = os.getenv("HOME")
    with open(f"{home}/.port_connected_to", "w+") as f:
        f.write(node)
    click.echo(api.hello())


if __name__ == "__main__":
    cli()
