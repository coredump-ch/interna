from django.test import Client


def test_members_view(client: Client):
    response = client.get('/robots.txt')  # type: HttpResponse
    assert response.status_code == 200
    assert 'User-agent: *\nDisallow: /' in response.content.decode('utf8')
