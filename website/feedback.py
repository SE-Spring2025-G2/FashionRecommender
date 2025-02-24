from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Feedback
from . import db
from flask_login import login_required, current_user

feedbackbp = Blueprint('feedback', __name__)

@feedbackbp.route("/feedback", methods=["POST","GET"])
@login_required
def feedback(userid = None):
    # print("request {}".format(userid), flush=True)
    #print the ftype, comments, frate and name from the form
    if request.method == "POST":
        feedback_form = request.form
        # print(feedback_form)
        ftype = feedback_form.get('ftype')
        comments = feedback_form.get('comments')
        frate = feedback_form.get('rating')
        name = feedback_form.get('name') if feedback_form.get('anon') != 'on' else 'Anonymous'
        # print(feedback_form.get('ftype'))
        # print(feedback_form.get('comments'))
        # print(feedback_form.get('rating'))
        # print(feedback_form.get('name'))
        # print(feedback_form.get('anon'))

        new_feedback = Feedback(
            ftype=ftype,
            comments=comments,
            frate=frate,
            name=name,
            userid=current_user.id
        )

        db.session.add(new_feedback)
        db.session.commit()
        flash('Feedback submitted successfully', 'success')
        return redirect(url_for('feedback.feedback'))

    # Query previous feedbacks
    feedbacks = Feedback.query.all()
    return render_template("feedback.html", user=current_user, feedbacks=feedbacks, enumerate=enumerate)
    # return render_template("feedback.html",user=current_user, enumerate=enumerate)

# @feedbackbp.route('/feedback', methods=['GET', 'POST'])
# @login_required
# def feedback():
#     print("A")
#     if request.method == 'POST':
#         ftype = request.form.get('ftype')
#         comments = request.form.get('comments')
#         name = request.form.get('name') if request.form.get('anon') != 'anon' else 'Anonymous'

#         if not ftype or not comments:
#             flash('Please fill out all fields', 'danger')
#             return redirect(url_for('feedback.feedback'))

#         new_feedback = Feedback(ftype=ftype, comments=comments, name=name, user_id=current_user.id)
#         db.session.add(new_feedback)
#         db.session.commit()
#         flash('Feedback submitted successfully', 'success')
#         return redirect(url_for('feedback.feedback'))

#     feedbacks = Feedback.query.all()
#     return render_template('feedback.html', feedbacks=feedbacks, user = current_user)