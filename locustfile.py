from locust import HttpUser, task, between


class QuickstartUser(HttpUser):

    def on_start(self):
        with self.client.post("/", data={"email": "john@simplylift.co"}) as response:
            if "john@simplylift.co" not in response.text:
                response.failure("Bad request")

    def on_stop(self):
        self.client.get("/logout")

    @task
    def display_competition(self):
        with self.client.get("/") as response:
            if "Competitions:" not in response.text:
                response.failure("Bad request")
            elif response.elapsed.total_seconds() > 5:
                response.failure("Processing times exceeded")

    @task
    def book_places(self):
        with self.client.post("/purchasePlaces",
                              data={"places": 1, "club": "Simply Lift", "competition": "Fall Classic"}) as response:
            if response.elapsed.total_seconds() > 5:
                response.failure("Processing times exceeded")

    @task
    def display_points(self):
        with self.client.get("/display") as response:
            if "points" not in response.text:
                response.failure("Bad request")
            elif response.elapsed.total_seconds() > 5:
                response.failure("Processing times exceeded")



