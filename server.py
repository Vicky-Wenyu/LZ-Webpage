from dotenv import load_dotenv
from flask import Flask, render_template, request 
import os
import requests
import smtplib

load_dotenv('Lazy Zabra Webpage\.env')

def send_email(name, email, message):
  recipient_email = 'geyerkristoffer@gmail.com'
  with smtplib.SMTP('smtp.gmail.com') as server:
    email_body = "subject:Lazy Zebra Message!\n\n" + f"{name} is tring to contact you, please email back at {email}. Here is your message '{message}'"+ "\n From Vicky" 
    server.starttls()
    server.login(os.environ['SENDER_EMAIL'], os.environ['PASSWORD'])
    server.sendmail(os.environ['SENDER_EMAIL'], recipient_email, email_body)

app = Flask(__name__)
app.send_email = send_email

@app.route("/")
def home_page ():
  blog_request = requests.get('https://api.npoint.io/29e74705f4ce2aa5ff49')
  all_blogs =  blog_request.json()
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