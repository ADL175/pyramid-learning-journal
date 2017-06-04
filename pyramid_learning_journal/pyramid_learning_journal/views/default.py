
from pyramid.view import view_config
from pyramid_learning_journal.models import Journal
from pyramid.httpexceptions import (HTTPNotFound, HTTPFound)
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


@view_config(route_name='create', renderer='../templates/new-journal.jinja2')
def create_view(request):
    """View to create a new journal entry."""
    if request.method == "POST" and request.POST:
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


@view_config(route_name='update', renderer='../templates/edit-journal.jinja2')
def update_view(request):
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
        journal.title = request.POST['title']
        journal.body = request.POST['body']
        request.dbsession.flush()
        return HTTPFound(request.route_url('detail', id=journal.id))
