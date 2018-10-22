import graphene
from graphene_django.types import DjangoObjectType
from . import models, mutations, types


class Query(object):

    all_users = graphene.List(types.UserType)

    def resolve_all_users(self, info, **kwargs):
        return models.User.objects.all()


class Mutation(object):

    create_user = mutations.CreateUser.Field()
