import pytest
from app import app as flask_app
import app as app_module


@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client


def test_projects_page_renders(monkeypatch, client):
    # Monkeypatch DAL.getAllProjects to return a controlled list
    fake_projects = [
        {'Title': 'Alpha', 'Description': 'First', 'Image': ''},
        {'Title': 'Beta', 'Description': 'Second', 'Image': 'beta.jpg'},
    ]

    # app.py imported getAllProjects directly, so patch it on the app module
    monkeypatch.setattr(app_module, 'getAllProjects', lambda: fake_projects)

    resp = client.get('/projects')
    assert resp.status_code == 200
    body = resp.get_data(as_text=True)
    assert 'Alpha' in body
    assert 'Beta' in body
    assert 'beta.jpg' in body or 'beta.jpg' in body


def test_add_project_post_redirect(monkeypatch, client):
    # Patch saveProjectDB so it doesn't touch DB
    saved = {}

    def fake_save(title, desc, image):
        saved['title'] = title
        saved['desc'] = desc
        saved['image'] = image

    # patch the save function on the app module (app.py imports it directly)
    monkeypatch.setattr(app_module, 'saveProjectDB', fake_save)

    resp = client.post('/projects/add', data={'title': 'X', 'description': 'Y', 'image': 'z.jpg'})
    # After a successful POST, endpoint redirects to /projects
    assert resp.status_code in (302, 301)
    assert saved['title'] == 'X'
    assert saved['desc'] == 'Y'
    assert saved['image'] == 'z.jpg'
