import graphene
from graphene_django.types import DjangoObjectType
import graphql_jwt
from graphql_jwt.decorators import login_required
from . import models, mutations, types


class UserResponse(graphene.ObjectType):

    """ User Query Response """

    ok = graphene.Boolean(required=True)
    user = graphene.Field(types.UserType)
    error = graphene.String()


class Query(object):

    """ User Queries """

    users = graphene.List(types.UserType, required=True)
    user = graphene.Field(
        UserResponse, username=graphene.String(required=True))
    me = graphene.Field(types.UserType)

    def resolve_users(self, info, **kwargs):
        return models.User.objects.all()

    def resolve_user(self, info, **kwargs):
        username = kwargs.get('username')
        if username is not None:
            try:
                user = models.User.objects.get(username=username)
                ok = True
                return UserResponse(ok=ok, user=user)
            except models.User.DoesNotExist:
                ok = False
                error = 'User Not Found'
                return UserResponse(ok=ok, error=error)
        ok = False
        error = 'Username is mandatory'
        return UserResponse(ok=ok, error=error)

    @login_required
    def resolve_me(self, info, **kwargs):
        return info.context.user


class Mutation(object):
    create_user = mutations.CreateUser.Field(required=True)
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
