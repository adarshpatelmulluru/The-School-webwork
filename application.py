from flask import Flask, render_template, url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import delete
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)



class Todo(db.Model):
     student_id = db.Column(db.Integer, primary_key=True)
     student_name = db.Column(db.String(200), nullable=False)
     student_number = db.Column(db.Integer, default=0)
     student_mail = db.Column(db.String(50), nullable=False)
     student_marks = db.Column(db.Integer, default=0)
     date_created = db.Column(db.DateTime, default=datetime.utcnow)


     def __repr__(self):
        return '<student %r>' % self.id
'''
with app.app_context():
    db.create_all()
'''

@app.route('/')







@app.route('/', methods = ['POST','GET'])
def writer():
    if request.method == 'POST':
       student_id = request.form['std_id']
       student_name = request.form['std_name']
       student_number = request.form['std_rollno']
       student_mail = request.form['std_mail']
       student_marks = request.form['std_marks']

       student_list=Todo(student_id=student_id,student_name=student_name,student_number=student_number,student_mail=student_mail,student_marks=student_marks)
       try:
            db.session.add(student_list)
            db.session.commit()
            return redirect('/')
       except:
            return 'Error in creating student data'


    else:
       past_list=Todo.query.order_by(Todo.date_created).all()
       return render_template('index.html', past_list=past_list)


@app.route('/delete/<int:student_id>')
def delete(student_id):
    student_delete = Todo.query.get_or_404(student_id)

    try:
         db.session.delete(student_delete)
         db.session.commit()
         return redirect('/')
    except:
         return 'There was a problem in deleting student detail'

@app.route('/update/<int:student_id>' ,methods=['GET','POST'])
def update(student_id):
    list= Todo.query.get_or_404(student_id)

    if request.method == 'POST':
        list.student_id = request.form['std_id']
        list.student_name = request.form['std_name']
        list.student_number = request.form['std_rollno']
        list.student_mail = request.form['std_mail']
        list.student_marks = request.form['std_marks']

        try:
             db.session.commit()
             return redirect('/')
        except:
             return 'There was an issue updating the student data'
    else:
         return render_template('update.html',list=list)

if __name__ == '__main__':
    app.run(debug=True, port=8080, use_reloader=False)
