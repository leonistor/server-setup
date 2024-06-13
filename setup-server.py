#!/usr/bin/env python

import click
import subprocess
import os


@click.command()
@click.option("--hosts", default="safta.lan", help="target hosts")
@click.option("--deploy", default="deploy_clear.test", help="deploy function")
def hello(hosts, deploy):
    """Invoke pyinfra"""
    # subprocess.run(["pyinfra", hosts, deploy], shell=True, check=True)
    os.system(f"pyinfra {hosts} {deploy}")


if __name__ == "__main__":
    hello()
