from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField , DateField , DateTimeField , SelectField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField


# WTForm for creating a blog post
class CreatePostForm(FlaskForm):

    title = StringField("Task Title", validators=[DataRequired()])
    description = CKEditorField("Task Description")
    category=StringField("Category")
    status=SelectField('Status' , choices =[('TO DO') , ('IN PROGRESS') , ('DONE')] , validators=[DataRequired()])
    priority=SelectField('Priority' , choices =[('Low') , ('Medium') , ('High')])
    startdate = DateField('Start Date', format='%Y-%m-%d' ,validators=[DataRequired()])
    duedate = DateField('Due Date', format='%Y-%m-%d' , validators=[DataRequired()] )
    reporter= StringField("Reporter")
    submit = SubmitField("Create Task")

# Create a form to register new users
class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")


# Create a form to login existing users
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let Me Manage!")










































































# <div class="container px-4 px-lg-5">
#   <div class="row gx-4 gx-lg-5 justify-content-center">
#     <div class="col-md-10 col-lg-8 col-xl-7">
#       <!-- Post preview-->
#       {% for post in all_posts %}
#       <div class="post-preview">
#         <a href="{{ url_for('show_post', post_id=post.id) }}">
#           <h2 class="post-title">{{ post.title }}</h2>
#           <h3 class="post-subtitle">{{ post.subtitle }}</h3>
#         </a>
#         <p class="post-meta">
#           Posted by
#           <!-- post.author.name is now a User object -->
#           <a href="#">{{post.author.name}}</a>
#           on {{post.date}}
#           <!-- Only show delete button if user id is 1 (admin user) -->
#           {% if current_user.id == 1: %}
#           <a href="{{url_for('delete_post', post_id=post.id) }}">✘</a>
#           {% endif %}
#         </p>
#       </div>
#       <!-- Divider-->
#       <hr class="my-4" />
#       {% endfor %}

#       <!-- New Post -->
#       <!-- Only show Create Post button if user id is 1 (admin user) -->
#       {% if current_user.id == 1: %}
#       <div class="d-flex justify-content-end mb-4">
#         <a
#           class="btn btn-primary float-right"
#           href="{{url_for('add_new_post')}}"
#           >Create New Post</a
#         >
#       </div>
#       {% endif %}

#       <!-- Pager-->
#       <div class="d-flex justify-content-end mb-4">
#         <a class="btn btn-secondary text-uppercase" href="#!">Older Posts →</a>
#       </div>
#     </div>
#   </div>
# </div>


















#   <li>
#               <a href="{{ url_for('notes') }}" class="nav-link text-white">
#                 <svg class="bi d-block mx-auto mb-1" width="24" height="24"><use xlink:href="#table"></use></svg>
#                 Notes
#               </a>
#             </li>


#             <li>
#               <a href="{{ url_for('report') }}" class="nav-link text-white">
#                 <svg class="bi d-block mx-auto mb-1" width="24" height="24"><use xlink:href="#grid"></use></svg>
#                 Performance Report
#               </a>
#             </li>