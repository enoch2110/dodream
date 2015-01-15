from django.contrib.auth.models import User
from django.core.urlresolvers import RegexURLPattern, RegexURLResolver


class DecoratedURLPattern(RegexURLPattern):
    def resolve(self, *args, **kwargs):
        result = super(DecoratedURLPattern, self).resolve(*args, **kwargs)
        if result:
            result.func = self._decorate_with(result.func)
        return result


class DecoratedRegexURLResolver(RegexURLResolver):
    def resolve(self, *args, **kwargs):
        result = super(DecoratedRegexURLResolver, self).resolve(*args, **kwargs)
        if result:
            result.func = self._decorate_with(result.func)
        return result


def decorated_includes(func, includes, *args, **kwargs):
    """
    How to use:

    (r'', decorated_includes(
        user_passes_test(lambda u: u.is_authenticated() and u.profile.is_business() or u.is_superuser, login_url='/cnuadmin/signin'),
        include(cnuadmin_urls))
    ),
    """
    urlconf_module, app_name, namespace = includes

    for item in urlconf_module:
        if isinstance(item, RegexURLPattern):
            item.__class__ = DecoratedURLPattern
            item._decorate_with = func

        elif isinstance(item, RegexURLResolver):
            item.__class__ = DecoratedRegexURLResolver
            item._decorate_with = func

    return urlconf_module, app_name, namespace