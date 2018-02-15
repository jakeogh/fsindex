#!/usr/bin/env python3

from kcl.sqlalchemy.model.FileRecord import FileRecord
from kcl.sqlalchemy.model.Filename import Filename
from kcl.sqlalchemy.model.Path import Path

from sqlalchemy_utils.functions import create_database
from fsindex.model.Config import CONFIG
CONFIG.database = CONFIG.database_timestamp
create_database(CONFIG.database)

from kcl.sqlalchemy.test_enviroment_base import *
