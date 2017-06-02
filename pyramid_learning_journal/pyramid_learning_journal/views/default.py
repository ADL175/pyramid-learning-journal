
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound

JOURNALS = [
    {'id': 0, 'title': 'May 30 Entry', 'date': 'May 30, 2017', 'body': 'This weekend was rough, trying to get most of the work done on the server. The server was tough  and it was depressing not being able to get it up and running. Today we went over Pyramid, which was way easier than building our server, but there were still some growing pains with the assignment. Carlos and I partnered up and tried to problem solve it. Eventually, we were able to get it up and running. Trying to stay positive and practice deliberately.'},
    {'id': 1, 'title': 'May 31 Entry', 'date': 'May 31, 2017', 'body': 'Today we learned about templating via jinja2. We also learned about Binary Heap. Nick did a code review of my learning journal, which was very helpful for me. Carlos and I pair programmed on the learning journal and we were able to get the server to load properly. Today we also picked groups for our projects. Our project, TweetGrams was voted for and we have a pretty awesome team. Tonight, a couple of us are going to Avvo for a meetup tonight.'},
    {'id': 2, 'title': 'June 1 Entry', 'date': 'June 1, 2017', 'body': 'Today during class we reviewed BinHeap data strutures and code review of step 2 on the learning journal. For class, we learned about SQLAlchemy, models and postgres. During lab, Carlos and I got stuck on the learning journal assigment for step 3. Ely offered his help and he showed us how he uses PDB, which I had seen, but hadnt used. Afterwards, Nick helped us and it got to working, but we will have to implement a work around to deploy the DB to heroku. Today, after class, I went to a meetup at Axon, which was a great opportunity. I met some great Axon employees and learned a lot about their products. I also won a raffle prize!'},
    {'id': 3, 'title': 'Journal Entry 4', 'date': 'May 05, 2017', 'body': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'},
    {'id': 4, 'title': 'Journal Entry 5', 'date': 'May 09, 2017', 'body': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'},
    {'id': 5, 'title': 'Journal Entry 6', 'date': 'May 12, 2017', 'body': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'}
]


@view_config(route_name='home', renderer='../templates/index.jinja2')
def home_view(request):
    """View for the home route."""
    return {
        'page': 'Home',
        'journals': JOURNALS
    }


@view_config(route_name='detail', renderer="../templates/post.jinja2")
def detail_view(request):
    """View for the journal route."""
    the_id = int(request.matchdict['id'])

    journal = None
    for item in JOURNALS:
        if item['id'] == the_id:
            journal = item
            break

    # journal = list(filter(lambda item: item['id'] == the_id, JOURNALS))

    if not journal:
        raise HTTPNotFound

    return {
        'page': 'Journal Entry',
        'journal': journal
    }
