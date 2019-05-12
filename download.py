import us
import click
import logging
from tracts import USTractDownloader2010
import census_data_downloader
CENSUS_API_KEY = "2406531db87ec547327b463ef193df1afe91b80b"


@click.group(help="Download data about Native Americans")
def cli():
    pass


@cli.command(help="Download tract maps")
def tracts():
    USTractDownloader2010(data_dir="data/tiger/").run()


@cli.command(help='Download race data')
@click.option('--force', is_flag=True, help="Redownload raw data from the Census")
def race(force):
    runner = census_data_downloader.RaceDownloader(
       CENSUS_API_KEY,
       data_dir="/media/palewire/Passport/htc",
       force=force
    )
    runner.download_counties()
    for state in us.STATES:
        runner.download_tracts(state.abbr)


@cli.command(help='Download Internet service data')
@click.option('--force', is_flag=True, help="Redownload raw data from the Census")
def internet(force):
    runner = census_data_downloader.InternetDownloader(
       CENSUS_API_KEY,
       data_dir="/media/palewire/Passport/htc",
       force=force
    )
    for state in us.STATES:
        runner.download_tracts(state.abbr)
    runner.download_counties()


@cli.command(help='Download language data')
@click.option('--force', is_flag=True, help="Redownload raw data from the Census")
def language(force):
    runner = census_data_downloader.LanguageDownloader(
       CENSUS_API_KEY,
       data_dir="/media/palewire/Passport/htc",
       force=force
    )
    for state in us.STATES:
        runner.download_tracts(state.abbr)
    runner.download_counties()


def configure_logger():
    """
    Configures logging so it prints everything to the console.
    """
    for l in ['census_data_downloader', "tracts"]:
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
