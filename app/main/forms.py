from flask_wtf import FlaskForm
from wtforms import BooleanField, FormField, FieldList, HiddenField, StringField


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


def populate_user_form(users):
    user_list_form = UserListForm()

    if not user_list_form.users:
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

            user_list_form.users.append_entry(user_form)
    else:
        for user in user_list_form.users:
            found_user = [u for u in users if u['id'] == user.user_id.data]
            if found_user:
                user.str_email.data = found_user[0]['email']

    return user_list_form


def _has_access_area(area, user_access_area):
    if user_access_area:
        return area in user_access_area.split(',')
    return False
