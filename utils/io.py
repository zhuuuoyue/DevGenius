# coding: utf-8

def save_file_as_utf8_bom(path: str, content: str) -> None:
    with open(path, "w", encoding="utf8") as fp:
        fp.write(f"\uFEFF{content}")
