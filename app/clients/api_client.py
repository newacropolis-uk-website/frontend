from datetime import datetime

from app.clients import BaseAPIClient


class ApiClient(BaseAPIClient):
    def init_app(self, app):
        super(ApiClient, self).init_app(app)

    def get_speakers(self):
        return self.get(url='speakers')

    def get_venues(self):
        return self.get(url='venues')

    def get_events_in_future(self):
        return self.get_nice_event_dates(self.get(url='events/future'))

    def get_events_past_year(self):
        return self.get(url='events/past_year')

    def get_articles_summary(self):
        return self.get(url='articles/summary')

    def get_article(self, id):
        return self.get(url='article/{}'.format(id))

    def get_nice_event_dates(self, events):
        for event in events:
            for event_date in event['event_dates']:
                _datetime = datetime.strptime(event_date["event_datetime"], '%Y-%m-%d %H:%M')
                if _datetime.minute > 0:
                    time = _datetime.strftime('%-I:%M %p')
                else:
                    time = _datetime.strftime('%-I %p')
                event_date['event_datetime'] = _datetime.strftime('%a %-d %B at {}'.format(time))

        return events
