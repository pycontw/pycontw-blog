# -*- coding: utf-8 -*-

from datetime import datetime, date
from textwrap import dedent
import os
import shlex
import shutil
import sys

from invoke.tasks import task
from invoke.main import program
from invoke.context import Context
from pelican import main as pelican_main
from pelican.server import ComplexHTTPRequestHandler, RootedHTTPServer
from pelican.settings import DEFAULT_CONFIG, get_settings_from_file

# Default pelican task.py settings
OPEN_BROWSER_ON_SERVE = True
SETTINGS_FILE_BASE = "pelicanconf.py"
SETTINGS = {}
SETTINGS.update(DEFAULT_CONFIG)
LOCAL_SETTINGS = get_settings_from_file(SETTINGS_FILE_BASE)
SETTINGS.update(LOCAL_SETTINGS)

CONFIG = {
    "settings_base": SETTINGS_FILE_BASE,
    "settings_publish": "publishconf.py",
    # Output path. Can be absolute or relative to tasks.py. Default: 'output'
    "deploy_path": SETTINGS["OUTPUT_PATH"],
    # Github Pages configuration
    "github_pages_branch": "gh-pages",
    "commit_message": "'Publish site on {}'".format(date.today().isoformat()),
    # Host and port for `serve`
    "host": "localhost",
    "port": 8000,
}

# templates for creating a new post

POST_TEMPLATE = dedent(
    """
    Title: {title}
    Date: {date}
    Modified: {modified}
    Category: {category}
    Tags: {tags}
    Slug: {slug}
    Authors: {authors}
    Summary: {summary}

    [TOC]

    ---
    <!--your content here-->
"""
)


AVAILABLE_CATEGORIES = [
    "announcement",
    "interview",
    "online-conference",
    "programs",
    "registration",
    "sponsors",
    "tutoiral",
    "visiting group",
]


@task
def clean(context: Context) -> None:
    """Remove generated files"""
    if os.path.isdir(CONFIG["deploy_path"]):
        shutil.rmtree(CONFIG["deploy_path"])
        os.makedirs(CONFIG["deploy_path"])


@task
def build(context: Context) -> None:
    """Build local version of site"""
    pelican_run("-s {settings_base}".format(**CONFIG))


@task
def rebuild(context: Context) -> None:
    """`build` with the delete switch"""
    pelican_run("-d -s {settings_base}".format(**CONFIG))


@task
def regenerate(context: Context) -> None:
    """Automatically regenerate site upon file modification"""
    pelican_run("-r -s {settings_base}".format(**CONFIG))


@task
def serve(context: Context) -> None:
    """Serve site at http://$HOST:$PORT/ (default is localhost:8000)"""

    class AddressReuseTCPServer(RootedHTTPServer):
        allow_reuse_address = True

    server = AddressReuseTCPServer(
        CONFIG["deploy_path"],
        (CONFIG["host"], CONFIG["port"]),
        ComplexHTTPRequestHandler,
    )

    if OPEN_BROWSER_ON_SERVE:
        # Open site in default browser
        import webbrowser

        webbrowser.open("http://{host}:{port}".format(**CONFIG))

    sys.stderr.write("Serving at {host}:{port} ...\n".format(**CONFIG))
    server.serve_forever()


@task
def reserve(context: Context) -> None:
    """`build`, then `serve`"""
    build(context)
    serve(context)


@task
def preview(context: Context) -> None:
    """Build production version of site"""
    pelican_run("-s {settings_publish}".format(**CONFIG))


