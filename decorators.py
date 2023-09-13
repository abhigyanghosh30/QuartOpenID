# Core packages
import functools

# Third party packages
import quart
from login import user_info


def login_required(func):
    """
    Decorator that checks if a user is logged in, and redirects
    to login page if not.
    """

    @functools.wraps(func)
    async def is_user_logged_in(*args, **kwargs):
        if not user_info(quart.session):
            return quart.redirect("/login?next=" + quart.request.path)

        return await func(*args, **kwargs)

    return is_user_logged_in
