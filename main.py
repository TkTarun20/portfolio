from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
from flask_wtf.csrf import CSRFProtect
import datetime
import os


app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = os.environ['ID']
app.config['MAIL_PASSWORD'] = os.environ['PW']
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

csrf = CSRFProtect(app)
mail = Mail(app)

current_year = datetime.datetime.now().year

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            msg = Message(
                subject='Employment',
                recipients=[os.environ.get('ID')],
                body=f'Name: {request.form.get("name")}\n'\
                    f'Company: {request.form.get("company")}\n'\
                    f'Mail-id: {request.form.get("email")}\n'\
                    f'Message: {request.form.get("message")}',
                sender=os.environ.get('ID')
                    )
            mail.send(msg)
            flash('Message sent successfully!', category='success')
        except:
            flash('Message sending Failed! Please try again later.', category='danger')
        finally:
            return redirect(url_for('home'))
    return render_template('index.html', current_year=current_year)


@app.route('/certificate')
def show_certificate():
    return render_template('doc.html', current_year=current_year)


if __name__ == '__main__':
    app.run(debug=False)