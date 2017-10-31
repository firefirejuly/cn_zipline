import click
from zipline.data.bundles import register
from zipline.data import bundles as bundles_module
from cn_zipline.bundles.tdx_bundle import tdx_bundle
import pandas as pd
import os
from cn_stock_holidays.zipline.default_calendar import register_calendar


@click.group()
def main():
    pass


@main.command()
@click.option(
    '-b',
    '--bundle',
    default='quantopian-quandl',
    metavar='BUNDLE-NAME',
    show_default=True,
    help='The data bundle to ingest.',
)
@click.option(
    '--assets-version',
    type=int,
    multiple=True,
    help='Version of the assets db to which to downgrade.',
)
@click.option(
    '--show-progress/--no-show-progress',
    default=True,
    help='Print progress information to the terminal.'
)
def ingest(bundle, assets_version, show_progress):
    if bundle == 'tdx':
        register('tdx', tdx_bundle, 'SHSZ')
    bundles_module.ingest(bundle,
                          os.environ,
                          pd.Timestamp.utcnow(),
                          assets_version,
                          show_progress,
                          )


def register_tdx():
    register('tdx', tdx_bundle, 'SHSZ')


if __name__ == '__main__':
    register('tdx1', tdx_bundle, 'SHSZ')
    bundles_module.ingest('tdx1',
                          os.environ,
                          pd.Timestamp.utcnow(),
                          show_progress=True,
                          )
    # main()
