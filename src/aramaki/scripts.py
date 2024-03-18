import argparse
import asyncio
import sys

import pyramid.scripts.pserve
from pyramid.paster import bootstrap

import aramaki.federation
import aramaki.processing


def run_web(args):
    # Pass over all settings processing to the original pserve command
    args = ["aramaki web"] + args
    pyramid.scripts.pserve.main(args)


def run_processing(config_uri):
    with bootstrap(config_uri) as env:
        aramaki.processing.process_forever(env)


def run_federation(config_uri):
    with bootstrap(config_uri) as env:
        asyncio.run(aramaki.federation.server(env))


def main(argv=sys.argv):
    parser = argparse.ArgumentParser(
        prog="aramaki",
        description="Aramaki, the federated DevOps control plane.",
    )

    subparsers = parser.add_subparsers()

    web = subparsers.add_parser("web", help="Start the web server")
    web.add_argument("args", nargs=argparse.REMAINDER)
    web.set_defaults(func=run_web)

    processing = subparsers.add_parser(
        "processing", help="Start a queue processing worker."
    )
    processing.add_argument(
        "config_uri", help="The URI to the configuration file."
    )
    processing.set_defaults(func=run_processing)

    federation = subparsers.add_parser(
        "federation", help="Start the federation websocket server."
    )
    federation.add_argument(
        "config_uri", help="The URI to the configuration file."
    )
    federation.set_defaults(func=run_federation)

    args = parser.parse_args(argv[1:])

    func_args = dict(args._get_kwargs())
    del func_args["func"]

    args.func(**func_args)

    # federation = "aramaki.agent.federation:main"
    # processing = "aramaki.agent.worker:main"
    # web = "aramaki.agent.worker:main"
