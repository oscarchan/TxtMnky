from pyramid.config import Configurator
from pyramid_jinja2 import renderer_factory


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    from pyramid.session import UnencryptedCookieSessionFactoryConfig
    unsafe_session_factory = UnencryptedCookieSessionFactoryConfig('itsaseekreet')

    config = Configurator(settings=settings, session_factory= unsafe_session_factory)
    config.add_renderer('.jinja2', renderer_factory)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.include('.views')
    config.scan()
    return config.make_wsgi_app()
