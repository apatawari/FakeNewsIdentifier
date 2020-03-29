from flask import Flask, request, Response
from flask_mail import Mail, Message
import os
import json

app = Flask(__name__)

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.environ['EMAIL_USER'],
    "MAIL_PASSWORD": os.environ['EMAIL_PASSWORD']
}

@app.route('/api/email', methods=['POST'])
def send_email():
    
    response = request.data
    print(response)
    
    email_dict = json.loads(response)

    email_subject = email_dict['email_info']['subject']
    email_body = email_dict['email_info']['body']
    email_recipients= email_dict['email_info']['recipients']
    email_content_type=email_dict['supporting_info']['content_type']
    message_hash=email_dict['supporting_info']['message_hash']
    email_link = email_dict['supporting_info']['link']
    
    with app.app_context():
        msg = Message(subject=email_subject,
                      sender=app.config.get("MAIL_USERNAME"),
                      recipients=email_recipients, # use your email for testing
                      body=email_body)
    
        mail.send(msg)

    return Response("Email Sent Successfully",status=200)

if __name__ == '__main__':
    app.config.update(mail_settings)
    mail = Mail(app)
    from waitress import serve
    #app.run(host='127.0.0.1', port=5000, debug=True)
    serve(app, host="127.0.0.1", port=5000)
