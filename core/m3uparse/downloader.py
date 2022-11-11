import requests
import yarl

from .loader import m3u_parser


def safely_join_urls(base: yarl.URL, child: str) -> str:
    parsed_child = yarl.URL(child)

    if parsed_child.is_absolute():
        return parsed_child.human_repr()

    return base.join(parsed_child).human_repr()


def preflight(
    session: requests.Session, url: yarl.URL, headers, *, method="GET", **kwargs
):

    response = session.request(method, url.human_repr(), headers=headers, **kwargs)
    response.raise_for_status()

    data = m3u_parser(response.text.splitlines(False))

    if "PLAYLIST-TYPE" not in data:
        return {"live": True, "data": data}

    streams = data.get("streams", [])

    if not streams:
        return {"data": data}

    total_duration = sum(stream.get("duration", 0) for stream in streams)

    initial_stream = streams.pop(0)

    stream_response = session.request(
        "HEAD", safely_join_urls(url, initial_stream["url"]), headers=headers, **kwargs
    )
    stream_response.raise_for_status()

    return {
        "estimated_size": (
            int(stream_response.headers.get("content-length", 0))
            / initial_stream.get("duration", 1)
        )
        * total_duration,
        "duration": total_duration,
        "live": False,
        "data": data,
    }


def iter_stream_content(
    session: requests.Session,
    url,
    stream_data,
    *,
    headers,
    decryption_key,
    decrypter,
    **kwargs
):

    for stream in stream_data["segment"]:

        data = session.request(
            url=safely_join_urls(url, stream["url"]),
            headers=headers,
            **kwargs,
        ).content

        if decrypter:
            data = decrypter(decryption_key, data)

        yield data
