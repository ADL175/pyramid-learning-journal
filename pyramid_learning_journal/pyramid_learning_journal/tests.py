import pytest
from pyramid import testing
import transaction
from pyramid.httpexceptions import HTTPNotFound
import os
import io
from pyramid_learning_journal.models.meta import Base

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


# def test_detail_view_returns_dict(testapp):
#     """Home view returns a dictionary of values."""
#     from pyramid_learning_journal.views.default import detail_view
#     response = detail_view(testapp)
#     assert isinstance(response, dict)


# def test_detail_view_returns_count_matching_database(testapp):
#     """Home view response matches database count."""
#     from pyramid_learning_journal.views.default import detail_view
#     response = detail_view(testapp)
#     query = testapp.dbsession.query(Journal)
#     assert len(response['journal']) == query.count()


# def test_detail_route_returns_proper_content(testapp):
#     """Test the detail route returns proper journal entry."""
#     response = testapp.get('/journal/1')
#     html = response.html
#     import pdb; pdb.set_trace()
#     assert


    # config.add_route('detail', '/journal/{id:\d+}')
