# -*- coding: utf-8 -*-

"""Console script for glacier."""
import sys
import click
from glacier.glacier import Glacier


@click.group()
def main():
    pass


@main.command()
@click.option(
    "--vault-name",
    type=str,
    help="AWS Glacier Vault name",
    default=None,
)
def initialize_vaults(vault_name):
    glacier = Glacier(vault_name=vault_name)
    glacier.init_vault_folder()


@main.command()
@click.option(
    "--vault-name",
    type=str,
    help="AWS Glacier Vault name",
    default=None,
    required=True,
)
@click.option(
    "--output-format",
    type=str,
    help="Output format for archive",
    default="zip",
    required=True,
)
def download_archive(vault_name, output_format):
    glacier = Glacier(vault_name=vault_name, output_format=output_format)
    glacier.init_archive_job()
    glacier.retrieve_archive()


@main.command()
@click.option(
    "--vault-name",
    type=str,
    help="AWS Glacier Vault name",
    default=None,
    required=True,
)
def initialize_inventory(vault_name):
    glacier = Glacier(vault_name=vault_name)
    glacier.init_inventory_job()


@main.command()
@click.option(
    "--vault-name",
    type=str,
    help="AWS Glacier Vault name",
    default=None,
    required=True,
)
def retrieve_inventory(vault_name):
    glacier = Glacier(vault_name=vault_name)
    glacier.retrieve_inventory()


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
