from .default import list_view, detail_view, create_view, update_view


def includeme(config):
    """List the views to include for configurator object."""
    config.add_view(list_view, route_name="home")
    config.add_view(detail_view, route_name="single")
    config.add_view(create_view, route_name="new")
    config.add_view(update_view, route_name="edit")
