import re

METADATA_LINE = re.compile(r"^#EXT(?P<name>.+?)(?P<data>:.+)?$")
ATTRIBUTE_NAMES = re.compile(r"(.+?)=(.+?)(?:,|$)")

DECLARATIONS = {
    "stream_inf": "stream",
    "inf": "segment",
}


def extract_line_content(line):
    metadata_line_match = METADATA_LINE.match(line)

    if not metadata_line_match:
        return None

    field_name, data = metadata_line_match.groups()

    if field_name[:3] == "-X-":
        field_name = field_name[3:]

    field_name = field_name.lower().replace("-", "_")

    if data is None:
        return {"value": field_name}
    else:
        data = data[1:]

    attributes = ATTRIBUTE_NAMES.findall(data)

    if not attributes:
        return {field_name: data}

    return {field_name: {attribute: value for attribute, value in attributes}}


def merge_dictionaries(parent, child):

    for key, value in child.items():
        if key not in parent:
            parent[key] = value
        else:
            existing_value = parent[key]

            if not isinstance(existing_value, list):
                existing_value = [existing_value]
            if isinstance(value, list):
                existing_value.extend(value)
            else:
                existing_value.append(value)
            parent[key] = existing_value


def m3u_parser(m3u8_media_stream):

    metadata = {}

    end_of_media = False

    declaration = None
    declaration_meta = {}

    iterator = iter(enumerate(m3u8_media_stream))

    def save_declaration(url=None):
        nonlocal declaration, declaration_meta

        if declaration is not None:
            if url is not None:
                declaration_meta["url"] = url
            metadata.setdefault(declaration, []).append(declaration_meta)

        declaration, declaration_meta = None, {}

    for n, line in iterator:

        if not line.strip():
            continue

        content = extract_line_content(line)

        if content is None:
            save_declaration(line)
            continue

        if "value" in content:
            if content["value"] == "endlist":
                end_of_media = True
            continue

        if any((key in content) for key in DECLARATIONS):
            if declaration is not None:
                raise ValueError(
                    f"Unexpected redeclaration in existing declaration {n}: {line!r}"
                )

            if end_of_media:
                raise ValueError(f"Unexpected declaration after ENDLIST {n}: {line!r}")

            if "inf" in content:

                declaration = "segment"
                data = content["inf"]

                if data is None:
                    continue

                duration, title = data.split(",")

                declaration_meta.update(
                    duration=float(duration),
                )

                if title:
                    declaration_meta.update(
                        title=title,
                    )

            if "stream_inf" in content:

                if declaration is not None:
                    raise ValueError(
                        f"Unexpected redeclaration in existing declaration {n}: {line!r}"
                    )

                declaration = "stream"
                declaration_meta = content["stream_inf"]
        else:
            if declaration is not None:
                merge_dictionaries(declaration_meta, {"metadata": content})
            else:
                merge_dictionaries(metadata, content)

    return metadata
