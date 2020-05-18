from flask import Flask, render_template, request, redirect,url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///newmeet.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)


class Meet(db.Model):
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    meetingroom = db.Column(db.String(200))
    employee = db.Column(db.String(200))
    stime = db.Column(db.String(200))
    etime = db.Column(db.String(200))


@app.route('/new',methods=["GET","POST"])
def new_meeting():
    if request.method == "GET":
        meetings = Meet.query.all()
        page = 'home'
        meeting = Meet(meetingroom='', employee='', stime='', etime='')
        return render_template('home.html', meetings=meetings, page=page, meeting=meeting)
    else:
        meetingroom = request.form['meetingroom']
        employee = request.form['employee']
        stime = request.form['stime']
        etime = request.form['etime']
        newmeeting = Meet(meetingroom=meetingroom, employee=employee, stime=stime, etime=etime)
        db.session.add(newmeeting)
        db.session.commit()
        return redirect(url_for('get_meeting'))


@app.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html')


# Get List for all meeting

@app.route('/all',methods=['GET','POST'])
def get_meeting():
    meetings = Meet.query.all()
    page ='home'
    meeting = Meet(meetingroom='',employee='',stime='',etime='')
    return render_template('all.html',meetings=meetings,page=page,meeting=meeting)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Meet.query.get_or_404(id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for('get_meeting'))


@app.route('/update/<int:id>',methods=["GET","POST"])
def update(id):
    meeting = Meet.query.get_or_404(id)
    if request.method == 'POST':
        meeting.meetingroom = request.form['meetingroom']
        meeting.employee = request.form['employee']
        meeting.stime = request.form['stime']
        meeting.etime = request.form['etime']
        db.session.commit()
        return redirect('/all')
    else:
        meetings = Meet.query.all()
        page ='updatehome'
        return render_template('new.html',page=page,meetings=meetings,meeting=meeting)


if __name__ == "__main__":
    app.run(debug=True)