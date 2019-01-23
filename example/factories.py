import factory
from faker import Factory as FakerFactory

from example.models import (
    AuthorType,
    Author,
    AuthorBio,
    Book,
    Comment
)

faker = FakerFactory.create()
faker.seed(2019)


class AuthorTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AuthorType

    name = factory.LazyAttribute(lambda x: faker.name())


class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author

    name = factory.LazyAttribute(lambda x: faker.name())
    email = factory.LazyAttribute(lambda x: faker.email())
    bio = factory.RelatedFactory('example.factories.AuthorBioFactory', 'author')
    author_type = factory.SubFactory(AuthorTypeFactory)


class AuthorBioFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AuthorBio

    author = factory.SubFactory(AuthorFactory)
    body = factory.LazyAttribute(lambda x: faker.text())


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    title = factory.LazyAttribute(lambda x: faker.sentence(nb_words=4))

    @factory.post_generation
    def authors(self, create, extracted, **kwargs):
        if extracted:
            if isinstance(extracted, (list, tuple)):
                for author in extracted:
                    self.authors.add(author)
            else:
                self.authors.add(extracted)


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    book = factory.SubFactory(BookFactory)
    body = factory.LazyAttribute(lambda x: faker.text())
    author = factory.SubFactory(AuthorFactory)
