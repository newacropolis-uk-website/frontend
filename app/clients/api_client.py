from datetime import datetime

from app.clients import BaseAPIClient


class ApiClient(BaseAPIClient):
    def init_app(self, app):
        super(ApiClient, self).init_app(app)

    def get_speakers(self):
        return self.get(url='speakers')

    def get_venues(self):
        return self.get(url='venues')

    def get_venue_by_id(self, venue_id):
        return self.get(url='venue/{}'.format(venue_id))

    def add_event(self, event):
        return self.post(url='event', data=event)

    def delete_event(self, event_id):
        return self.delete(url='event/{}'.format(event_id))

    def update_event(self, event_id, event):
        return self.post(url='event/{}'.format(event_id), data=event)

    def get_event_types(self):
        return self.get(url='event_types')

    def get_limited_events(self):
        return self.get_nice_event_dates(self.get(url='events/limit/30'))

    def get_events_in_future(self):
        events = self.get_nice_event_dates(self.get(url='events/future'))
        return self._get_events_intro_courses_prioritised(events)

    def get_events_past_year(self):
        return self.get(url='events/past_year')

    def get_articles_summary(self):
        return self.get(url='articles/summary')

    def get_article(self, id):
        return self.get(url='article/{}'.format(id))

    def get_nice_event_dates(self, events):
        for event in events:
            dates = []
            for event_date in event['event_dates']:
                _datetime = datetime.strptime(event_date["event_datetime"], '%Y-%m-%d %H:%M')
                if _datetime.minute > 0:
                    time = _datetime.strftime('%-I:%M %p')
                else:
                    time = _datetime.strftime('%-I %p')
                if event['event_type'] == 'Introductory Course':
                    event['event_monthyear'] = _datetime.strftime('%B %Y')
                event_date['event_date'] = _datetime.strftime('%Y-%m-%d')
                dates.append(_datetime.strftime('%Y-%m-%d'))
                event_date['event_time'] = _datetime.strftime('%H:%M')
                if not event.get('event_time'):
                    event['event_time'] = _datetime.strftime('%H:%M')
                if not event.get('end_time'):
                    event['end_time'] = event_date.get("end_time")
                event_date['formatted_event_datetime'] = _datetime.strftime('%a %-d %B at {}'.format(time))
            event['dates'] = dates
        return events

    def _get_events_intro_courses_prioritised(self, events):
        intro_courses_first = []
        other_events = []
        for event in events:
            if event['event_type'] == 'Introductory Course':
                intro_courses_first.append(event)
            else:
                other_events.append(event)

        intro_courses_first.extend(other_events)
        return intro_courses_first

    def get_user(self, email):
        return self.get(url='user/{}'.format(email))

    def get_users(self):
        return self.get(url='users')

    def create_user(self, profile):
        data = {
            'email': profile['email'],
            'name': profile['name'],
        }
        return self.post(url='user', data=data)

    def update_user_access_area(self, user_id, access_area):
        data = {
            'access_area': access_area
        }
        return self.post(url='user/{}'.format(user_id), data=data)
