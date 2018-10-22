import graphene
from django.db import IntegrityError
from . import types, models


class CreateUser(graphene.Mutation):

    """ Create an User """

    class Arguments:
        bio = graphene.String()
        website = graphene.String()
        username = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)

    ok = graphene.Boolean(required=True)
    user = graphene.Field(types.UserType)
    error = graphene.String()

    def mutate(self, info, **kwargs):
        try:
            user = models.User.objects.create(**kwargs)
            user.save()
            ok = True
            user = user
            return CreateUser(ok=ok, user=user)
        except IntegrityError:
            ok = False
            error = "Username is duplicated"
            return CreateUser(ok=False, error=error)
