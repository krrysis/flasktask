import email
from flask import Flask, render_template, url_for, request, redirect
from flask import *
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import re
import gladiator as gl
from sqlalchemy import false

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)




class Todo(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(200), nullable=False)
    add = db.Column(db.String(200), nullable=False)
    mob = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

ROWS_PER_PAGE = 5
@app.route('/', methods=['POST', 'GET'])
def index():
    
    if request.method == 'POST':
        task_fullname = request.form['fullname']
        task_add = request.form['add']
        task_mob = request.form['mob']
        task_email = request.form['email']
        blank=''
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        def isValid(email):
            if re.fullmatch(regex, email):
                return True
            else:
                return False
        
        print(isValid(task_email))
        if(isValid(task_email)==True):
            new_task = Todo(fullname=task_fullname, add=task_add, mob=task_mob, email=task_email)
        else:
            return 'server side validation found invalid email'   

        exists = db.session.query(Todo.id).filter_by(email=task_email).first() is not None
        if exists == True:
            return 'email id already exists in records'
        else:
            pass
        print('exists is printing ',exists)
        try:
            
            db.session.add(new_task)
            db.session.commit()
            
            return redirect('/')
        except:
            return 'There was an issue adding employee'

    else:
        #tasks = Todo.query.order_by(Todo.date_created).all()
        page = request.args.get('page', 1, type=int)
        tasks = Todo.query.paginate(page=page, per_page=ROWS_PER_PAGE)
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.fullname = request.form['fullname']
        #2nd field address
        task.add = request.form['add']
        task.mob = request.form['mob']
        task.email = request.form['email']
                

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)