from pathlib import Path
from typing import Optional

import click

from storage import DataStore, DataStoreError


def format_user(user: object) -> str:
    return f"[{user.id}] {user.name} <{user.email}> (projects: {len(user.project_ids)})"


def format_project(project: object) -> str:
    return f"[{project.id}] {project.name} (owner: {project.owner_user_id}, tasks: {len(project.task_ids)})"


def format_task(task: object) -> str:
    contributors = ", ".join(str(uid) for uid in task.contributor_ids) if task.contributor_ids else "none"
    return f"[{task.id}] {task.title} [{task.status}] (project: {task.project_id}, contributors: {contributors})"


@click.group()
@click.option(
    "--data-file",
    type=click.Path(dir_okay=False, writable=True),
    default=None,
    help="Path to the data file for persistence.",
)
@click.pass_context
def cli(ctx: click.Context, data_file: Optional[str]) -> None:
    ctx.ensure_object(dict)
    ctx.obj["data_file"] = Path(data_file) if data_file else None


def get_store(ctx: click.Context) -> DataStore:
    return DataStore(path=str(ctx.obj["data_file"]) if ctx.obj.get("data_file") else None)


@cli.group(help="Manage users")
@click.pass_context
def user(ctx: click.Context) -> None:
    pass


@user.command("create", help="Create a new user")
@click.option("--name", required=True, help="User name")
@click.option("--email", required=True, help="User email")
@click.pass_context
def create_user(ctx: click.Context, name: str, email: str) -> None:
    store = get_store(ctx)
    try:
        user = store.add_user(name, email)
        click.echo(f"Created user {format_user(user)}")
    except DataStoreError as exc:
        raise click.ClickException(str(exc))


@user.command("list", help="List users")
@click.option("--verbose", is_flag=True, help="Show detailed user info")
@click.pass_context
def list_users(ctx: click.Context, verbose: bool) -> None:
    store = get_store(ctx)
    users = store.list_users()
    if not users:
        click.echo("No users found.")
        return
    for user in users:
        click.echo(format_user(user) if not verbose else repr(user))


@cli.group(help="Manage projects")
@click.pass_context
def project(ctx: click.Context) -> None:
    pass


@project.command("add", help="Add a project for a user")
@click.option("--user-id", type=int, required=True, help="Owner user ID")
@click.option("--name", required=True, help="Project name")
@click.pass_context
def add_project(ctx: click.Context, user_id: int, name: str) -> None:
    store = get_store(ctx)
    try:
        project = store.add_project(user_id, name)
        click.echo(f"Created project {format_project(project)}")
    except (KeyError, DataStoreError) as exc:
        raise click.ClickException(str(exc))


@project.command("list", help="List projects")
@click.option("--user-id", type=int, help="Filter by user ID")
@click.pass_context
def list_projects(ctx: click.Context, user_id: Optional[int]) -> None:
    store = get_store(ctx)
    try:
        projects = store.list_projects(user_id=user_id)
        if not projects:
            click.echo("No projects found.")
            return
        for project in projects:
            click.echo(format_project(project))
    except KeyError as exc:
        raise click.ClickException(str(exc))


@cli.group(help="Manage tasks")
@click.pass_context
def task(ctx: click.Context) -> None:
    pass


@task.command("add", help="Add a task to a project")
@click.option("--project-id", type=int, required=True, help="Project ID")
@click.option("--title", required=True, help="Task title")
@click.option("--description", default="", help="Task description")
@click.option("--contributors", type=int, multiple=True, help="Contributor user IDs")
@click.pass_context
def add_task(ctx: click.Context, project_id: int, title: str, description: str, contributors: tuple) -> None:
    store = get_store(ctx)
    try:
        task = store.add_task(
            project_id=project_id,
            title=title,
            description=description,
            contributor_ids=list(contributors),
        )
        click.echo(f"Created task {format_task(task)}")
    except (KeyError, DataStoreError) as exc:
        raise click.ClickException(str(exc))


@task.command("list", help="List tasks")
@click.option("--project-id", type=int, help="Filter by project ID")
@click.pass_context
def list_tasks(ctx: click.Context, project_id: Optional[int]) -> None:
    store = get_store(ctx)
    try:
        tasks = store.list_tasks(project_id=project_id)
        if not tasks:
            click.echo("No tasks found.")
            return
        for task in tasks:
            click.echo(format_task(task))
    except KeyError as exc:
        raise click.ClickException(str(exc))


@task.command("complete", help="Mark a task complete")
@click.option("--task-id", type=int, required=True, help="Task ID")
@click.pass_context
def complete_task(ctx: click.Context, task_id: int) -> None:
    store = get_store(ctx)
    try:
        task = store.complete_task(task_id)
        click.echo(f"Task completed: {format_task(task)}")
    except (KeyError, DataStoreError) as exc:
        raise click.ClickException(str(exc))


@task.command("assign", help="Assign a contributor to a task")
@click.option("--task-id", type=int, required=True, help="Task ID")
@click.option("--user-id", type=int, required=True, help="Contributor user ID")
@click.pass_context
def assign_task(ctx: click.Context, task_id: int, user_id: int) -> None:
    store = get_store(ctx)
    try:
        task = store.assign_contributor(task_id, user_id)
        click.echo(f"Assigned contributor {user_id} to task: {format_task(task)}")
    except (KeyError, DataStoreError) as exc:
        raise click.ClickException(str(exc))

