import datetime,time,sys
from flask import Flask
from flask import render_template, flash, redirect, request, url_for,g
from flask_login import login_required, current_user, LoginManager, login_user, logout_user

# from app import with_s as ws
from app import app
from app.forms import UsernamePasswordForm,RecordForm
from . import db
from app.models import Records,Admin



@app.route('/', methods = ['GET', 'POST'])
def index():
    mtime=str(time.strftime("%Y-%m-%d %H:%M", time.localtime()))
    form = RecordForm()
    form.time.data=mtime
    if form.validate_on_submit():
        myRecord=Records(form.time.data,form.record.data)
        db.session.add(myRecord)
        db.session.commit()
        # return redirect(url_for('success'))
        return render_template('success.html')
    return render_template('index.html',form=form)


@app.route('/showchart')
@login_required
def showchart():
    '''按照要求显示图表'''
    rs=Records.query.all()
    mlist=[]
    mstr={}
    mstr2={}
    for i in rs:
        timeArray = time.strftime("%Y-%m-%d",time.strptime(i.date, "%Y-%m-%d %H:%M"))
        mstr[timeArray]=len(i.text)
        mlist.append(timeArray)
        if timeArray in mstr2:
            mstr2[timeArray]=mstr2[timeArray] + mstr[timeArray]
        else:
            mstr2[timeArray]= mstr[timeArray]
    data = mstr2
    mlist.sort()
    return render_template('showchart.html',data=data,list=mlist)

@app.route('/showlist', methods = ['GET', 'POST'])
@login_required
def showlist():
    rs=Records.query.all()
    mstr={}
    mlist=[]
    for i in rs:
        mlist.append(i.date)
        mstr[i.date]=i.text
    return render_template('showlist.html',list=mlist,data=mstr )

@app.route('/login', methods = ['GET', 'POST'])
def login():
    next = request.args.get('next')
    form = UsernamePasswordForm()
    if form.validate_on_submit():
        user = Admin.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(next or url_for('index'))
        flash('用户名或密码错误')
    return render_template('login.html', form = form)

@app.route("/rzContent")
@login_required
def rzContent():
    return render_template('rzContent.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
