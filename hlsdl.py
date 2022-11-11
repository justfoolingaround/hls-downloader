import re
import sys

import click
import requests
import yarl
from rich.console import Console
from rich.markup import escape

from core.crypto import DECRYPTERS
from core.decorators import request_cli
from core.m3uparse.downloader import iter_stream_content, preflight, safely_join_urls

RESOLUTION_REGEX = re.compile(r"\d+x(\d+)", re.IGNORECASE)

console = Console(stderr=True)

PREFIX = escape("[remote-hls]")


@click.command()
@click.option(
    "--file",
    "-f",
    required=False,
    default="-",
    type=click.Path(allow_dash=True, file_okay=True, writable=True, resolve_path=True),
    help="File to output to.",
)
@click.option(
    "--strict",
    is_flag=True,
    help="Strictly follow the HLS specification. This will cause the program to fail if it encounters a non-compliant stream.",
)
@request_cli()
def __hls_downloader__(
    url, params, headers, method, data, timeout, file, no_verify, strict
):

    headers = dict(headers)

    session = requests.Session()
    session.headers.update(headers)

    preflight_data = preflight(
        session,
        yarl.URL(url),
        headers,
        method=method,
        params=params,
        data=data,
        timeout=timeout,
        verify=not no_verify,
    )

    stream_data = preflight_data.pop("data")
    streams = stream_data.get("segment", [])

    if not streams:
        internal_streams = stream_data.get("stream", [])

        if internal_streams:
            if strict:
                return console.print(
                    PREFIX, "[red]Cannot download from multi-stream playlist.[/red]"
                )
            else:
                highest_resolution = max(
                    internal_streams,
                    key=lambda x: int(
                        RESOLUTION_REGEX.search(x.get("RESOLUTION", "0x0")).group(1)
                    ),
                )

                url = safely_join_urls(yarl.URL(url), highest_resolution["url"])

                console.print(
                    PREFIX,
                    f"[yellow]Stream contained internal streams, selected the highest resolution {highest_resolution['RESOLUTION']!r} with URL {url!r}[/yellow]",
                )

                return __hls_downloader__.callback(
                    url=url,
                    params=params,
                    headers=headers,
                    method=method,
                    data=data,
                    timeout=timeout,
                    file=file,
                    no_verify=no_verify,
                    strict=strict,
                )

        return console.print(PREFIX, "[red]No segments found in playlist.[/red]")

    decryption_methods = stream_data.get("key", {})
    decrypter, decryption_key = None, None

    if decryption_methods:
        decrypter = DECRYPTERS.get(decryption_methods.get("METHOD"), None)
        decryption_key = session.get(
            safely_join_urls(yarl.URL(url), decryption_methods["URI"][1:-1]),
            headers=headers,
            timeout=timeout,
            verify=not no_verify,
        ).content

    if file == "-":
        console.print(PREFIX, "[green]Streaming bytes to stdout.[/]")
        writin = sys.stdout.buffer
    else:
        writin = open(file, "wb")

    for content in iter_stream_content(
        session,
        yarl.URL(url),
        stream_data,
        headers=headers,
        method=method,
        params=params,
        data=data,
        timeout=timeout,
        verify=not no_verify,
        decryption_key=decryption_key,
        decrypter=decrypter,
    ):

        writin.write(content)
        writin.flush()

    if file != "-":
        writin.close()


if __name__ == "__main__":
    __hls_downloader__()
