import os
import shlex
import shutil
import sys
from datetime import date, datetime
from textwrap import dedent

import questionary
from invoke.context import Context
from invoke.main import program
from invoke.tasks import task
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
    "commit_message": f"'Publish site on {date.today().isoformat()}'",
    # Host and port for `serve`
    "host": "localhost",
    "port": 8000,
}

# templates for creating a new post

POST_TEMPLATE = dedent(
    """Title: {title}
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
    "tutorial",
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
        f"{theme_path}/templates/**/*.html",
    ]

    content_file_extensions = [".md", ".rst"]
    for extension in content_file_extensions:
        path = SETTINGS["PATH"]
        content_glob = f"{path}/**/*{extension}"
        watched_globs.append(content_glob)

    static_file_extensions = [".css", ".js"]
    for extension in static_file_extensions:
        static_file_glob = f"{theme_path}/static/**/*{extension}"
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
        uv run ruff check {python_targets} && \
        uv run cz check --rev-range origin/main..
        """
    )


@task
def format(context: Context) -> None:
    """Run autoformater on python code"""
    python_targets = "pelicanconf.py publishconf.py tasks.py"
    context.run(
        f"""
        uv run ruff check {python_targets} --fix && \
        uv run ruff format {python_targets}
        """
    )


@task
def security_check(context: Context) -> None:
    """Run pip-autid on dependencies"""
    context.run("""uv run pip-audit""")


@task
def setup_pre_commit_hooks(context: Context) -> None:
    """Setup pre-commit hook to automate check before git commit and git push"""
    context.run("git init")
    context.run(
        "uv run pre-commit install -t pre-commit & "
        "uv run pre-commit install -t pre-push & "
        "uv run pre-commit install -t commit-msg &"
        "uv run pre-commit autoupdate"
    )


@task
def run_pre_commit(context: Context) -> None:
    """Run pre-commit on all-files"""
    context.run("uv run pre-commit run --all-files")


def _ask_multiple_inputs_question(prompt: str, break_symbol: str = "!") -> str:
    questionary.print(f'{prompt} Enter "{break_symbol}" to finish"')
    answers = []
    while (answer := questionary.text("", qmark="->").ask()) != break_symbol:
        answers.append(answer)
    return ", ".join(answer)


def _validate_datetime(datetime_str: str) -> bool:
    try:
        datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
        return True
    except ValueError:
        return False


@task
def create_post(context: Context) -> None:
    """Create a new post with required metadata."""
    questionary.print("Create a new post", style="bold")

    answers = questionary.form(
        title=questionary.text(
            "Title of the post: ", validate=lambda answer: answer != ""
        ),
        date=questionary.text(
            "Date: ",
            default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            validate=_validate_datetime,
        ),
        category=questionary.select("Select a category:", choices=AVAILABLE_CATEGORIES),
    ).ask()
    tags = _ask_multiple_inputs_question("Type any number of tags.")
    authors = _ask_multiple_inputs_question("Specify any number of authors.")

    slug_title = "-".join(answers["title"].lower().split())
    slug_date = datetime.now().strftime("%Y-%m-%d")
    slug = f"{slug_date}-{slug_title}"
    summary = questionary.text("Summary: ").ask()

    rendered_template = POST_TEMPLATE.format(
        title=answers["title"],
        date=answers["date"],
        modified=answers["date"],
        category=answers["category"],
        tags=tags,
        authors=authors,
        slug=slug,
        summary=summary,
    )
    file_path = f"content/posts/{slug}.md"
    with open(file_path, "w") as out:
        out.write(rendered_template)

    questionary.print(
        f"\nFile has already been written to {file_path}.\n"
        "Please open the file to continue editing the content. Have a nice day~"
    )
