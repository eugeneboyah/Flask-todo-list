from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# Telling where our database is located = database type 
# along with the path of the database and the database filename
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# initialize the database 
db = SQLAlchemy(app)

# create a model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)  # Fixed typo from 'constent' to 'content'
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)  # Changed astimezone to utcnow

    # create a function that returns the task and its id whenever we create it
    def __repr__(self):
        return f'<Task {self.id}>'
    
    # Create all database tables
with app.app_context():
    db.create_all()

# 🛠️ Route for the home page 
@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(f"Error adding task: {e}")
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)
    

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    
    except Exception as e:
            print(f"Error deleting task: {e}")
            return 'There was an issue deleting that task'
    
@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
        
    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    print("Flask is starting...")  # Print this message for debugging
    app.run(debug=True, host='0.0.0.0', port=5000)
