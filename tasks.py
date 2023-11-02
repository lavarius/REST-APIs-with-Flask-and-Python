import os
import requests
import jinja2

from dotenv import load_dotenv

load_dotenv()

DOMAIN = os.getenv("MAILGUN_DOMAIN")
tempalte_loader = jinja2.FileSystemLoader("templates")
tempalte_env = jinja2.Environment(loader=tempalte_loader)


def render_template(template_filename, **context):
    return tempalte_env.get_template(template_filename).render(**context)


def send_simple_message(to, subject, body, html):
    return requests.post(
		f"https://api.mailgun.net/v3/{DOMAIN}/messages",
		auth=("api", os.getenv("MAILGUN_API_KEY")),
		data={"from": f"Mark Bartolo <mailgun@{DOMAIN}>",
			"to": [to],
			"subject": subject,
			"text": body,
            "html": html})


def send_user_registration_email(email, username):
    return send_simple_message(
        email,
        "Successfully signed up",
        f"Hi {username}! You have successfully signed up to the Stores REST API.",
        # code from action.html
        render_template("email/action.html", username=username)
    )