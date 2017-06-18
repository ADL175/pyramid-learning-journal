
from pyramid.view import view_config
from pyramid.httpexceptions import (
    HTTPNotFound,
    HTTPFound
    )
from pyramid.security import remember, forget
from pyramid.session import check_csrf_token
from pyramid_learning_journal.models import Journal
from pyramid_learning_journal.security import check_credentials
import datetime


@view_config(route_name='home', renderer='../templates/index.jinja2')
def home_view(request):
    """View for the home route."""
    session = request.dbsession
    all_journals = session.query(Journal).all()
    return {
        'page': 'Home',
        'journals': all_journals
    }


@view_config(route_name='detail', renderer="../templates/post.jinja2")
def detail_view(request):
    """View for the journal route."""
    the_id = int(request.matchdict['id'])
    session = request.dbsession
    journal = session.query(Journal).get(the_id)
    if not journal:
        raise HTTPNotFound

    return {
        'page': 'Journal Entry',
        'journal': journal
    }


@view_config(
    route_name='create', renderer='../templates/new-journal.jinja2',
    permission='secret'
    )
def create_view(request):
    """Authenticates user to view to create a new journal entry."""
    if request.method == "POST" and request.POST:
        # check_csrf_token(request)
        if not request.POST['title'] or not request.POST['body']:
            return {
                'title': request.POST['title'],
                'body': request.POST['body'],
                'error': "Bro, you need to add stuff!"
            }
        new_journal = Journal(
            title=request.POST['title'],
            body=request.POST['body']
        )
        request.dbsession.add(new_journal)
        return HTTPFound(
            location=request.route_url('home')
        )
    return {}


@view_config(
    route_name='update',
    renderer='../templates/edit-journal.jinja2',
    permission='secret'
    )
def update_view(request):
    """Authenticates user and allows update journal entry."""
    the_id = int(request.matchdict['id'])
    session = request.dbsession
    journal = session.query(Journal).get(the_id)
    if not journal:
        raise HTTPNotFound
    if request.method == 'GET':
        return {
            'page': 'Edit Page',
            'title': journal.title,
            'body': journal.body
        }
    if request.method == 'POST':
        # check_csrf_token(request)
        journal.title = request.POST['title']
        journal.body = request.POST['body']
        request.dbsession.flush()
        return HTTPFound(request.route_url('detail', id=journal.id))


@view_config(
    route_name='login',
    renderer='../templates/login.jinja2',
    require_csrf=False
    )
def login(request):
    """View for user login."""

    if request.method == 'GET':
        return {}
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        if check_credentials(username, password):
            headers = remember(request, username)
            return HTTPFound(
                location=request.route_url('home'),
                headers=headers
            )
        return {'error': 'Bad username or password'}


@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(request.route_url('home'), headers=headers)
