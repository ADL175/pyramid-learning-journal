import pytest
import transaction
from pyramid import testing
from pyramid_learning_journal.models import Journal, get_tm_session
from pyramid_learning_journal.models.meta import Base
import os
import io

# =================== FUNCTIONAL TESTS =============


@pytest.fixture
def testapp(request):
    """Create a test application to use for functional tests."""
    from pyramid_learning_journal import main
    from webtest import TestApp
    from pyramid.config import Configurator

    def main(global_config, **settings):
        """ This function returns a Pyramid WSGI application.
        """
        settings['sqlalchemy.url'] = os.environ.get('DATABASE_URL_TEST')
        config = Configurator(settings=settings)
        config.include('pyramid_jinja2')
        config.include('.models')
        config.include('.routes')
        config.scan()
        return config.make_wsgi_app()

    app = main({})
    testapp = TestApp(app)

    SessionFactory = app.registry["dbsession_factory"]
    engine = SessionFactory().bind
    Base.metadata.create_all(bind=engine)

    def tearDown():
        Base.metadata.drop_all(bind=engine)

    request.addfinalizer(tearDown)

    return testapp


# def test_home_route_returns_home_content(testapp):
#     """Test the thome route returns home content."""
#     response = testapp.get('/')
#     html = response.html
#     assert 'Journal' in str(html.find('h1').text)
#     assert 'Journal' in str(html.find('title').text)
#
#
# def test_home_route_has_h1(testapp):
#     """The home page has a table in the html."""
#     response = testapp.get('/', status=200)
#     html = response.html
#     assert len(html.find_all("h1")) == 2


@pytest.fixture
def new_session(testapp):
    """Return a session for inspecting the database."""
    SessionFactory = testapp.app.registry["dbsession_factory"]
    with transaction.manager:
        dbsession = get_tm_session(SessionFactory, transaction.manager)
    return dbsession


# def test_home_route_is_found(testapp):
#     """The home page has a good route."""
#     response = testapp.get('/', status=200)
#     assert response.status_code == 200
#
#
# def test_detail_route_is_found(testapp):
#     """The detail page has a good route."""
#     response = testapp.get('/journal/1', status=200)
#     assert response.status_code == 200
#
#
# def test_detail_route_is_not_found(testapp):
#     """The detail page has a bad route."""
#     response = testapp.get('/journal/1123', status=404)
#     assert response.status_code == 404


def test_create_route_is_found(testapp):
    """The create page has a table in the html."""
    response = testapp.get('/journal/new-journal', status=200)
    assert response.status_code == 200


# def test_edit_route_is_found(testapp):
#     """The edit page is a good route."""
#     response = testapp.get('/journal/1/edit', status=200)
#     assert response.status_code == 200
#
#
# def test_edit_route_is_not_found(testapp):
#     """The edit page is a bad route."""
#     response = testapp.get('/journal/asdf/edit', status=404)
#     assert response.status_code == 404


def test_user_can_create_new_post(testapp):
    """User can post new post."""
    # import pdb; pdb.set_trace()
    testapp.post("/journal/new-journal", params={
        "title": "Test Title for Pytest",
        "body": "Lorem ipsum dolor sit amet, consectetur adipisicing elit."
    })
    response = testapp.get('/')
    assert "Test Title for Pytest" in response.text

#
# def test_user_can_edit_post(testapp):
#     """User can post edit post."""
#     response = testapp.get("/journal/4/edit")
#     testapp.post('/journal/4/edit', params={
#         "title": "Edited title for Pytest",
#         "body" : "Lorem ipsum dolor sit amet."
#     })
#     response = testapp.get('/journal/4')
#     assert "Edited title for Pytest" in response.text
