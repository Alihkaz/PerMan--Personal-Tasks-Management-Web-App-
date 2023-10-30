#
import datetime
from flask import Flask, abort, render_template, redirect, url_for, flash, request ,jsonify
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from forms import CreatePostForm, RegisterForm, LoginForm


#FLASK_KEY" is the name of your environment variable.
# so Flask key is a variable that is equal to the actaul password ,
#  so instead of typing the password , we put the variable ,
#  and then acess the password just on our pc through the os library ! 



app = Flask(__name__)
import os
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
ckeditor = CKEditor(app)
Bootstrap5(app)

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

#-----------------------------------------------------------------------------------------------#
# For adding profile images to the comment section
gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)


#---------------------------------------------------------------------------------------------------------#

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] =  os.environ.get("DB_URI", "sqlite:///tasks.db")  
db = SQLAlchemy()
db.init_app(app)



#----------------------------------Creating Relational DataBases------------------------------------------#
#---------------------------------------------------------------------------------------------------------#


# CONFIGURE TABLES
class Tasks(db.Model):
    __tablename__ = "usertasks"

    id = db.Column(db.Integer, primary_key=True)
    # Create Foreign Key, "users.id" the users refers to the tablename of User.
    #so this acts as a key which shows this post to whom is related in the users table

    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    # Create reference to the User object. The "posts" refers to the posts property in the User class.

    title = db.Column(db.String(250), unique=True, nullable=False)

    description = db.Column(db.Text, nullable=False)

    category=db.Column(db.String(250), nullable=False)

    priority=db.Column(db.String(250), nullable=False)

    startdate = db.Column(db.String(250), nullable=False)

    duedate = db.Column(db.String(250), nullable=False)

    status=db.Column(db.String(250), nullable=False)

    reporter = relationship("User", back_populates="tasks")
    






# Create a User table for all your registered users
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    # This will act like a list of BlogPost objects attached to each User.
    # The "author" refers to the author property in the BlogPost class.
    #so here we are saying that this user have posts , its done by seeing the id of the user of the post !
    tasks = relationship("Tasks", back_populates="reporter")




#-----------------------------------------------------------------------------------------------#



with app.app_context():
    db.create_all()


# Create an admin-only decorator
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.id != 1:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)

    return decorated_function



#------------------------------------------Authentication Page-----------------------------------------------------#
#------------------------------------------------------------------------------------------------------------------#

@app.route('/', methods=["GET", "POST"])
def authenticate():
   return render_template("authentication.html")





#--------------------------------------Authentication after filling the data-------------------------------------------#
#-----------------------------------------------------------------------------------------------#

# Register new users into the User database
@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        # Check if user email is already present in the database.
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        user = result.scalar()
        if user:
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))
        #encryption and decryption
        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )

        # adding the new user to the users database , along with the data we get from the form ! 


        new_user = User(
            email=form.email.data,
            name=form.name.data,
            password=hash_and_salted_password)
        

        db.session.add(new_user)
        db.session.commit()


        # This line will authenticate the user with Flask-Login
        login_user(new_user)
        return redirect(url_for("get_board"))
    return render_template("register.html", form=form, current_user=current_user)




#-----------------------------------------------------------------------------------------------#



@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        password = form.password.data
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        # Note, email in db is unique so will only have one result.
        user = result.scalar()
        # Email doesn't exist
        if not user:
            flash("That email does not exist, please try again , or sign-up instead")
            return redirect(url_for('login'))
        # Password incorrect
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('get_board'))

    return render_template("login.html", form=form, current_user=current_user)



#----------------------------------------------------------------------------------------------------------#


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authenticate'))





#------------------------------------------Main Page(for board)-----------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#



