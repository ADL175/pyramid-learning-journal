from pyramid import testing
from pyramid.httpexceptions import HTTPNotFound
import pytest
import os
import io
from pyramid_learning_journal.models.meta import Base
# from pyramid_learning_journal.views.default import JOURNALS
# from pyramid import testing
# from pyramid.response import Response
# import pytest



# HERE = os.path.dirname(__file__)
#
#
# @pytest.fixture
# def httprequest():
#     req = testing.DummyRequest()
#     return req


# def test_return_of_views_are_responses():
#     """Test if the return of views are responses."""
#     from pyramid_learning_journal.views.default import (
#         home_view,
#         detail_view
#     )
#     assert isinstance(list_view(httprequest), Response)
#     assert isinstance(detail_view(httprequest), Response)
#     assert isinstance(create_view(httprequest), Response)
#     assert isinstance(update_view(httprequest), Response)


# def test_html_content_in_response(httprequest):
#     """Test the html content."""
#     from pyramid_learning_journal.views.default import list_view
#     file_content = io.open(os.path.join(HERE, 'templates/index.html')).read()
#     response = list_view(httprequest)
#     assert file_content == response.textd


# def check_if_ok_status_with_request(httprequest):
#     """Check if 200 status on request."""
#     from pyramid_learning_journal.views.default import list_view
#     response = list_view(httprequest)
#     assert response.status_code == 200

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
    # import pdb; pdb.set_trace()
    assert 'Journal' in str(html.find('h1').text)
    assert 'Journal' in str(html.find('title').text)

#
# def test_home_route_listing_has_all_journals(testapp):
#     """Test the home route listing has all journals."""
#     response = testapp.get('/')
#     html = response.html
#     assert len(JOURNALS) == len(html.find_all('li'))
#
#
# def test_detail_route_with_bad_id(testapp):
#     """Test the detail route with a bad ID."""
#     response = testapp.get('/journal/400', status=404)
#     assert "Alchemy scaffold" in response.text
