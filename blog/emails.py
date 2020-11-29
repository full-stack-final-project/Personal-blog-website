from flask import url_for, current_app
from flask_mail import Message
from blog.extensions import mail
from threading import Thread



def send_mail(subject, to, html):
    message = Message(subject,sender=current_app.config['MAIL_DEFAULT_SENDER'] ,recipients=[to], html=html)
    thread = Thread(target=_send_async, 
            args=[current_app._get_current_object(), message])
    thread.start()
    return thread
    
    
def _send_async(app, message):
    with app.app_context():
        mail.send(message)
    

def send_new_comment_reminding(article):
    send_mail(subject='New Comment for your article(Do not reply this email)', 
        to=current_app.config['MAIL_USERNAME'],
        html='<p>New comment for your <a href="%s">"%s"</a></p>'
             % ( (url_for('blog.display_article', article_id=article.id, _external=True)  + '#comments'), article.title)

def send_reply_comment(comment):
    send_mail(subject='New Reply for your comment(s) in your article(Do not reply this email)', 
        to=comment.email,
        html='<p>New reply for your comment(s) in <a href="%s">"%s"</a></p>'
             % ( (url_for('blog.display_article', article_id=comment.article_id, _external=True) + '#comments'), comment.article.title)