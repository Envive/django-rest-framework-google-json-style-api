import pytest
from pytest_factoryboy import register

from example.factories import (
    AuthorTypeFactory,
    AuthorBioFactory,
    AuthorFactory,
    BookFactory,
    CommentFactory
)

register(BookFactory)
register(AuthorFactory)
register(AuthorBioFactory)
register(AuthorTypeFactory)
register(CommentFactory)


@pytest.fixture
def book_with_single_author(author_factory, book_factory, comment_factory):
    author = author_factory()
    book = book_factory(authors=(author,))
    comment_factory(book=book)
    return book


@pytest.fixture
def book_with_multi_author(author_factory, book_factory, comment_factory):
    authors = [
        author_factory(),
        author_factory(),
    ]
    book = book_factory(authors=authors)
    comment_factory(book=book)
    return book


@pytest.fixture
def multi_author(author_factory, book_factory, comment_factory):
    authors = [
        author_factory(),
        author_factory(),
    ]

    book_factory(authors=authors),
    book_factory(authors=(authors[0],)),
    book_factory(authors=(authors[1],)),

    return authors
