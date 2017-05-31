# def includeme(config):
#     config.add_static_view('static', 'static', cache_max_age=3600)
#     config.add_route('home', '/')
#     config.add_route('single', '/journal/{id:\d+}')
#     config.add_route('new', '/journal/new-entry')
#     config.add_route('edit', '/journal/{id:\d+}/edit-entry')

def incudeme(config):
    config.add_static_view('static', 'pyramid_learning_journal: static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('detail', '/journal/{id:\d+}')
