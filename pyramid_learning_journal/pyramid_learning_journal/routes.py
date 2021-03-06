def includeme(config):
    config.add_static_view('static', 'pyramid_learning_journal:static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('detail', '/journal/{id:\d+}')
    config.add_route('create', '/journal/new-journal')
    config.add_route('update', '/journal/{id:\d+}/edit')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('test', '/test')
