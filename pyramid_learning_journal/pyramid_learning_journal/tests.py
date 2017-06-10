import pytest
import transaction
from pyramid import testing
from pyramid_learning_journal.models.meta import Base
import os

SITE_ROOT = 'http://localhost'


@pytest.fixture(scope="session")
def configuration(request):
    """Sets up a configurator instance.
    Configuraor instance sets up a pointer to the lcoation of the database.
    It includes the models from apps model package.
    Finally, it tears everything down, including the in memory SQL Lite database.
    This configuration will persist for the entire duration of your pytest run."""
    config = testing.setUp(settings={
        'sqlalchemy.url': 'postgres://localhost:5432/psycotest_test'
    })
    config.include("pyramid_learning_journal.models")
    config.include("pyramid_learning_journal.routes")

    def teardown():
        testing.tearDown()

    request.addfinalizer(teardown)
    return config


@pytest.fixture
def db_session(configuration, request):
    """Creates a session for interacting witht the test databaseself.
    This uses the dbsession_factory on the configurator instacne to create a new databse session. It binds that session to the available engine and rturns a new session for every call of the dummy_request object."""
    SessionFactory = configuration.registry["dbsession_factory"]
    session = SessionFactory()
    engine = session.bind
    Base.metadata.create_all(engine)

    def teardown():
        session.transaction.rollback()
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def dummy_request(db_session):
    from pyramid import testing
    req = testing.DummyRequest()
    req.dbsession = db_session
    return req


@pytest.fixture
def post_request(dummy_request):
    dummy_request.method = "POST"
    return dummy_request


@pytest.fixture
def set_credentials():
    from pyramid_learning_journal.security import context
    import os
    os.environ['AUTH_PASSWORD'] = context.hash('flamingo')


def test_create_view_post_empty_data_returns_empty_dict(post_request):
    from pyramid_learning_journal.views.default import create_view
    response = create_view(post_request)
    assert response == {}


def test_create_view_post_incomplete_data_returns_error(post_request):
    from pyramid_learning_journal.views.default import create_view
    data = {
        'title': '',
        'body': ''
    }
    post_request.POST = data
    response = create_view(post_request)
    assert 'error' in response


def test_create_view_post_incomplete_data_returns_data(post_request):
    from pyramid_learning_journal.views.default import create_view
    data = {
        'title': 'blah blah',
        'body': ''
    }
    post_request.POST = data
    response = create_view(post_request)
    assert 'title' in response
    assert 'body' in response
    assert response['title'] == 'blah blah'
    assert response['body'] == ''


def test_create_view_post_with_data_redirects(post_request):
    from pyramid_learning_journal.views.default import create_view
    from pyramid.httpexceptions import HTTPFound
    data = {
        'title': 'blah blah',
        'body': 'boo boo boo'
    }
    post_request.POST = data
    response = create_view(post_request)
    assert response.status_code == 302
    assert isinstance(response, HTTPFound)


def test_login_bad_credentials_fails(post_request):
    from pyramid_learning_journal.views.default import login
    data = {
        'username': 'armydavidlim',
        'password': 'not_poop'
    }
    post_request.POST = data
    response = login(post_request)
    assert response == {'error': 'Bad username or password'}


def test_get_login_returns_dict(dummy_request):
    from pyramid_learning_journal.views.default import login
    dummy_request.method = "GET"
    response = login(dummy_request)
    assert response == {}
#
# WIP NOT WORKING
# def test_login_is_successful_with_good_creds(post_request, set_credentials):
#     from pyramid_learning_journal.views.default import login
#     from pyramid.httpexceptions import HTTPFound
#     data = {
#         'username': 'armydavidlim',
#         'password': 'poop'
#     }
#     post_request.POST = data
#     response = login(post_request)
#     assert isinstance(response, HTTPFound)
#
#
def test_logout_redirects(dummy_request):
    from pyramid_learning_journal.views.default import logout
    from pyramid.httpexceptions import HTTPFound
    response = logout(dummy_request)
    assert isinstance(response, HTTPFound)


#=============INTEGRATION TESTS AFTER THIS POINT==============

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


def test_home_route_returns_home_content(testapp):
    """Test the thome route returns home content."""
    response = testapp.get('/')
    html = response.html
    assert 'Journal' in str(html.find('h1').text)
    assert 'Journal' in str(html.find('title').text)


def test_home_route_has_h1(testapp):
    """The home page has a table in the html."""
    response = testapp.get('/', status=200)
    html = response.html
    assert len(html.find_all("h1")) == 2


@pytest.fixture
def new_session(testapp):
    """Return a session for inspecting the database."""
    SessionFactory = testapp.app.registry["dbsession_factory"]
    with transaction.manager:
        dbsession = get_tm_session(SessionFactory, transaction.manager)
    return dbsession


def test_home_route_is_found(testapp):
    """The home page has a good route."""
    response = testapp.get('/', status=200)
    assert response.status_code == 200
#
#WIP
# def test_detail_route_is_found(testapp):
#     """The detail page has a good route."""
#     response = testapp.get('/journal/1', status=200)
#     assert response.status_code == 200
#
#
def test_detail_route_is_not_found(testapp):
    """The detail page has a bad route."""
    response = testapp.get('/journal/1123', status=404)
    assert response.status_code == 404

# WIP
# def test_create_route_is_found(testapp):
#     """The create page has a table in the html."""
#     response = testapp.get('/journal/new-journal', status=200)
#     assert response.status_code == 200

# WIP
# def test_edit_route_is_found(testapp):
#     """The edit page is a good route."""
#     response = testapp.get('/journal/1/edit', status=200)
#     assert response.status_code == 200
#
# WIP#
# def test_edit_route_is_not_found(testapp):
#     """The edit page is a bad route."""
#     response = testapp.get('/journal/asdf/edit', status=404)
#     assert response.status_code == 404

# WIP
# def test_user_can_create_new_post(testapp):
#     """User can post new post."""
#     # import pdb; pdb.set_trace()
#     testapp.post("/journal/new-journal", params={
#         "title": "Test Title for Pytest",
#         "body": "Lorem ipsum dolor sit amet, consectetur adipisicing elit."
#     })
#     response = testapp.get('/')
#     assert "Test Title for Pytest" in response.text

# WIP#
# def test_user_can_edit_post(testapp):
#     """User can post edit post."""
#     response = testapp.get("/journal/4/edit")
#     testapp.post('/journal/4/edit', params={
#         "title": "Edited title for Pytest",
#         "body" : "Lorem ipsum dolor sit amet."
#     })
#     response = testapp.get('/journal/4')
#     assert "Edited title for Pytest" in response.text
