#!/usr/bin/env python3

from kcl.sqlalchemy.model import FileRecord
from kcl.sqlalchemy.visualization import sa_display as kcl_sa_display

@click.command()
def sa_display():
    kcl_sa_display()

