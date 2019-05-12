from flask import session
from flask_wtf import FlaskForm
from wtforms import BooleanField, FormField, FieldList, FileField, HiddenField, SelectField, StringField, TextAreaField
from wtforms.validators import DataRequired


class UserForm(FlaskForm):

    str_email = StringField()
    user_id = HiddenField()
    admin = BooleanField('admin')
    event = BooleanField('event')
    email = BooleanField('email')
    magazine = BooleanField('magazine')
    report = BooleanField('report')
    shop = BooleanField('shop')
    announcement = BooleanField('announcement')
    article = BooleanField('article')


class UserListForm(FlaskForm):
    users = FieldList(FormField(UserForm), min_entries=0)

    def populate_user_form(self, users):
        if not self.users:
            for user in users:
                user_form = UserForm()
                user_form.user_id = user['id']
                user_form.str_email = user['email']

                user_form.admin = _has_access_area('admin', user['access_area'])
                user_form.event = _has_access_area('event', user['access_area'])
                user_form.email = _has_access_area('email', user['access_area'])
                user_form.magazine = _has_access_area('magazine', user['access_area'])
                user_form.report = _has_access_area('report', user['access_area'])
                user_form.shop = _has_access_area('shop', user['access_area'])
                user_form.announcement = _has_access_area('announcement', user['access_area'])
                user_form.article = _has_access_area('article', user['access_area'])

                self.users.append_entry(user_form)
        else:
            for user in self.users:
                found_user = [u for u in users if u['id'] == user.user_id.data]
                if found_user:
                    user.str_email.data = found_user[0]['email']


def _has_access_area(area, user_access_area):
    if user_access_area:
        return area in user_access_area.split(',')
    return False


class EventForm(FlaskForm):

    events = SelectField('Events')
    alt_event_images = SelectField('Event Images')
    event_type = SelectField('Event type', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    sub_title = StringField('Sub-title')
    description = TextAreaField('Description', validators=[DataRequired()])
    booking_code = StringField('Booking code')
    image_filename = FileField('Image filename')
    existing_image_filename = HiddenField('Existing image filename')
    fee = StringField('Fee')
    conc_fee = StringField('Concession fee')
    multi_day_fee = StringField('Multi day fee')
    multi_day_conc_fee = StringField('Multi day concession fee')
    venue = SelectField('Venue')
    event_dates = HiddenField()
    start_time = HiddenField()
    end_time = HiddenField()
    speakers = SelectField('Speakers')
    dates = HiddenField()
    default_event_type = HiddenField()


def set_events_form(events, event_types, speakers, venues):
    form = EventForm()
    if form.events:
        if form.image_filename.data:
            filename = form.image_filename.data.filename
        else:
            filename = form.existing_image_filename.data
        submitted_event = {
            'event_id': form.events.data,
            'event_type_id': form.event_type.data,
            'title': form.title.data,
            'sub_title': form.sub_title.data,
            'description': form.description.data,
            'image_filename': filename,
            'fee': int(form.fee.data) if form.fee.data else 0,
            'conc_fee': int(form.conc_fee.data) if form.conc_fee.data else 0,
            'multi_day_fee': int(form.multi_day_fee.data) if form.multi_day_fee.data else 0,
            'multi_day_conc_fee': int(form.multi_day_conc_fee.data) if form.multi_day_conc_fee.data else 0,
            'venue_id': form.venue.data,
            'event_dates': form.event_dates.data,
            'start_time': form.start_time.data,
            'end_time': form.end_time.data,
            'dates': form.dates.data,
            'booking_code': form.booking_code.data
        }
        session['submitted_event'] = submitted_event

    set_events(form.events, events, 'New event')
    set_events(form.alt_event_images, events, 'Or use an existing event image:')

    form.event_type.choices = []

    for i, event_type in enumerate(event_types):
        if event_type['event_type'] == 'Talk':
            form.default_event_type.data = i

        form.event_type.choices.append(
            (event_type['id'], event_type['event_type'])
        )

    form.venue.choices = []

    default_venue = [v for v in venues if v['default']][0]
    form.venue.choices.append(
        (default_venue['id'], u'{} - {}'.format(default_venue['name'], default_venue['address']))
    )

    for venue in [v for v in venues if not v['default']]:
        form.venue.choices.append(
            (venue['id'], u'{} - {}'.format(venue['name'], venue['address']))
        )

    form.speakers.choices = [('', '')]
    for speaker in speakers:
        form.speakers.choices.append((speaker['id'], speaker['name']))

    return form


def set_events(form_select, events, first_item_text=''):
    form_select.choices = [('', first_item_text)]

    for event in events:
        form_select.choices.append(
            (
                event['id'],
                '{} - {} - {}'.format(
                    event['event_dates'][0]['event_datetime'], event['event_type'], event['title'])
            )
        )
