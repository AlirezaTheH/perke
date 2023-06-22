from pathlib import Path

import gdown

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
    gdown.download(
        id='1Q3JK4NVUC2t5QT63aDiVrCRBV225E_B3',
        output=str(
            Path(__file__).parent.parent / 'resources' / 'pos_tagger.model'
        ),
        quiet=False,
    )
