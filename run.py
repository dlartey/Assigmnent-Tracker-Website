from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from datetime import datetime 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Create a Flask Instance
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Assignment.db'

app.config['SECRET_KEY'] = "coursework1"

# Initialize The Database
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Create Model
class Assignment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(40), nullable = False)
	code = db.Column(db.String(10), nullable = False)
	deadline = db.Column(db.String)
	description = db.Column(db.String(400))
	completed = db.Column(db.Integer)
	date_added = db.Column(db.DateTime, default=datetime.utcnow)

	# Create A String
	def __repr__(title):
		return '<Title %r>' % title.title


class AssignmentForm(FlaskForm):
    title = StringField("title", validators=[DataRequired()])
    code = StringField("module code", validators=[DataRequired()])
    deadline = StringField("date", validators=[DataRequired()])
    description = StringField("description", validators=[DataRequired()])
    submit = SubmitField("Submit")
    complete = IntegerField("completed", validators=[DataRequired()])

# Update Database Record
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
	form = AssignmentForm()
	update_assignment = Assignment.query.get_or_404(id)
	if request.method == "POST":
		update_assignment.title = request.form['title']	
		update_assignment.completed = request.form['complete']
		update_assignment.description = request.form['description']	
		update_assignment.deadline = request.form['deadline']
		update_assignment.title = request.form['title']	
		update_assignment.code = request.form['code']			
		try:
			db.session.commit()
			flash("User Updated Successfully!")
			return render_template("update.html", 
				form=form,
				update_assignment = update_assignment)
		except:
			flash("Error!  Looks like there was a problem...try again!")
			return render_template("update.html", 
				form=form,
				update_assignment = update_assignment)
	else:
		return render_template("update.html", 
				form=form,
				update_assignment = update_assignment)

@app.route('/add_assignment', methods=['GET', 'POST'])
def add_assignment():
	title = None
	form = AssignmentForm()
	if form.validate_on_submit():
		data = Assignment.query.filter_by(title=form.title.data).first()
		if data is None:
			# If there is no title in the database then add a new one
			data = Assignment(title=form.title.data, code=form.code.data, deadline=form.deadline.data, description=form.description.data, completed=form.complete.data)
			db.session.add(data)
			db.session.commit()
		title = form.title.data
		form.title.data = ''
		form.code.data = ''
		form.deadline.data = ''
		form.description.data = ''
		form.complete.data = ''

		flash("Assignment Added Successfully!")
	get_assignments = Assignment.query.order_by(Assignment.id)
	return render_template("add_assignment.html", 
		form=form,
		title=title,
		get_assignments=get_assignments)

# Create a route decorator
@app.route('/')
def index():
	return render_template("index.html")

@app.route('/uncompleted', methods=['GET', 'POST'])
def uncompleted():
	uncomplete = Assignment.query.filter_by(completed=0)
	return render_template("uncompleted.html", 
		uncomplete=uncomplete)

@app.route('/completed', methods=['GET', 'POST'])
def completed():
	complete = Assignment.query.filter_by(completed=1)
	return render_template("completed.html", 
		complete=complete)

@app.route('/all_assignments', methods=['GET', 'POST'])
def all_assignments():
	assingments = Assignment.query.order_by(Assignment.id)
	return render_template("all_assignments.html", 
		assingments=assingments)