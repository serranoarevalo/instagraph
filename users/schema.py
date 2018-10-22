import graphene
from graphene_django.types import DjangoObjectType
from . import models, mutations, types


class UserResponse(graphene.ObjectType):
    ok = graphene.Boolean(required=True)
    user = graphene.Field(types.UserType)
    error = graphene.String()


class Query(object):

    users = graphene.List(types.UserType, required=True)
    user = graphene.Field(
        UserResponse, username=graphene.String(required=True))

    def resolve_users(self, info, **kwargs):
        return models.User.objects.all()

    def resolve_user(self, info, **kwargs):
        username = kwargs.get('username')
        if username is not None:
            try:
                user = models.User.objects.get(username=username)
                return UserResponse(ok=True, user=user)
            except models.User.DoesNotExist:
                return UserResponse(ok=False, error='User not found')

        return UserResponse(ok=False, error='Username is mandatory')


class Mutation(object):
    create_user = mutations.CreateUser.Field(required=True)
