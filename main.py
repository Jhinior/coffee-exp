from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField , URLField , SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location =  URLField('Cafe Location on Google Maps (URL)', validators=[DataRequired(),URL()])
    opening = StringField('Opening Time e.g 8AM',validators=[DataRequired()])
    closing = StringField('Closing Time e.g 5PM',validators=[DataRequired()])
    coffee = SelectField('Coffee Rating',choices=['☕','☕☕','☕☕☕','☕☕☕☕','☕☕☕☕☕'],validators=[DataRequired()])
    wifi = SelectField('Wifi Strength', choices=['✘','💪', '💪💪', '💪💪💪', '💪💪💪💪', '💪💪💪💪💪'],validators=[DataRequired()])
    power = SelectField('Power', choices=['✘','🔌', '🔌🔌', '🔌🔌🔌', '🔌🔌🔌🔌', '🔌🔌🔌🔌🔌'],validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add',methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    data_added = []
    if form.validate_on_submit():
        print(form.data)
        for data in form.data.values():
            data_added.append(data)
        data_added.remove(data_added[-1])
        data_added.remove(data_added[-1])
        with open('cafe-data.csv', "a", newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(data_added)

    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
