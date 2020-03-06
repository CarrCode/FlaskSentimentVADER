from flask import render_template, url_for, request
from app import app, db
from app.models import Post
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class PostForm(FlaskForm):
    post = TextAreaField('How do you feel about it?', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = PostForm()
    sent_model = SentimentIntensityAnalyzer()
    if form.validate_on_submit():
        sent = sent_model.polarity_scores(str(form.post.data))
        snt = pd.DataFrame.from_dict([sent]).drop('compound',axis=1).rename(columns={"neg": "Negative", "pos": "Positive", "neu": "Neutral"})
        sentimax = snt[snt.idxmax(axis=1)]
        for col in sentimax.columns: 
            sentiment = col
        post = Post(body=form.post.data, sentiment=sentiment)
        db.session.add(post)
        db.session.commit()
        return render_template("results.html", title="Sentiment Analysis", sentiment=sentiment)       
    return render_template("index.html", title="Sentiment Analysis", form=form)