@app.route('/board')
def get_board():
        

        #what we are doing here is first make sure that the user is looged in the authentication module , once he is logged in we get 
        # the id of him , then we search in the data base for the tasks and all data related to the id , by that
        # we create for each user a separate account ! So we are filtering the tasks according to the author id . 


       
            result = db.session.execute(db.select(Tasks).where(Tasks.author_id == current_user.id))
            tasks = result.scalars().all()
            to_do_tasks=[task for task in tasks if task.status=='TO DO']
            inprogress_tasks=[task for task in tasks if task.status=='IN PROGRESS']
            done_tasks=[task for task in tasks if task.status=='DONE']
            return render_template("index.html", to_do_tasks=to_do_tasks,
                                                inprogress_tasks=inprogress_tasks,
                                                done_tasks=done_tasks,
                                                current_user=current_user)
        
        


#-----------------------------------------------------------------------------------------------#



# showing the requested task to see from the board ,
# then getting it bfrom the dayabase , and rendering the details to a special format ! 
@app.route("/post/<int:task_id>", methods=["GET", "POST"])
def show_task(task_id):

    requested_task = db.get_or_404(Tasks, task_id)

    return render_template("task_details.html",
                            task=requested_task,
                           current_user=current_user)



#-----------------------------------------------------------------------------------------------#

# Use a decorator so only an admin user can create new posts
@app.route("/new-post", methods=["GET", "POST"])
def add_new_task():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_task = Tasks(
            title=form.title.data,
            description=form.description.data,
            category=form.category.data,
            priority=form.priority.data,
            startdate=form.startdate.data,
            duedate=form.duedate.data,
            status=form.status.data,
            reporter=current_user)
        


        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for("get_board"))
    return render_template("create_task.html", form=form, current_user=current_user)



#-----------------------------------------------------------------------------------------------#

# Use a decorator so only an admin user can edit a post
@app.route("/edit-task/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):

    # what we are doing here is getting the id of the task that the user wants to edit 
    # then fill the data of that task in the form we used to create it with
    # to avoid repition , then we managed to submit to the database the new info of the 
    # task , including its status that it will let it move automatically, 
    task = db.get_or_404(Tasks, task_id)
    edit_form = CreatePostForm(
        title=task.title,
        description=task.description,
        category=task.category,
        priority=task.priority,
        startdate=datetime.datetime.strptime(task.startdate,'%Y-%m-%d'),
        duedate=datetime.datetime.strptime(task.duedate,'%Y-%m-%d'),
        status=task.status,
        reporter=current_user)
   
    # here what we are aiming to do is editing or updating the task in the database with the new data that we get from the 
    # edit form , that is sending the task with a new fresh data about it,
    if edit_form.validate_on_submit():

        task.title = edit_form.title.data
        task.description = edit_form.description.data
        task.category = edit_form.category.data
        task.priority = edit_form.priority.data
        task.startdate = edit_form.startdate.data
        task.duedate =edit_form.duedate.data
        task.status = edit_form.status.data
        task.reporter = current_user

        db.session.commit()


        return redirect(url_for("show_task", task_id=task.id))
    return render_template("create_task.html",
                            form=edit_form, 
                            is_edit=True,
                            current_user=current_user)



#-----------------------------------------------------------------------------------------------#


# Use a decorator so only an admin user can delete a post
@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    post_to_delete = db.get_or_404(Tasks, task_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_board'))



#---------------------------------------Calendar System--------------------------------------------------# 
#-----------------------------------------------------------------------------------------------------#

#getting the calendar html file that will display the calendar with all of its functionality
@app.route("/calendar" ,  methods=["GET", "POST"])
def calendar():
    return render_template("calendar.html")


#giving the function in the html the data about the tasks to be displayed as a form of events on the calendar
@app.route('/calendar-events' , methods=["GET", "POST"])
def calendar_events():
    result = db.session.execute(db.select(Tasks).where(Tasks.author_id == current_user.id))
    tasks = result.fetchall()
    resp = jsonify({'success' : 1, 'result' : tasks})
    resp.status_code = 200
    return resp


	


#-----------------------------------------------------------------------------------------------#

if __name__ == "__main__":
    app.run(debug=True, port=5001)