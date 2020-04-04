# -*- codig: utf-8 -*-

import os

from app import app, db
from app.models import Users, PriceHistory
from app.helpers import get_date_object_from_string, get_spreadsheets_object, get_current_year

from flask import render_template, request, session, url_for, redirect, flash, g


@app.before_request
def before_request():
    if 'current_user' in session:
        g.current_user = True

        user = Users.query.filter_by(username=session['current_user']).first()

        if user.admin:
            g.admin = True
    
    else:
        g.current_user = False
        g.admin = False


@app.route('/')
@app.route('/home')
def index():
    year = request.args.get('year', get_current_year())
    month = request.args.get('month', 'all')

    ph = PriceHistory

    if month == 'all':
        qr = ph.query.filter(ph.date.between(f'{year}-01-01', f'{year}-12-31')).all()
    else:
        qr = ph.query.filter(ph.date.like(f'{year}-{month}-%')).all()

    dates = [str(ph_object.date) for ph_object in qr]
    prices = [ph_object.price for ph_object in qr]
    
    return render_template('index.html', title='Inicio', dates=dates, prices=prices)


@app.route('/about')
def about():
    return render_template('about.html', title='Acerca de')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.current_user:
        return redirect(url_for('index'))

    if request.method == 'POST':
        user = Users.query.filter_by(username=request.form['username']).first()

        if user and user.check_password(request.form['password']):
            session['current_user'] = user.username
            flash('Welcome {}!'.format(user.username), 'success')
            return redirect(url_for('index'))
        else:
            flash('Something went wrong there. Try again.', 'error')
            return redirect(url_for('login'))
    
    return render_template('login.html', title='Login')


@app.route('/logout')
def logout():
    session.pop('current_user', None)
    return redirect(url_for('index'))


@app.route('/admin')
def admin():
    if g.current_user and g.admin:
        return render_template('admin.html', title='Admin Panel')
    return redirect(url_for('index'))


@app.route('/admin/upload', methods=['GET', 'POST'])
def upload():
    if g.current_user and g.admin:

        if request.method == 'POST':
            file = request.files['file']
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('Your file has been uploaded', 'success')
    
        return render_template('upload.html', title='Admin Panel')
    
    return redirect(url_for('index'))


@app.route('/admin/update', methods=['GET', 'POST'])
def update():
    if g.current_user and g.admin:

        if request.method == 'POST':

            if request.form['update_method'] == 'xlsx':
                sheet = get_spreadsheets_object(app.config['UPLOAD_FOLDER'] + 'dolartoday.xlsx', 'DolarToday')

                ph = PriceHistory

                count = 0
                for i in range(1, sheet.nrows):
                    date = sheet.cell_value(i, 0)
                    price = sheet.cell_value(i, 1)

                    date_obj = get_date_object_from_string(date)

                    ph_obj = ph.query.filter_by(date=date_obj).first()

                    if not ph_obj:
                        new_ph = PriceHistory(date=date_obj, price=price)
                        db.session.add(new_ph)
                        db.session.commit()
                        count += 1
                
                flash('Updated records: {}'.format(count), 'success')

        return render_template('update.html', title='Admin Panel')
    
    return redirect(url_for('index'))