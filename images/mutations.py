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


class LikeImage(graphene.Mutation):

    """ Like an Image """

    class Arguments:
        imageId = graphene.Int(required=True)

    ok = graphene.Boolean(required=True)
    error = graphene.String()

    def mutate(self, info, **kwargs):
        id = kwargs.get('imageId')
        user = info.context.user
        if id is not None:

            try:
                image = models.Image.objects.get(id=id)
                try:
                    like = models.Like.objects.get(creator=user, image=image)
                    like.delete()
                except models.Like.DoesNotExist:
                    like = models.Like.objects.create(
                        creator=user, image=image)
                    like.save()
                ok = True
                return LikeImage(ok=ok)

            except models.Image.DoesNotExist:
                ok = False
                error = 'Image Not Found'
                return LikeImage(ok=ok, error=error)

        ok = False
        error = 'ID is mandatory'
        return LikeImage(ok=ok, error=error)
