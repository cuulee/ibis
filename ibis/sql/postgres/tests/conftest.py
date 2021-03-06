# Copyright 2015 Cloudera Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import getpass
import os

import pytest

import ibis

PG_USER = os.environ.get(
    'IBIS_POSTGRES_USER',
    os.environ.get('PGUSER', getpass.getuser())
)
PG_PASS = os.environ.get('IBIS_POSTGRES_PASS', os.environ.get('PGPASSWORD'))
PG_HOST = os.environ.get('PGHOST', 'localhost')
IBIS_TEST_POSTGRES_DB = os.environ.get(
    'IBIS_TEST_POSTGRES_DB',
    os.environ.get('PGDATABASE', 'ibis_testing')
)


@pytest.fixture(scope='module')
def con():
    return ibis.postgres.connect(
        host=PG_HOST,
        user=PG_USER,
        password=PG_PASS,
        database=IBIS_TEST_POSTGRES_DB,
    )


@pytest.fixture(scope='module')
def db(con):
    return con.database()


@pytest.fixture(scope='module')
def alltypes(db):
    return db.functional_alltypes


@pytest.fixture(scope='module')
def df(alltypes):
    return alltypes.execute()


@pytest.fixture(scope='module')
def at(alltypes):
    return alltypes.op().sqla_table


@pytest.fixture
def translate():
    from ibis.sql.postgres.compiler import PostgreSQLExprTranslator
    return lambda expr: PostgreSQLExprTranslator(expr).get_result()
