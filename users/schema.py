import graphene
from graphene_django.types import DjangoObjectType
from . import models


class UserType(DjangoObjectType):

    class Meta:
        model = models.User


class Query(object):

    all_users = graphene.List(UserType)

    def resolve_all_users(self, info, **kwargs):
        return models.User.objects.all()
