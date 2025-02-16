from dotenv import load_dotenv
from flask import Flask, render_template, request 
import os
import requests
import smtplib
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


load_dotenv('Lazy Zebra Webpage\.env')

''' 
#previouse email function#

def send_email(name, email, message):
  recipient_email = os.environ.get("RECIPIENT_EMAIL")
  with smtplib.SMTP('smtp.gmail.com') as server:
    email_body = "subject:Lazy Zebra Message!\n\n" + f"{name} is tring to contact you, please email back at {email}. Here is your message '{message}'"+ "\n From Vicky" 
    sender_email = os.environ.get("SENDER_EMAIL")
    sender_pw = os.environ.get('PASSWORD')
    server.starttls()
    server.login(sender_email, sender_pw)
    server.sendmail(os.environ.get("SENDER_EMAIL"), recipient_email, email_body)

'''
def send_email(name, email, message_from_webpage):
      message = Mail(
      from_email= os.environ.get("SENDER_EMAIL"),
      to_emails= os.environ.get("RECIPIENT_EMAIL"),
      subject='Lazy Zebra Message!',
      html_content= f"{name} is tring to contact you, please email back at {email}. Here is your message '{message_from_webpage}'"+ " From Vicky")
      api_key = os.environ.get('SENDGRID_API_KEY')
      sg = SendGridAPIClient(api_key)
      response = sg.send(message)
      print(response.status_code)
      print(response.body)
      print(response.headers)

app = Flask(__name__)
app.send_email = send_email

@app.route("/")
def home_page ():
  blog_request = requests.get('https://api.npoint.io/29e74705f4ce2aa5ff49')
  all_blogs =  blog_request.json()
  print('visited home page')
  return render_template("index.html", all_blogs = all_blogs)

@app.route('/blog/<id>')
def blog(id):
    blog_request = requests.get( url = 'https://api.npoint.io/29e74705f4ce2aa5ff49')
    all_blogs =  blog_request.json()
    blog_to_display = None
    for blog in all_blogs:
        if blog.get('id') == int(id):
            blog_to_display =  blog
    return render_template("blog.html", blog = blog_to_display, id = id)   



@app.route("/contact", methods = ["GET","POST"])
def form_data ():
  if request.method == 'POST':
    name = request.form["fullname"]
    email = request.form["email"]
    message = request.form["message"]
    app.send_email(name, email, message)
    print(f'email sent')
    return f'<h1> Message sent successfully! </h1>'
  else:
     return render_template('contact.html')
  

@app.route("/about")
def about():
  return render_template('about.html')

@app.route("/services")
def service():
  return render_template('service.html')
  

if __name__ == "__main__":
  app.run(debug= True)