import os
import tempfile
from DAL import DB_FILE, ensure_db, saveProjectDB, getAllProjects


def test_database_create_and_seed(tmp_path, monkeypatch):
    # Use a temporary database file to avoid touching the real DB
    tmp_db = tmp_path / "test_projects.db"

    # Monkeypatch the DB_FILE constant inside DAL by setting the attribute on the module
    import importlib
    import DAL as dal_mod

    monkeypatch.setattr(dal_mod, 'DB_FILE', str(tmp_db))

    # Ensure DB creation and seeding runs without error
    dal_mod.ensure_db()

    # After seeding, there should be at least the two seeded rows
    rows = dal_mod.getAllProjects()
    assert isinstance(rows, list)
    assert len(rows) >= 2
    assert any('Workday' in r['Title'] for r in rows)


def test_save_project_and_retrieve(tmp_path, monkeypatch):
    tmp_db = tmp_path / "test_projects2.db"
    import DAL as dal_mod
    monkeypatch.setattr(dal_mod, 'DB_FILE', str(tmp_db))

    # Ensure DB and no rows initially (ensure_db will seed rows if empty)
    dal_mod.ensure_db()

    # Save a new project and verify it appears in getAllProjects()
    dal_mod.saveProjectDB('Test Project', 'A test description', 'test.jpg')
    all_projects = dal_mod.getAllProjects()

    assert any(p['Title'] == 'Test Project' and p['Image'] == 'test.jpg' for p in all_projects)
