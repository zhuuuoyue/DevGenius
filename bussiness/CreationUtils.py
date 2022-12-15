# coding: utf-8

def create_file(path: str, content: str) -> None:
    with open(path, "w", encoding="utf8") as fp:
        fp.write(f"\uFEFF{content}")
