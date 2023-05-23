from pathlib import Path
from os import path, makedirs
from jinja2 import Environment, PackageLoader, select_autoescape
import importlib


def verify_template_directory():
    directory = Path(path.join(path.abspath(__file__), "..", "..", "templates"))

    if not directory.is_dir():
        makedirs(directory)


def verify_template_layout(application):
    if not application._layout:
        return

    layout_file = Path(
        path.join(
            path.abspath(__file__),
            "..",
            "..",
            "templates",
            f"{application.name.lower()}.html",
        )
    )

    if not layout_file.is_file():
        f = open(layout_file, "x")
        f.write(application._layout)
        f.close()


def get_jinja_env_object():
    return Environment(loader=PackageLoader("cyclone"), autoescape=select_autoescape())


def parse_incoming_template(template: str) -> str:
    return template.replace("+#<", "{{").replace("+#>", "}}")


def parse_outgoing_template(template: str) -> str:
    return template.replace("{{", "+#<").replace("}}", "+#>")
