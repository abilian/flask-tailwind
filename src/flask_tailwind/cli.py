"""Console script for flask_tailwind."""
import shutil
import sys
from pathlib import Path

import click
from devtools import debug
from flask import current_app
from flask.cli import with_appcontext

from .npm import NPM


@click.group()
def tailwind():
    """Perform Tailwind operations."""
    pass


# @db.command()
# @click.option('-d', '--directory', default=None,
#               help=('Migration script directory (default is "migrations")'))
# @click.option('--multidb', is_flag=True,
#               help=('Support multiple databases'))
# @click.option('-t', '--template', default=None,
#               help=('Repository template to use (default is "flask")'))
# @click.option('--package', is_flag=True,
#               help=('Write empty __init__.py files to the environment and '
#                     'version locations'))
# @with_appcontext
# def init(directory, multidb, template, package):
#     """Creates a new migration repository."""
#     _init(directory, multidb, template, package)


@tailwind.command()
@with_appcontext
def init():
    source_dir = Path(__file__).parent / "cruft"
    dest_dir = current_app.root_path
    debug(source_dir, dest_dir)
    # shutil.copy(source_dir, )
    return

    # app_path = cookiecutter(
    #     os.path.dirname(os.path.dirname(os.path.dirname())),
    #     output_dir=os.getcwd(),
    #     directory="app_template",
    #     no_input=options["no_input"],
    #     overwrite_if_exists=False,
    #     extra_context={
    #         "app_name": options["app_name"] if options.get("app_name") else "theme"
    #     },
    # )
    #
    # app_name = os.path.basename(app_path)
    #
    # self.stdout.write(
    #     self.style.SUCCESS(
    #         f"Tailwind application '{app_name}' "
    #         f"has been successfully created. "
    #         f"Please add '{app_name}' to INSTALLED_APPS in settings.py."
    #     )
    # )


@tailwind.command()
@with_appcontext
def install():
    npm_run("install")


@tailwind.command()
@with_appcontext
def build(self, **options):
    npm_run("run", "build")


@tailwind.command()
@with_appcontext
def start(self, **options):
    """Start watching css changes for dev."""
    npm_run("run", "start")
    # if options.get("no_sync"):
    #     self.npm_command("run", "dev:tailwind")
    # else:
    #     self.npm_command("run", "start")


@tailwind.command()
@with_appcontext
def check_updates():
    """Check outdated Tailwind dependencies."""
    npm_run("outdated")


@tailwind.command()
@with_appcontext
def update():
    """Update Tailwind and its dependencies, if needed."""
    npm_run("update")


@tailwind.command()
@with_appcontext
def npm(*args):
    """Call directly npm with given args."""
    npm_run(*args)


def npm_run(*args):
    npm = NPM()

    # class Command(LabelCommand):
    #     help = "Runs tailwind commands"
    #     missing_args_message = """
    # Command argument is missing, please add one of the following:
    #   init - to initialize django-tailwind app
    #   install - to install npm packages necessary to build tailwind css
    #   build - to compile tailwind css into production css
    #   start - to start watching css changes for dev
    #   check-updates - to list possible updates for tailwind css and its dependencies
    #   update - to update tailwind css and its dependencies
    # Usage example:
    #   python manage.py tailwind start
    # """
    npm = None
    validate = None

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.validate = Validations()

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            "--no-sync",
            action="store_true",
            help="Starts Tailwind dev server without browser sync",
        )
        parser.add_argument(
            "--no-input",
            action="store_true",
            help="Initializes Tailwind project without user prompts",
        )
        parser.add_argument(
            "--app-name",
            help="Sets default app name on Tailwind project initialization",
        )

    def validate_app(self):
        try:
            self.validate.has_settings()
            app_name = get_config("TAILWIND_APP_NAME")
            self.validate.is_installed(app_name)
            self.validate.is_tailwind_app(app_name)
        except ValidationError as err:
            raise CommandError(err)

    def handle(self, *labels, **options):
        return self.handle_labels(*labels, **options)

    def handle_labels(self, *labels, **options):
        self.validate.acceptable_label(labels[0])
        if labels[0] != "init":
            self.validate_app()
            self.npm = NPM(cwd=get_tailwind_src_path(get_config("TAILWIND_APP_NAME")))

        getattr(self, "handle_" + labels[0].replace("-", "_") + "_command")(
            *labels[1:], **options
        )
