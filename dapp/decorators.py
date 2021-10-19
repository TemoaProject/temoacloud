from django.core.exceptions import PermissionDenied
from django.core.files.uploadedfile import InMemoryUploadedFile


def user_is_staff(function):
    def wrap(request, *args, **kwargs):

        # print("type", request, type(request) )
        if type(request) == InMemoryUploadedFile or request.user.is_staff:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    wrap.__dict__ = function.__dict__
    return wrap


# Super user owns all restaurants
def is_superuser(user):
    return user.is_superuser


# Manager and Admin must belong to staff
def is_staff(user):
    return user.is_staff


# Can be manager or admin
def is_manager_or_admin(user):

    if is_admin(user):
        return True

    if is_manager(user):
        return True

    return False


# Manager can check orders on restaurant (single location)
def is_manager(user):
    return user.groups.filter(name='Manager').exists()


# Staff owns single restaurant with full control on single location
def is_admin(user):
    return user.groups.filter(name='Admin').exists()


# Get all approved store list
def allowed_stores(request):

    user = request.user.profile
    owner = request.user.profile.owner()

    return request.user.profile.stores.all()
