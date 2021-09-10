import pytest
import server

@pytest.fixture()
def clients():
    server.app.config['TESTING'] = True
    clients = server.app.test_client()
    return clients

class TestServer:
    def setup_method(self):
        self.club = [{
            "name": "test test",
            "email": "test@test.fr",
            "points": "13"},
            {
            "name": "test1 test1",
            "email": "test@test1.fr",
            "points": "13"},
        ]

        self.competitions = [{
            "name": "Festival Test",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25"}]

        self.bad_email = "bad_email@bademail.fr"
        self.good_email = "test@test.fr"
        self.session = {'email': "test@test.fr"}

        server.competitions = self.competitions
        server.clubs = self.club

    def test_bad_login(self, clients):
        login = clients.post("/", data={'email': str(self.bad_email)})
        assert b"Bad email or password" in login.data

    def test_good_login(self, clients):
        login = clients.post("/", data={'email': str(self.good_email)})
        assert b"test@test.fr" in login.data

    def test_display_points(self, clients):
        request = clients.get("/display")
        assert b"test" in request.data
        assert b"13" in request.data

    def test_display_competitions(self, clients):
        request = clients.post("/", data=self.session)
        assert b"Festival Test" in request.data

    def test_access_booking_with_session(self, clients):
        server.session = self.session
        request = clients.get('/book/Festival%20Test/test%20test')
        assert b'Festival Test' in request.data
        assert b'25' in request.data

    def test_access_booking_without_session(self, clients):
        server.session.clear()
        request = clients.get('/book/Festival%20Test/test%20test')
        assert b'Not connected' in request.data

    def test_access_booking_with_session_bad_competition(self, clients):
        server.session = self.session
        request = clients.get('/book/Festival%20Test2021/test%20test')
        assert b'Club or competition not found!' in request.data

    def test_access_booking_with_session_bad_club(self, clients):
        request = clients.get('/book/Festival%20Test/test%20test2021')
        assert b'Club or competition not found' in request.data

    def test_book_place(self, clients):
        data = {
            "competition": "Festival Test",
            "club": "test test",
            "places": 2,
        }
        request = clients.post('/purchasePlaces', data=data)
        assert b"Great-booking complete!" in request.data


    def test_book_place_13(self, clients):
        data = {
            "competition": "Festival Test",
            "club": "test test",
            "places": 13,
        }
        request = clients.post('/purchasePlaces', data=data)
        assert b"You can t book" in request.data

    def test_book_with_not_enough_points(self, clients):
        server.clubs[0]['points'] = '2'
        data = {
            "competition": "Festival Test",
            "club": "test test",
            "places": 10,
        }
        request = clients.post('/purchasePlaces', data=data)
        assert b"You can t book" in request.data

    def test_book_with_not_enough_places(self, clients):
        server.clubs[0]['points'] = '13'
        server.competitions[0]['numberOfPlaces'] = '4'
        print(server.competitions)
        data = {
            "competition": "Festival Test",
            "club": "test test",
            "places": 6,
        }
        request = clients.post('/purchasePlaces', data=data)
        assert b"You can t book" in request.data

    def test_book_with_not_enough_competition(self, clients):
        data = {
            "competition": "Festival63 Test",
            "club": "test test",
            "places": 6,
        }
        request = clients.post('/purchasePlaces', data=data)
        assert b"Club or competition not found" in request.data

    def test_book_with_error_in_club(self, clients):
        server.session.clear()
        server.session = {'email': "test@test1.fr"}
        data = {
            "competition": "Festival Test",
            "club": "test test",
            "places": 1,
        }
        request = clients.post('/purchasePlaces', data=data)
        assert b"You try to book for another club" in request.data


    def test_book_with_not_session(self, clients):
        server.session.clear()
        print(server.competitions)
        data = {
            "competition": "Festival Test",
            "club": "test test",
            "places": 1,
        }
        request = clients.post('/purchasePlaces', data=data)
        assert b"Not connected" in request.data


    def test_logout(self, clients):
        server.session = self.session
        request = clients.get('/logout',)
        assert len(server.session) == 0


