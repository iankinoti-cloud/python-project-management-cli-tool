from click.testing import CliRunner

from commands import cli


def test_cli_command_flow(tmp_path):
    data_file = tmp_path / "data.json"
    runner = CliRunner()

    result = runner.invoke(cli, ["--data-file", str(data_file), "user", "create", "--name", "Alice", "--email", "alice@example.com"])
    assert result.exit_code == 0
    assert "Created user [1] Alice <alice@example.com>" in result.output

    result = runner.invoke(cli, ["--data-file", str(data_file), "project", "add", "--user-id", "1", "--name", "Website Redesign"])
    assert result.exit_code == 0
    assert "Created project [1] Website Redesign" in result.output

    result = runner.invoke(cli, [
        "--data-file",
        str(data_file),
        "task",
        "add",
        "--project-id",
        "1",
        "--title",
        "Design mockups",
        "--description",
        "Create wireframes",
        "--contributors",
        "1",
    ])
    assert result.exit_code == 0
    assert "Created task [1] Design mockups [open]" in result.output

    result = runner.invoke(cli, ["--data-file", str(data_file), "task", "list", "--project-id", "1"])
    assert result.exit_code == 0
    assert "[1] Design mockups [open]" in result.output


def test_cli_error_for_missing_user(tmp_path):
    data_file = tmp_path / "data.json"
    runner = CliRunner()

    result = runner.invoke(cli, ["--data-file", str(data_file), "project", "add", "--user-id", "999", "--name", "No Owner"])
    assert result.exit_code != 0
    assert "User 999 not found" in result.output
