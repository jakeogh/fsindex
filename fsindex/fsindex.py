#!/usr/bin/env python3

import click
import shutil
from kcl.printops import eprint
from kcl.printops import set_verbose
from .update import update_db

CONTEXT_SETTINGS = \
    dict(help_option_names=['--help'],
         terminal_width=shutil.get_terminal_size((80, 20)).columns)

@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('--verbose', is_flag=True, callback=set_verbose, expose_value=False)
def fsindex(ctx):
    eprint("ctx:", ctx)

@dnsgate.command()
@click.argument('root', required=True, nargs=1)
def update(root):
    update_db(root)

@dnsgate.command()
def stats():
    db_stats()

if __name__ == '__main__':
    # pylint: disable=no-value-for-parameter
    fsindex()
    # pylint: enable=no-value-for-parameter
    eprint("Exiting without error.", level=LOG['DEBUG'])
