from flask_wtf import FlaskForm
from wtforms import MultipleFileField, PasswordField, RadioField, SelectField, StringField, SubmitField, TextAreaField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import InputRequired, Length

from app import db
from app.db_config import db_config
from app.models import Post


class LoginForm(FlaskForm):
    password = PasswordField("Password", validators=[InputRequired(),
            Length(max=db_config["MAXLEN_USER_PASSWORD"])])
    submit = SubmitField("Submit")


class ChooseActionForm(FlaskForm):
    action = RadioField("Actions", choices=[("create", "Create post"), ("edit", "Edit/delete post"),
            ("change_admin_password", "Change admin password")], validators=[InputRequired()])
    submit = SubmitField("Submit")


class CreateBlogpostForm(FlaskForm):
    blog_id = SelectField("Blog", validators=[InputRequired()])
    title = StringField("Title", validators=[InputRequired(),
            Length(max=db_config["MAXLEN_POST_TITLE"])])
    subtitle = StringField("Subtitle", validators=[Length(max=db_config["MAXLEN_POST_SUBTITLE"])])
    content = TextAreaField("Content (Markdown, LaTeX supported)", validators=[InputRequired(),
            Length(max=db_config["MAXLEN_POST_CONTENT"])])
    images = MultipleFileField("Upload images")
    submit = SubmitField("Submit")
    cancel = SubmitField("Cancel", render_kw={"onclick": "window.history.back()"})


class SearchBlogpostForm(FlaskForm):
    post = QuerySelectField("Post", validators=[InputRequired()],
            query_factory=lambda: db.session.query(Post), get_label="title")
    submit = SubmitField("Submit")
    cancel = SubmitField("Cancel", render_kw={"onclick": "window.history.back()"})


class EditBlogpostForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired(),
            Length(max=db_config["MAXLEN_POST_TITLE"])])
    subtitle = StringField("Subtitle", validators=[Length(max=db_config["MAXLEN_POST_SUBTITLE"])])
    content = TextAreaField("Content (markdown supported)", validators=[InputRequired(),
            Length(max=db_config["MAXLEN_POST_CONTENT"])])
    images = MultipleFileField("Upload images")
    submit = SubmitField("Submit")
    delete = SubmitField("Delete Post", render_kw={"onclick": "return confirm('Sanity check');"})
    cancel = SubmitField("Cancel", render_kw={"onclick": "window.history.back()"})


class ChangeAdminPasswordForm(FlaskForm):
    old_password = PasswordField("Old password", validators=[InputRequired(),
            Length(max=db_config["MAXLEN_USER_PASSWORD"])])
    new_password_1 = PasswordField("New password", validators=[InputRequired(),
            Length(max=db_config["MAXLEN_USER_PASSWORD"])])
    new_password_2 = PasswordField("Repeat new password", validators=[InputRequired(),
            Length(max=db_config["MAXLEN_USER_PASSWORD"])])
    submit = SubmitField("Submit")
    cancel = SubmitField("Cancel", render_kw={"onclick": "window.history.back()"})
