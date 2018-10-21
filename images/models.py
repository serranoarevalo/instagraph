from django.db import models
from users import models as user_models


class Image(user_models.DateModel):

    """ Image Model """

    file = models.FileField(upload_to='user_image')
    location = models.CharField(max_length=140)
    caption = models.TextField()
    creator = models.ForeignKey(
        user_models.User, related_name='images', on_delete=models.CASCADE)

    def __str__(self):
        return self.location


class Comment(user_models.DateModel):

    """ Comment Model """

    message = models.TextField()
    creator = models.ForeignKey(
        user_models.User, related_name='image_comments', on_delete=models.CASCADE)
    image = models.ForeignKey(
        Image, related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.message


class Like(user_models.DateModel):

    """ Like Model """

    creator = models.ForeignKey(
        user_models.User, related_name='image_likes', on_delete=models.CASCADE)
    image = models.ForeignKey(
        Image, related_name='likes', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.creator.username} {self.image.caption}'
