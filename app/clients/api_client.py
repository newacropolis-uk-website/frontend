from app.clients import BaseAPIClient


class ApiClient(BaseAPIClient):
    def init_app(self, app):
        super(ApiClient, self).init_app(app)

    def get_speakers(self):
        return self.get(url='speakers')

    def get_venues(self):
        return self.get(url='venues')

    def get_events_past_year(self):
        return self.get(url='events/past_year')
