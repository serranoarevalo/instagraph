import graphene
from graphene_django.types import DjangoObjectType
from . import models, types


class Query(object):

    images = graphene.List(types.ImageType, required=True)

    def resolve_images(self, info, **kwargs):
        return models.Image.objects.all()
