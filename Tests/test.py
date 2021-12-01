from flask import session, config, json
from app import app
from unittest import TestCase
from models import connect_db, db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

connect_db(app)
db.drop_all
db.create_all


class BloglyTests(TestCase):

    def setUp(self):
        """To do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        User.query.delete()

        user = User(
            first_name='Max',
            last_name='Val',
            image_url=''
        )

        db.session.add(user)
        db.session.commit()

    def tearDown(self):

        db.session.rollback()

    def test_home(self):
        """Make sure the instruction page displays properly"""

        with self.client:
            res = self.client.get('/')
            self.assertEquals(res.status, "302 FOUND")

    def test_users_list(self):
        """Make sure the list shows properly"""

        with self.client:
            res = self.client.get('/users')
            self.assertIn(b'Max Val', res.data)

    def test_new_user(self):
        """Test the creation of a new user"""

        #  Test POST
        tester = app.test_client(self)
        res = tester.post('/users/new', data=dict(first_name="Nerea",
                                                  last_name="AC", image_url=""), follow_redirects=True)
        self.assertIn(b'Nerea AC', res.data)
        self.assertEquals(res.status, "200 OK")

        user = User.query.filter(User.first_name == 'Nerea')

        self.assertEquals(user.one().first_name, 'Nerea')
        self.assertEquals(user.one().last_name, 'AC')

        # Test GET
        with self.client:
            res = self.client.get('/users/new')
            self.assertEquals(res.status, "200 OK")

    def test_delete_user(self):
        """Test the deletion of a user"""

        user1 = User.query.filter(User.first_name == 'Max')
        user_id = user1.one().id

        tester = app.test_client(self)
        res = tester.post(f'/users/{user_id}/delete')
        user = User.query.all()

        self.assertNotIn(user, user1)
