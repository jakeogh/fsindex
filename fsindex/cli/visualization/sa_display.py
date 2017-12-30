#!/usr/bin/env python3

import click
from kcl.sqlalchemy.model.FileRecord import FileRecord
from kcl.sqlalchemy.model.Filename import Filename
from kcl.sqlalchemy.model.Path import Path
from kcl.sqlalchemy.model.BytesHash import BytesHash

from kcl.sqlalchemy.visualization.sa_display import sa_display as kcl_sa_display

@click.command()
def sa_display():
    #import IPython; IPython.embed()
    kcl_sa_display(globals())
