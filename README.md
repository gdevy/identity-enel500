# identity-enel500

## Portal

### CLI

Run the application using (use `--help` option to see available commands)

```shell
python src/portal/cli
```

## Setup (Passport)

TODO

## Setup (Portal)

### Python

#### Virtual Environment

To run the python application you need to set up a virtual environment to keep packages isolate. We will
use [venv](https://docs.python.org/3/library/venv.html) as it comes bundled with Python.

Create a virtual environment inside the project directory

```shell
cd <project dir>
python -m venv ./venv/
```

This will create a `venv` variable that you need to "activate" when you want to execute any python code related to the
project. To do that run:

```shell
source venv/bin/activate
```

to leave this environment run:

```shell
deactivate
```

#### Dependencies

> click (=8.0.3)

Used to create a CLI interface for the project. [docs](https://click.palletsprojects.com/en/8.0.x/)

TODO