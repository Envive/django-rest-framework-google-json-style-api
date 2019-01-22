from django.db import models # noqa


class BaseModel(models.Model):
    """
    I hear RoR has this by default, who doesn't need these two fields!
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AuthorType(BaseModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)


class Author(BaseModel):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    author_type = models.ForeignKey(AuthorType, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)


class AuthorBio(BaseModel):
    author = models.OneToOneField(Author, related_name='bio', on_delete=models.CASCADE)
    body = models.TextField()

    def __str__(self):
        return self.author.name

    class Meta:
        ordering = ('id',)


class Book(BaseModel):
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField(Author, related_name='books')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('id',)


class Comment(BaseModel):
    book = models.ForeignKey(Book, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()
    author = models.ForeignKey(
        Author,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='comments',
    )

    def __str__(self):
        return self.body

    class Meta:
        ordering = ('id',)
