"""
Overview
--------

Initialization of all views contained in this project.
"""
def includeme(config):
    """
    Contains the routing information for all HTTP requests to this project.
    """
    add_route = config.add_route

    add_route('survey_create', '/surveys/create')

    config.scan('.')