@task
def livereload(context: Context) -> None:
    """Automatically reload browser tab upon file modification."""
    from livereload import Server

    def cached_build():
        cmd = "-s {settings_base} -e CACHE_CONTENT=true LOAD_CONTENT_CACHE=true"
        pelican_run(cmd.format(**CONFIG))

    cached_build()
    server = Server()
    theme_path = SETTINGS["THEME"]
    watched_globs = [
        CONFIG["settings_base"],
        "{}/templates/**/*.html".format(theme_path),
    ]

    content_file_extensions = [".md", ".rst"]
    for extension in content_file_extensions:
        content_glob = "{0}/**/*{1}".format(SETTINGS["PATH"], extension)
        watched_globs.append(content_glob)

    static_file_extensions = [".css", ".js"]
    for extension in static_file_extensions:
        static_file_glob = "{0}/static/**/*{1}".format(theme_path, extension)
        watched_globs.append(static_file_glob)

    for glob in watched_globs:
        server.watch(glob, cached_build)

    if OPEN_BROWSER_ON_SERVE:
        # Open site in default browser
        import webbrowser

        webbrowser.open("http://{host}:{port}".format(**CONFIG))

    server.serve(host=CONFIG["host"], port=CONFIG["port"], root=CONFIG["deploy_path"])


@task
def build_publish(context: Context) -> None:
    """Build pages with publishconf.py"""
    pelican_run("-s {settings_publish}".format(**CONFIG))


@task
def gh_pages(context: Context) -> None:
    """Publish to GitHub Pages"""
    preview(context)
    context.run(
        "ghp-import -b {github_pages_branch} "
        "-m {commit_message} "
        "{deploy_path} -p".format(**CONFIG)
    )


def pelican_run(cmd):
    cmd += " " + program.core.remainder  # allows to pass-through args to pelican
    pelican_main(shlex.split(cmd))


@task
def style(context: Context) -> None:
    """Run style check on python code"""
    python_targets = "pelicanconf.py publishconf.py tasks.py"
    context.run(
        f"""
        pipenv run ruff check {python_targets} && \
        pipenv run black --check {python_targets} && \
        pipenv run cz check --rev-range origin/main..
        """
    )


@task
def format(context: Context) -> None:
    """Run autoformater on python code"""
    python_targets = "pelicanconf.py publishconf.py tasks.py"
    context.run(
        f"""
        pipenv run ruff format {python_targets} && \
        pipenv run black {python_targets}
        """
    )


@task
def security_check(c):
    """Run pip-autid on dependencies"""
    c.run(
        """
        pipenv requirements > requirements.txt && \
        pipenv run pip-audit -r requirements.txt && \
        rm -rf requirements.txt
        """
    )


def _input_date() -> str:
    default_time = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    return input(f"Date (default: {default_time}): ") or default_time


def _input_category() -> str:
    print("Select a category:")
    for idx, cat in enumerate(AVAILABLE_CATEGORIES):
        print(f"{idx}. {cat}")

    selection = int(input("Your selection (default: 0): ") or 0)
    if selection < 0 or selection >= len(AVAILABLE_CATEGORIES):
        raise ValueError(f"Numbers should be within 0~{len(AVAILABLE_CATEGORIES) - 1}")

    return AVAILABLE_CATEGORIES[selection]


def _input_tags() -> str:
    print('Type any number of tags. Enter "!" to finish\n')
    tags = []
    while (tag := input("-> ")) != "!":
        tags.append(tag)
    return ", ".join(tags)


def _input_authors() -> str:
    print('Specify any number of authors. Enter "!" to finish\n')
    authors = []
    while (author := input("-> ")) != "!":
        authors.append(author)
    return ", ".join(authors)


@task
def create_post(context: Context) -> None:
    """Create a new post with required metadata."""
    print("Create a new post to pycontw-blog\n".title())

    title = input("Title of the post: ")
    date = modified = _input_date()
    category = _input_category()
    tags = _input_tags()
    authors = _input_authors()

    slug_title = "-".join(title.lower().split())
    slug_date = datetime.now().strftime("%Y-%m-%d")
    slug = f"{slug_date}-{slug_title}"
    summary = input("Summary: ")

    rendered_template = POST_TEMPLATE.format(
        title=title,
        date=date,
        modified=modified,
        category=category,
        tags=tags,
        authors=authors,
        slug=slug,
        summary=summary,
    )
    file_path = f"content/posts/{slug}.md"
    with open(file_path, "w") as out:
        out.write(rendered_template)

    print(f"\nFile has already been written to {file_path}.")
    print("Please open the file to continue editing the content. Have a nice day~")
