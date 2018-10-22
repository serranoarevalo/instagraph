import graphene
from django.db import IntegrityError
from graphene_file_upload.scalars import Upload
from . import types, models


class CreateImage(graphene.Mutation):

    """ Create an Image """

    class Arguments:
        file = Upload()
        location = graphene.String()
        caption = graphene.String(required=True)

    ok = graphene.Boolean(required=True)
    image = graphene.Field(types.ImageType)
    error = graphene.String()

    def mutate(self, info, file, **kwargs):

        user = info.context.user

        if user.is_authenticated:
            image = models.Image.objects.create(**kwargs, creator=user)
            image.save()
            ok = True
            return CreateImage(ok=ok, image=image)
        else:
            ok = False
            error = 'You need to log in first'
            return CreateImage(ok=ok, error=error)
