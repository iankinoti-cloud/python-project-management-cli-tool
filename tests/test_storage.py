import pytest

from storage import DataStore


def test_data_store_basic_lifecycle(tmp_path):
    data_file = tmp_path / "data.json"
    store = DataStore(path=str(data_file))

    user = store.add_user("Alice", "alice@example.com")
    assert user.id == 1
    assert user.name == "Alice"

    project = store.add_project(user.id, "Website Redesign")
    assert project.id == 1
    assert project.owner_user_id == user.id

    task = store.add_task(project.id, "Design mockups", "Create wireframes", contributor_ids=[user.id])
    assert task.id == 1
    assert task.status == "open"
    assert user.id in task.contributor_ids

    reloaded = DataStore(path=str(data_file))
    assert len(reloaded.list_users()) == 1
    assert reloaded.list_projects(user_id=user.id)[0].id == project.id
    assert reloaded.list_tasks(project_id=project.id)[0].id == task.id

    completed = reloaded.complete_task(task.id)
    assert completed.status == "complete"

    assigned = reloaded.assign_contributor(task.id, user.id)
    assert assigned.contributor_ids == [user.id]


def test_data_store_invalid_project_user(tmp_path):
    data_file = tmp_path / "data.json"
    store = DataStore(path=str(data_file))

    with pytest.raises(KeyError, match="User 999 not found"):
        store.add_project(999, "No Owner")
