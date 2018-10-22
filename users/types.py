import graphene
from graphene_django.types import DjangoObjectType
from . import models


class UserType(DjangoObjectType):

    full_name = graphene.String()

    class Meta:
        model = models.User
        exclude_fields = ('password',)

    def resolve_full_name(self, info):
        return f'{self.first_name} {self.last_name}'
