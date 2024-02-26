# -*- coding: utf-8 -*-
# Copyright 2014 Objectif Libre
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#
from oslo_config import cfg
import threading
from oslo_db.sqlalchemy import session
from oslo_db.sqlalchemy import enginefacade

_FACADE = None
_FACADE_NEW = None


def _create_facade_lazily():
    global _FACADE
    if _FACADE is None:
        ctx = enginefacade.transaction_context()
        ctx.configure(sqlite_fk=True)
        _FACADE = ctx
    return _FACADE

_CONTEXT = threading.local()

def get_engine():
    facade = _create_facade_lazily()
    return facade.get_legacy_facade().get_engine()

def get_session(**kwargs):
    facade = _create_facade_lazily()
    return facade.get_legacy_facade().get_session(**kwargs)

def session_for_read():
    return _create_facade_lazily().reader.using(_CONTEXT)

def session_for_write():
    return _create_facade_lazily().writer.using(_CONTEXT)
