from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import Required

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Write a brief bio about you.',validators = [Required()])
    submit = SubmitField('Save')

class CreateBlog(FlaskForm):
    title = StringField('Title',validators=[Required()])
    content = TextAreaField('Blog content',validators=[Required()])
    submit = SubmitField('Post')

class CommentForm(FlaskForm):
    description = TextAreaField('Add Comments', validators = [Required()])
    submit = SubmitField('Submit')