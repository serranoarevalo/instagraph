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
        if user.is_authenticated:
            if id is not None:
                try:
                    image = models.Image.objects.get(id=id)
                    try:
                        like = models.Like.objects.get(
                            creator=user, image=image)
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
        ok = False
        error = 'You need to log in'
        return LikeImage(ok=ok, error=error)


class CreateComment(graphene.Mutation):

    """ Create a Comment """

    class Arguments:
        message = graphene.String(required=True)
        imageId = graphene.Int(required=True)

    ok = graphene.Boolean(required=True)
    comment = graphene.Field(types.CommentType)
    error = graphene.String()

    def mutate(self, info, **kwargs):
        message = kwargs.get('message')
        imageId = kwargs.get('imageId')
        user = info.context.user
        if user.is_authenticated:
            if message is not None and imageId is not None:
                try:
                    image = models.Image.objects.get(id=imageId)
                    comment = models.Comment.objects.create(
                        message=message, image=image, creator=user)
                    comment.save()
                    ok = True
                    return CreateComment(ok=ok, comment=comment)
                except models.Image.DoesNotExist:
                    ok = False
                    error = 'Image not found'
                    return CreateComment(ok=ok, error=error)
            ok = False
            error = 'Message and ImageID are mandatory'
            return CreateComment(ok=ok, error=error)
        ok = False
        error = 'You need to log in'
        return CreateComment(ok=ok, error=error)


class DeleteImage(graphene.Mutation):

    """ Delete Image """

    class Arguments:
        imageId = graphene.Int(required=True)

    ok = graphene.Boolean(required=True)
    error = graphene.String()

    def mutate(self, info, **kwargs):
        user = info.context.user
        imageId = kwargs.get('imageId')

        if user.is_authenticated:
            try:
                image = models.Image.objects.get(id=imageId, creator=user)
                image.delete()
                ok = True
                return DeleteImage(ok=ok)
            except models.Image.DoesNotExist:
                ok = False
                error = 'Image not found'
                return DeleteImage(ok=ok, error=error)
        else:
            ok = False
            error = "You need to log in"
            return DeleteImage(ok=ok, error=error)
