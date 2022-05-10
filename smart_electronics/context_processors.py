"""
Adds a custom context processor which will add profile related to the user
in the context dictionary. It is done to aviod overriding context in each view.
"""


def add_user_profile(request):
    """Adds User profile to the context if user is Signed In.

    Args:
        request: wsgi request object

    Returns:
        dict: context dictionary
    """
    return {
        "user_profile": request.user.profile if request.user.is_authenticated else None,
    }
