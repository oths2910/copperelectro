from flask import Flask, render_template, request, flash
from flask_mail import Mail, Message
import csv

app = Flask(__name__)

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": 'copperelectromeltcontact', #os.environ['EMAIL_USER'],
    "MAIL_PASSWORD": 'C3s2palx1320' #os.environ['EMAIL_PASSWORD']
}

app.config.update(mail_settings)
mail = Mail(app)

def send_mail(data):
    name = data["name"]
    email = data["email"]
    subject = data["subject"]
    message = data["message"]
    with app.app_context():
        msg = Message(subject=f'Demande de contact de {email}',
                      sender=app.config.get("MAIL_USERNAME"),
                      recipients=["othman.lamdouar@gmail.com"], # replace with your email for testing
                      body=f"Nouvelle demande de contact :\n\n{name}<{email}>\n\nSujet : {subject}\n\n{message}")
        mail.send(msg)

@app.route('/')
def hello_world():
    #return 'Heeloll lo'
    return render_template('index.html')   

@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)

def write_to_csv(data):
    with open('database.csv', mode='a', newline='') as database2:
        name = data["name"]
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        csv_writer = csv.writer(database2, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([name,email,subject,message])

@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        data = request.form.to_dict()
        print('try to send mail')
        send_mail(data)#write_to_csv(data)
        return render_template('message_sent.html')