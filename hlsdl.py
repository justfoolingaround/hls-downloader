from pathlib import Path

import click
import httpx

from core.download import hls_download
from core.utils import *


@click.command()
@click.option('-i', '--input', required=True, help="Input url for the stream.")
@click.option('-o', '--output', required=False, default='./output.ts', help="Output file to which the stream is to be downloaded.")
@click.option('-pq', '--preferred-quality', required=False, default=1080, type=int, help="Preferred quality for downloading.")
@click.option('--headers', default='', required=False, help="Access headers for the stream.")
@click.option('-q', '--quiet', is_flag=True, flag_value=True)
def __hls_downloader__(input, output, preferred_quality, headers, unverify, quiet):
    session = httpx.Client()
    
    tqdm = None
    has_tqdm = False

    try:
        from tqdm import tqdm
        has_tqdm = True
    except ImportError:
        pass
    
    if quiet:
        has_tqdm = False
    return hls_download(session, output, input, convert_headers_to_dict(headers), preferred_quality, Path(output), (lambda *args, **kwargs: tqdm(*args, **kwargs)) if has_tqdm else None)
    
if __name__ == '__main__':
    __hls_downloader__()
