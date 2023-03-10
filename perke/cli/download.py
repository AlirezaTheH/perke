from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

import requests
import rich_click.typer as typer
from github import Github
from github.GitReleaseAsset import GitReleaseAsset

from perke.cli.base import app


@app.command('download')
def download_command() -> None:
    """
    Perke requires a trained POS tagger model. We use hazm's tagger
    model. This command aims to easily download latest hazm's resources
    (tagger and parser models).
    """
    download()


def download() -> None:
    """
    Function version of `download_command` to be available in the
    package.
    """
    asset = get_latest_resources_asset()
    extract_path = Path(__file__).parent.parent / 'resources'
    download_and_extract_asset(asset, extract_path)


def get_latest_resources_asset() -> GitReleaseAsset:
    """
    Searches through hazm's releases and find the latest release that
    contains resources.

    Returns
    -------
    The resources asset
    """
    g = Github()
    repo = g.get_repo('sobhe/hazm')
    for release in repo.get_releases():
        for asset in release.get_assets():
            if asset.name.startswith(f'resources-{release.tag_name[1:]}'):
                return asset


def download_and_extract_asset(
    asset: GitReleaseAsset,
    extract_path: Path,
) -> None:
    """
    Downloads a GitHub asset file and extract it.

    Parameters
    ----------
    asset:
        The GitHub asset to be downloaded

    extract_path:
        The extract path for the downloaded file to be extracted
    """
    chunk_size = 1024 * 1024
    with typer.progressbar(
        length=asset.size, label=f'Downloading {asset.name} ...', fill_char='='
    ) as progress:
        with requests.get(url=asset.browser_download_url, stream=True) as r:
            with BytesIO() as io_file:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    io_file.write(chunk)
                    progress.update(chunk_size)
                with ZipFile(io_file) as zip_file:
                    zip_file.extractall(path=extract_path)
    typer.secho('Download completed.', fg='green')
