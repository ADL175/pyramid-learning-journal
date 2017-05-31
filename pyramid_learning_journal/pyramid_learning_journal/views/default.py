from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound


JOURNAL_ENTRIES = [
    {'id': 0, 'title': 'Journal Entry 1', 'date': 'March 13th 2017', 'body': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'},
    {'id': 1, 'title': 'Journal Entry 1', 'date': 'March 14th 2017', 'body': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'},
    {'id': 2, 'title': 'Journal Entry 1', 'date': 'April 1st 2017', 'body': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'},
    {'id': 3, 'title': 'Journal Entry 1', 'date': 'May 5th 2017', 'body': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'},
    {'id': 4, 'title': 'Journal Entry 1', 'date': 'May 19th 2017', 'body': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'},
    {'id': 5, 'title': 'Journal Entry 1', 'date': 'May 30th 2017', 'body': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'},
]


@view_config(route_name='home', renderer='../templates/index.jinja2')
def home_view(request):
    """View for the home route."""
    return {
        'page': 'Home',
        'journal': JOURNAL_ENTRIES
    }


@view_config(route_name='detail', renderer='../templates/individual-etry.jinja2')
def detail_view(request):
    """View for the detail route."""
    the_id = int(request.matchdict['id'])
    try:
        entry = JOURNAL_ENTRIES[the_id]
    except IndexError:
        raise HTTPNotFound

    return {
        'page': 'Journal Entry',
        'entry': entry
    }
# from pyramid.response import Response
# import io
# import os
#
# HERE = os.path.dirname(__file__)
#
#
# def list_view(request):
#     """List of journal entries."""
#     with io.open(os.path.join(HERE, '../templates/index.html')) as the_file:
#         imported_text = the_file.read()
#
#     return Response(imported_text)
#
#
# def detail_view(request):
#     """Single journal entry."""
#     with io.open(os.path.join(HERE, '../templates/post.html')) as the_file:
#         imported_text = the_file.read()
#
#     return Response(imported_text)
#
#
# def create_view(request):
#     """Create a new view."""
#     with io.open(os.path.join(HERE, '../templates/create.html')) as the_file:
#         imported_text = the_file.read()
#
#     return Response(imported_text)
#
#
# def update_view(request):
#     """Update existing view."""
#     with io.open(os.path.join(HERE, '../templates/edit.html')) as the_file:
#         imported_text = the_file.read()
#
#     return Response(imported_text)
