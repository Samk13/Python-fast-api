from app import schemas


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get('/posts/')

    def validate(post):
        return schemas.PostResponseVotes(**post)
    posts_map = map(validate, res.json())
    posts_list = list(posts_map)
    assert res.status_code == 200
    assert len(res.json()) == 3
    assert posts_list[0].Post.title == 'Test title 2'
    assert posts_list[1].Post.title == 'Test title 3'
    assert posts_list[2].Post.id == 1

# cause there is no authorization in get all posts should be 200


def test_unauthorized_get_all_posts(client):
    res = client.get('/posts/')
    assert res.status_code == 200


def test_unauthorized_get_one_post(client, test_posts):
    print(vars(test_posts[0]))
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_one_post_not_exists(authorized_client, test_posts):
    res = authorized_client.get('/posts/100')
    assert res.status_code == 404
