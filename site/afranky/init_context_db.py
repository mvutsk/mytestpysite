from werkzeug.security import generate_password_hash
from common.acc_models import User, Friend
from common.post_models import Post, Comment


def main():
    try:
        user1 = User(usernam='user1', name="I'm without imagination", email='user1@example.com', visit_count=4)
        user1.pw_hash = generate_password_hash('user1pass', method='pbkdf2:sha1')
        user1.save()
        user2 = User(usernam='user2', name='Crazy user', email='user2@example.com', visit_count=7)
        user2.pw_hash = generate_password_hash('user2pass', method='pbkdf2:sha1')
        user2.save()
        user3 = User(usernam='user3', name='я есть Грут!', email='user3@example.com', visit_count=1)
        user3.pw_hash = generate_password_hash('user3pass', method='pbkdf2:sha1')
        user3.save()

        post1 = Post(title="First page here", body="Simple text, actually only simple text.", author=user1)
        post1.save()
        post2 = Post(title="Second article, no magic", body="Here should be funny story, but unfortunately I missed it.", author=user2)
        post2.save()
        post3 = Post(title="Don't open, nothing here", body="Here it is - nothing.", author=user2)
        post3.save()

        u1u2 = Friend(friend_user_id=user2.id, status='friend')
        user1.friends.append(u1u2)
        user1.save()
        u2u1 = Friend(friend_user_id=user1.id, status='friend')
        user2.friends.append(u2u1)
        user2.save()
        u1u3 = Friend(friend_user_id=user3.id, status='requested')
        user1.friends.append(u1u3)
        user1.save()
        u3u1 = Friend(friend_user_id=user1.id, status='initiator')
        user3.friends.append(u3u1)
        user3.save()
        u3u2 = Friend(friend_user_id=user2.id, status='friend')
        user3.friends.append(u3u2)
        user3.save()
        u2u3 = Friend(friend_user_id=user3.id, status='friend')
        user2.friends.append(u2u3)
        user2.save()

        post1.comments.append(Comment(body="I'm first!", author=user2))
        post1.save()
        post2.comments.append(Comment(body="I know how to do magic here!", author=user2))
        post2.save()
        post2.comments.append(Comment(body="я есть Грут! я есть Грут!", author=user3))
        post2.save()
        post3.comments.append(Comment(body="Don't post anything else please...", author=user1))
        post3.save()

    except:
        print("Something went wrong. Is db started?")

if __name__ == '__main__':
    main()
