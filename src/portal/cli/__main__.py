from pathlib import Path

import click
import cv2.cv2

from src.portal.biometrics.camera import create_probe
from src.portal.biometrics.template import pipeline


@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    pass


@click.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name',
              help='The person to greet.')
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo(f"Hello {name}!")


@click.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name',
              help='The person to greet.')
def hello2(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo(f"Hello {name}!")


@click.command()
@click.option('--output', help='path to output file')
def take_image(output):
    """Test image acquisition, writes to output file"""
    create_probe(Path(output))


@click.command()
@click.option('--input_image', help='path to output file')
def create_template(input_image):
    """Test image acquisition, writes to output file"""
    print(pipeline(Path(input_image)))


if __name__ == '__main__':
    cli.add_command(hello2)
    cli.add_command(hello)
    cli.add_command(take_image)
    cli.add_command(create_template)
    cli()
