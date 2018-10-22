import graphene
from graphene_django.types import DjangoObjectType
from . import models, types, mutations


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
                ok = True
                return ImageResponse(ok=ok, image=image)
            except models.Image.DoesNotExist:
                ok = False
                error = 'Image Not Found'
                return ImageResponse(ok=ok, error=error)
        ok = False
        error = 'ID is mandatory'
        return ImageResponse(ok=ok, error=error)


class Mutation(object):
    create_image = mutations.CreateImage.Field(required=True)
    like_image = mutations.LikeImage.Field(required=True)
