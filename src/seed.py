""" src.seed """
import logging
from importlib import import_module
from inspect import getmembers
from inspect import isclass

import click
from flask.cli import AppGroup
from flask.cli import with_appcontext


logger = logging.getLogger(__name__)


@click.command()
@click.argument("name", nargs=1)
@click.argument("action", nargs=1)
@with_appcontext
def seed(name, action):
    """SeedCommand"""
    if not name:
        raise TypeError("Not found argument name")

    if not action:
        raise TypeError("Not found argument action")

    if action not in ["up", "down"]:
        raise TypeError("The action must be up or down")

    seeds = {}
    modules = import_module("src.seeds")
    for _, obj in getmembers(modules):
        if isclass(obj):
            seeds[obj.__seed__] = obj

    if name == "all":
        return __run_all(seeds, action)

    if not __exists_seed(seeds, name):
        raise TypeError("%s not found in registered seeds list" % name)

    return __run_seed(seeds[name], action)


def __exists_seed(seeds, name):
    return True if name in seeds else None


def __run_seed(seed, action):
    if action == "down":
        return seed.down()
    __instance = seed()
    __instance.up()


def __run_all(seeds, action):
    for key, seed in seeds:
        __run_seed(seed, action)
