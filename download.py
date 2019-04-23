#! /usr/bin/env python
# -*- coding: utf-8 -*
import click
import logging
from urllib.request import urlretrieve
from tracts import TractDownloader2010


@click.group(help="Our custom data downloaders for this project")
def cli():
    pass


@cli.command(help="Download tract-level 'hard to count' data from the Census")
def htc():
    url = "https://census.ca.gov/wp-content/uploads/sites/4/2019/03/Tract-level-CA-HTC-Index-for-public-website-download-20190304.xlsx"
    urlretrieve(url, "data/htc/tracts.xlsx")


@cli.command(help='Download tract shapefiles from the Census')
def tracts():
    obj = TractDownloader2010()
    obj.run()


def configure_logger():
    """
    Configures logging so it prints everything to the console.
    """
    for l in ['tracts']:
        logger = logging.getLogger(l)
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s|%(name)s|%(levelname)s|%(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)


if __name__ == '__main__':
    configure_logger()
    cli()
