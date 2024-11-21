from flask_wtf import FlaskForm
import wtforms



class ReviewForm(FlaskForm):
    grade = wtforms.RadioField("Оберіть оцінку")
    text = wtforms.TextAreaField("Введіть свій відгук")
    author = wtforms.StringField("Напишіть своє ім'я")
    submit = wtforms.SubmitField("Зберегти")