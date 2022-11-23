import json
import click


def error(msg):
    click.secho(msg, fg="red")


def get_resource(name, call, paginate=False, start=0, end=0):
    if start and start > end:
        error("Start index cannot be larger than the end index")
        return
    click.secho(f"{name}:", fg="green")
    data = call()
    if paginate:
        if end <=0:
            data = data[start: ]
        else:
            data = data[start:end+1]
    click.echo(json.dumps(data, indent=2))
