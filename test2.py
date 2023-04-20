import binascii
import hashlib
import os
import wtforms as wtforms
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from flask import render_template, request, flash, app
from werkzeug.utils import redirect


class UserRegistryForm(wtforms):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')



def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def verify_password(stored_password, provided_password):
    # Verify a stored password against one provided by user
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

@app.route('/test2', methods=['GET', 'POST'])
def user_registry():
    form = UserRegistryForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            email = request.form['email']
            password = hash_password(request.form['password'])
            name = request.form['name']
            return redirect('/')
    else:
        return render_template('registry_form.html', title='Register', form=form)


if __name__ == '__main__':
    app.debug = True
    app.run()
