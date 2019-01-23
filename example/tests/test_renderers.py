import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_multiple_author(book_with_multi_author, client):

    expected = {
            'method': 'list',
            'params': {},
            'data': {
                'items': [
                    {
                        'title': book_with_multi_author.title,
                        'authors': [
                            {
                                'name': author.name
                            } for author in book_with_multi_author.authors.all()
                        ],
                        'comments': [
                            {
                                'author': {
                                    'name': comment.author.name
                                },
                                'body': comment.body,
                            } for comment in book_with_multi_author.comments.all()
                        ]
                    }
                ]
            }
        }

    response = client.get(reverse("book-list"))

    assert expected == response.json()


def test_author_with_meta(multi_author, client):

    expected = {
            'method': 'list',
            'params': {},
            'data': {
                'num_author': len(multi_author),
                'items': [
                    {
                        'name': author.name,
                    } for author in multi_author
                ]
            }
        }

    response = client.get(reverse("author-list"))

    assert expected == response.json()
