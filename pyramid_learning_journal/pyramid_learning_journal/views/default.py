from pyramid.response import Response
import io
import os

HERE = os.path.dirname(__file__)


def list_view(request):
    """List of journal entries."""
    with io.open(os.path.join(HERE, '../templates/index.html')) as the_file:
        imported_text = the_file.read()

    return Response(imported_text)


def detail_view(request):
    """Single journal entry."""
    with io.open(os.path.join(HERE, '../templates/post.html')) as the_file:
        imported_text = the_file.read()

    return Response(imported_text)


def create_view(request):
    """Create a new view."""
    with io.open(os.path.join(HERE, '../templates/create.html')) as the_file:
        imported_text = the_file.read()

    return Response(imported_text)


def update_view(request):
    """Update existing view."""
    with io.open(os.path.join(HERE, '../templates/edit.html')) as the_file:
        imported_text = the_file.read()

    return Response(imported_text)
