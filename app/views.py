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
    if request.method == 'GET':   # 这里必须要增加一个request的判断，否则form.time.data每次都会赋值错误
        form.time.data=mtime
    # form['time']=mtime
    if form.validate_on_submit():
        mdate=form.time.data
        myRecord=Records(mdate,form.record.data)
        # myRecord=Records(form['time'],form['record'])
        db.session.add(myRecord)
        db.session.commit()
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
        if not timeArray in mlist:
            mlist.append(timeArray)
        if timeArray in mstr2:
            mstr2[timeArray]=mstr2[timeArray] + mstr[timeArray]
        else:
            mstr2[timeArray]= mstr[timeArray]
    data = mstr2
    mlist.sort()
    print(mlist)
    return render_template('showchart.html',data=data,list=mlist)

@app.route('/showlist', methods = ['GET', 'POST'])
@login_required
def showlist():
    rs=Records.query.all()
    mstr={}
    mlist=[]
    for i in rs:
        timeStr=i.date.replace("+"," ")
        mlist.append(timeStr)
        mstr[timeStr]=i.text
    form = RecordForm()
    if form.validate_on_submit():
        mdate=form.time.data
        rs=Records.query.filter_by(date=mdate).first()
        if rs is not None:
            rs.date=mdate
            rs.text=form.record.data
            db.session.commit()
        else:
            rs2=Records.query.filter_by(text=form.record.data).first()
            if rs2 is not None:
                rs2.date=mdate
                rs2.text=form.record.data
                db.session.commit()
            else:
                flash('日期和时间都对不上啊！')
    return render_template('showlist.html',list=mlist,data=mstr ,form2=form)

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

@app.route("/myLog")
@login_required
def myLog():
    name = request.args.get('name')
    print("name={"+name+"}")
    name=name[0:16]
    # name2=name[0:16].replace(" ","+")
    # name = request.args.get('name').replace("%3A",":").replace(" ","+")
    rs=Records.query.filter_by(date=name).first()
    if rs == None:
        return("没有找到内容！")
    myStr=rs.date
    print(myStr+" "+rs.text)
    return myStr+" "+rs.text

