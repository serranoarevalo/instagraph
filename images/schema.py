import graphene
from graphene_django.types import DjangoObjectType
from . import models, types


class ImageResponse(graphene.ObjectType):
    ok = graphene.Boolean(required=True)
    image = graphene.Field(types.ImageType)
    error = graphene.String()


class Query(object):

    images = graphene.List(types.ImageType, required=True)
    image = graphene.Field(ImageResponse, id=graphene.Int(required=True))

    def resolve_images(self, info, **kwargs):
        return models.Image.objects.all()

    def resolve_image(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            try:
                image = models.Image.objects.get(id=id)
                return ImageResponse(ok=True, image=image)
            except models.Image.DoesNotExist:
                return ImageResponse(ok=False, error='Image Not Found')
        return ImageResponse(ok=False, error='ID is mandatory')
