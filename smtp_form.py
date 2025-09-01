from flask import Flask, request, Response, url_for, redirect, current_app, abort, jsonify, make_response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import smtplib, ssl, traceback
from email.message import EmailMessage
import json
import logging
from datetime import datetime, date, timedelta
import calendar
from itertools import count
# from uuid import uuid4  # Removed for GitHub upload
import redis
import psycopg2 
import secrets
import re
import string
import hashlib
import time
import os
import requests
# import base64  # Removed for GitHub upload
# from dateutil.relativedelta import relativedelta  # Removed for GitHub upload
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText  
from email.mime.image import MIMEImage



# Company-specific paths removed for GitHub upload
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'docs', 'screenshots'))
LOGO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'docs'))
logo_path = os.path.join(LOGO_DIR, 'company_logo.png')  # Generic placeholder


    
# License key generation functions removed for GitHub upload

def get_db_connection():
    try:
        return psycopg2.connect(
            database='your_database',
            user='your_user',
            password='your_password',
            host='localhost',
            port='5432'
        )
    except Exception as e:
        logging.error(f"Database connection failed: {e}")
        raise

def generate_human_readable_username():
    import random
    adjectives = ["brave", "swift", "clever", "mighty", "fierce", "jolly", "sly", "nimble", "witty", "bold"]
    nouns = ["tiger", "eagle", "fox", "panther", "wolf", "otter", "hawk", "lynx", "bear", "falcon"]
    adjective = random.choice(adjectives)
    noun = random.choice(nouns)
    number = random.randint(100, 999)
    return f"{adjective}_{noun}{number}"

def generate_random_password(length=12):
    import random
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choices(characters, k=length))
    
def generate_code(length=6):
    return ''.join(secrets.choice(string.digits) for _ in range(length))
    

# License key generation function removed for GitHub upload



app = Flask(__name__)

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["50 per minute"]
)
limiter.init_app(app)


logging.basicConfig(filename='feedback.log', level=logging.DEBUG)

with open('config.json', 'r') as f:
    config = json.load(f)

smtp_host = config['smtp_host']
smtp_port = config['smtp_port']
smtp_username = config['smtp_username']
smtp_password = config['smtp_password']
from_address = config['from_address']

# PayPal configuration removed for GitHub upload

redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# PayPal access token function removed for GitHub upload



def send_email_code(email, code):
    msg = EmailMessage()
    msg.set_content(
        f"Thank you for using our service.\n"
        f"Below is your verification code:\n\n"
        f"{code}\n\n"
        f"If you didn't request this, ignore the message."
    )
    
    html_content = f"""
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <title>Verification Code</title>
    </head>
    <body style="margin:0; padding:20px; background-color:#f7f7f7; font-family:Arial, sans-serif; color:#333;">
      <table width="100%" border="0" cellpadding="0" cellspacing="0">
        <tr>
          <td align="center" valign="top">
            <table width="650" border="0" cellpadding="0" cellspacing="0"
                   style="background-color:#fff; border-radius:8px; padding:30px; box-shadow:0 2px 10px rgba(0,0,0,0.4); margin:20px auto;">
    
              <!-- Header -->
              <tr>
                <td align="center" style="padding-bottom:20px;">
                  <h1 style="margin:0; font-size:22px; color:#292929;">Thank you for using our service</h1>
                  <p style="margin:5px 0 0 0; font-size:16px; color:#555;">Below is your verification code:</p>
                </td>
              </tr>
    
              <!-- Code Section -->
              <tr>
                <td style="padding:20px; background-color:#eee; border:2px solid #ddd; border-radius:8px; box-shadow:0 2px 10px rgba(0,0,0,0.2); text-align:center;">
                  <p style="margin:0 0 10px 0; font-size:16px;"><strong>Your code:</strong></p>
                  <div style="background:#ccc; border:1px dashed #ccc; border-radius:4px; padding:15px; font-size:18px; margin-bottom:15px; word-break:break-all; color:#292929; box-shadow:0 2px 10px rgba(0,0,0,0.2);">
                    {code}
                  </div>
                  <p style="margin:0 0 10px 0; font-size:16px; color:#333;">Please copy it and paste into the site page.</p>
                  <p style="margin:0; font-size:16px; color:#333;">If you didn't request this, simply ignore this email.</p>
                </td>
              </tr>
    
            </table>
          </td>
        </tr>
      </table>
    </body>
    </html>
    """
    msg.add_alternative(html_content, subtype="html")
    msg['Subject'] = "Your verification code"
    msg['From'] = from_address
    msg['To'] = email
    
    msg['Reply-To'] = from_address
    
    # Logo attachment removed for GitHub upload
        

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_host, smtp_port) as smtp:
            smtp.ehlo()
            smtp.starttls(context=context)
            smtp.ehlo()
            smtp.login(smtp_username, smtp_password)
            smtp.send_message(msg)
        logging.info(f"Email successfully sent to {email}")

    except Exception as err:
        logging.error(f"Failed to send email to {email}: {err}")
        raise  
        
def send_tryout_email(subject, email, name, username,password):

    msg = EmailMessage()
    msg.set_content (
            f"Hello {name},\n\n"
            f"Your tryout session credentials are:\n"
            f"Username: {username}\n"
            f"Password: {password}\n"
            f"Thank you for trying our service!"
        )

    html_content = f"""
        <html lang="en">
        <head>
          <meta charset="UTF-8">
          <title>Tryout Session</title>
        </head>
        <body style="margin:0; padding:20px; background-color:#f7f7f7; font-family:Arial, sans-serif; color:#333;">
          <table width="100%" border="0" cellpadding="0" cellspacing="0">
            <tr>
              <td align="center" valign="top">
                <table
                  width="650"
                  border="0"
                  cellpadding="0"
                  cellspacing="0"
                  style="
                    background-color:#fff;
                    border-radius:8px;
                    -webkit-border-radius:8px;
                    padding:30px;
                    box-shadow:0 2px 10px rgba(0,0,0,0.4);
                    margin-top:20px;
                    margin-bottom:20px;
                  "
                >
        
                  <!-- Header -->
                  <tr>
                    <td align="center" style="padding-bottom:30px;">
                      <h1 style="margin:10px; font-size:22px; color:#292929;">Hi {name}! Thank you for joining our tryout session!</h1>
                      <p style="margin:0; font-size:16px; color:#555;">Below are your credentials and access details for the trial console, and quick links to help you get started.</p>
                    </td>
                  </tr>
        
                  <!-- Credentials -->
                  <tr>
                    <td style="padding:20px; background-color: #fafafa; border:2px solid #ddd; border-radius:8px; box-shadow:0 2px 10px rgba(0,0,0,0.2);">
                      <div style="margin-bottom:15px;">
                        <strong style="font-size:16px; display:inline-block; width:160px;">Login:</strong>
                        <span style="font-size:16px;">{username}</span>
                      </div>
                      <div style="margin-bottom:15px;">
                        <strong style="font-size:16px; display:inline-block; width:160px;">Password:</strong>
                        <span style="font-size:16px;">{password}</span>
                      </div>
                      <div>
                        <strong style="font-size:16px; display:inline-block; width:160px;">Console Link:</strong>
                        <a href="#" style="font-size:16px; color:#1a73e8; text-decoration:none;">LINK</a>
                      </div>
                    </td>
                  </tr>
        
                  <!-- Spacer -->
                  <tr><td height="20" style="font-size:0; line-height:0;">&nbsp;</td></tr>
        
                  <!-- Quick Links -->
                  <tr>
                    <td>
                      <table width="100%" border="0" cellpadding="0" cellspacing="0">
                        <!-- Link block -->
                        <tr>
                          <td style="padding:15px; background-color:#fafafa; border:2px solid #ddd; border-radius:8px; box-shadow:0 2px 5px rgba(0,0,0,0.1);">
                            <a href="#" style="text-decoration:none; color:#333; display:flex; align-items:center; font-size:16px;">
                              <strong>Brief overview of the console</strong>
                              <span style="margin-left:auto; font-size:16px;">&rarr;</span>
                            </a>
                          </td>
                        </tr>
                        <tr><td height="10" style="font-size:0; line-height:0;">&nbsp;</td></tr>
                        <tr>
                          <td style="padding:15px; background-color:#fafafa; border:2px solid #ddd; border-radius:8px; box-shadow:0 2px 5px rgba(0,0,0,0.1);">
                            <a href="#" style="text-decoration:none; color:#333; display:flex; align-items:center; font-size:16px;">
                              <strong>Documentation</strong>
                              <span style="margin-left:auto; font-size:16px;">&rarr;</span>
                            </a>
                          </td>
                        </tr>
                        <tr><td height="10" style="font-size:0; line-height:0;">&nbsp;</td></tr>
                        <tr>
                          <td style="padding:15px; background-color:#fafafa; border:2px solid #ddd; border-radius:8px; box-shadow:0 2px 5px rgba(0,0,0,0.1);">
                            <a href="#" style="text-decoration:none; color:#333; display:flex; align-items:center; font-size:16px;">
                              <strong>Demos</strong>
                              <span style="margin-left:auto; font-size:16px;">&rarr;</span>
                            </a>
                          </td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
          </table>
        </body>
        </html>
        """
    
    msg.add_alternative(html_content, subtype="html")
    msg['Subject'] = subject
    msg['From'] = from_address
    msg['To'] = email
    
    # Logo attachment removed for GitHub upload
        

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_host, smtp_port) as smtp:
            smtp.ehlo()
            smtp.starttls(context=context)
            smtp.ehlo()
            smtp.login(smtp_username, smtp_password)
            smtp.send_message(msg)
        logging.info(f"Email successfully sent to {email}")
    except Exception as err:
        logging.error(f"Failed to send email to {email}: {err}")
        raise
        

def send_installation_commands_email(email, name):
    msg = EmailMessage()
    html_content = f"""
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <title>Installation Instructions</title>
    </head>
    <body style="margin:0; padding:20px; background-color:#f7f7f7; font-family: Arial, sans-serif; color:#333;">
    
      <table width="100%" border="0" cellpadding="0" cellspacing="0">
        <tr>
          <td align="center" valign="top">
            <table
              width="650"
              border="0"
              cellpadding="0"
              cellspacing="0"
              style="
                background-color:#fff;
                border-radius:8px;
                -webkit-border-radius:8px;
                padding:30px;
                box-shadow:0 2px 10px rgba(0,0,0,0.4);
                margin-top:20px;
                margin-bottom:20px;
              "
            >
    
              <!-- Header -->
              <tr>
                <td align="center" style="padding-bottom:30px;">
                  <h1 style="margin:10px; font-size:22px; color:#292929;">
                    Hi! Thank you for using our service!
                  </h1>
                  <p style="margin:0;">
                    Below you'll find the installation commands:
                  </p>
                </td>
              </tr>
    
              <!-- Installation Commands -->
              <tr>
                <td
                  style="
                    padding:20px;
                    background-color:#fafafa;
                    border:2px solid #ddd;
                    border-radius:8px;
                    -webkit-border-radius:8px;
                    box-shadow:0 2px 10px rgba(0,0,0,0.2);
                  "
                >
                  <strong style="font-size:16px;">Installation Commands:</strong>
                  <div
                    style="
                      font-family: monospace;
                      background:#fafafa;
                      padding:15px;
                      border-radius:5px;
                      white-space: pre-line;
                      margin-top:10px;
                    "
                  >
    bash <(wget -qO- http://example.com/bootstrap.sh)

    or
    
    bash <(curl -s http://example.com/bootstrap.sh)
                  </div>
                </td>
              </tr>
    
              <!-- Spacer -->
              <tr><td height="20" style="font-size:0; line-height:0;">&nbsp;</td></tr>
              
              <!-- Terms of free install -->
              <tr>
                <td
                  style="
                    padding:20px;
                    background-color:#fafafa;
                    border:2px solid #ddd;
                    border-radius:8px;
                    box-shadow:0 2px 10px rgba(0,0,0,0.2);
                  "
                >
                  <h2 style="margin:0 0 15px 0; color:#292929; font-size:18px;">
                    Please note the terms of your free installation
                  </h2>
                  <ol style="margin:0; padding-left:20px; font-size:16px; line-height:1.5; color:#333;">
                    <li style="margin-bottom:10px;">
                      <strong>30-Day Trial:</strong>
                      All automated features (backups, alerts, etc.) are fully enabled for 30 days after installation.
                    </li>
                    <li style="margin-bottom:10px;">
                      <strong>After the Trial:</strong>
                      Automation is disabled, but your databases remain accessible. Manual management is still available with limited functionality.
                    </li>
                    <li style="margin-bottom:10px;">
                      <strong>Activating a License:</strong>
                      Purchase a license on our website to restore automation. Licensed databases are re-enabled; extra databases are marked ?unlicensed.?
                    </li>
                    <li style="margin-bottom:10px;">
                      <strong>No Data Loss:</strong>
                      Even without a license, you retain full access to your clusters and data.
                    </li>
                  </ol>
                </td>
              </tr>
    
              <!-- Spacer -->
              <tr><td height="20" style="font-size:0; line-height:0;">&nbsp;</td></tr>
              <!-- System Requirements -->
              <tr>
                <td
                  style="
                    padding:20px;
                    background-color:#fafafa;
                    border:2px solid #ddd;
                    border-radius:8px;
                    -webkit-border-radius:8px;
                    box-shadow:0 2px 10px rgba(0,0,0,0.2);
                  "
                >
                  <h2 style="margin:0 0 15px 0; color:#292929; font-size:18px;">
                    System Requirements
                  </h2>
                  <table width="100%" border="0" cellspacing="0" cellpadding="0">
                    <tr>
                      <td style="font-size:16px; padding:5px;">Supported platforms:</td>
                      <td style="font-size:16px; padding:5px; text-align:right;"><strong>CentOS10</strong></td>
                    </tr>
                    <tr>
                      <td style="font-size:16px; padding:5px;">RAM:</td>
                      <td style="font-size:16px; padding:5px; text-align:right;"><strong>4GB</strong></td>
                    </tr>
                    <tr>
                      <td style="font-size:16px; padding:5px;">CPUs:</td>
                      <td style="font-size:16px; padding:5px; text-align:right;"><strong>2</strong></td>
                    </tr>
                    <tr>
                      <td style="font-size:16px; padding:5px;">Disk space:</td>
                      <td style="font-size:16px; padding:5px; text-align:right;"><strong>50GB</strong></td>
                    </tr>
                  </table>
                </td>
              </tr>
    
              <!-- Spacer -->
              <tr><td height="20" style="font-size:0; line-height:0;">&nbsp;</td></tr>
    
              <!-- VM Connection Details -->
              <tr>
                <td
                  style="
                    padding:20px;
                    background-color:#fafafa;
                    border:2px solid #ddd;
                    border-radius:8px;
                    -webkit-border-radius:8px;
                    box-shadow:0 2px 10px rgba(0,0,0,0.2);
                  "
                >
                  <h2 style="margin:0 0 15px 0; color:#292929; font-size:18px;">
                    VM Connection Details
                  </h2>
                  <ol style="margin:0; padding-left:20px; font-size:16px; line-height:1.5; color:#333;">
                    <li style="margin-bottom:10px;">
                      <strong>Run a script:</strong> Run the script <code>bootstrap.sh</code> on your VM and follow the instructions.
                    </li>
                    <li style="margin-bottom:10px;">
                      <strong>Accessing the console:</strong> Once the installation is complete you can access the company console at
                      <code>http://ip_address</code> (you will get it after successful installation).
                    </li>
                    <li style="margin-bottom:10px;">
                      <strong>Login and password:</strong> Your initial username and password are ...
                    </li>
                  </ol>
                  <p style="margin:10px 0 20px 0; font-size:16px; color:#333;">
                Below you can find quick links to get started: how to create your first user, a brief overview of the console, and more.
                  </p>
                </td>
              </tr>
    
              <!-- Spacer -->
              <tr><td height="20" style="font-size:0; line-height:0;">&nbsp;</td></tr>
    
              <!-- Quick Links -->
              <tr>
                <td>
                  <table width="100%" border="0" cellpadding="0" cellspacing="0">
                    <!-- Link block -->
                    <tr>
                      <td style="padding:15px; background-color:#fafafa; border:2px solid #ddd; border-radius:8px; box-shadow:0 2px 5px rgba(0,0,0,0.1);">
                        <a href="#" style="text-decoration:none; color:#333; display:flex; align-items:center; font-size:16px;">
                          <strong>Create a new user</strong>
                          <span style="margin-left:auto; font-size:16px;">&rarr;</span>
                        </a>
                      </td>
                    </tr>
                    <tr><td height="10" style="font-size:0; line-height:0;">&nbsp;</td></tr>
                    <tr>
                      <td style="padding:15px; background-color:#fafafa; border:2px solid #ddd; border-radius:8px; box-shadow:0 2px 5px rgba(0,0,0,0.1);">
                        <a href="#" style="text-decoration:none; color:#333; display:flex; align-items:center; font-size:16px;">
                          <strong>Brief overview of the console</strong>
                          <span style="margin-left:auto; font-size:16px;">&rarr;</span>
                        </a>
                      </td>
                    </tr>
                    <tr><td height="10" style="font-size:0; line-height:0;">&nbsp;</td></tr>
                    <tr>
                      <td style="padding:15px; background-color:#fafafa; border:2px solid #ddd; border-radius:8px; box-shadow:0 2px 5px rgba(0,0,0,0.1);">
                        <a href="#" style="text-decoration:none; color:#333; display:flex; align-items:center; font-size:16px;">
                          <strong>Documentation</strong>
                          <span style="margin-left:auto; font-size:16px;">&rarr;</span>
                        </a>
                      </td>
                    </tr>
                    <tr><td height="10" style="font-size:0; line-height:0;">&nbsp;</td></tr>
                    <tr>
                      <td style="padding:15px; background-color:#fafafa; border:2px solid #ddd; border-radius:8px; box-shadow:0 2px 5px rgba(0,0,0,0.1);">
                        <a href="#" style="text-decoration:none; color:#333; display:flex; align-items:center; font-size:16px;">
                          <strong>Demos</strong>
                          <span style="margin-left:auto; font-size:16px;">&rarr;</span>
                        </a>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
    </body>
    </html>
      """

    msg.add_alternative(html_content, subtype='html')
    msg['Subject'] = "Your installation commands"
    msg['From'] = from_address
    msg['To'] = email
    
    # Logo attachment removed for GitHub upload


    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_host, smtp_port) as smtp:
            smtp.starttls(context=context)
            smtp.login(smtp_username, smtp_password)
            smtp.send_message(msg)
        logging.info(f"Installation commands sent to {email}")
    except Exception as err:
        logging.error(f"Failed to send installation email to {email}: {err}")
        raise
        

# License email function removed for GitHub upload


@app.route('/send-install-commands', methods=['OPTIONS', 'POST'])
def send_install_commands():
    if request.method == 'OPTIONS':
        return '', 204

    data = request.get_json(silent=True) or {}
    email = data.get('email', '').strip()
    if not email:
        return jsonify({"error": "Email required"}), 400

    try:
        send_installation_commands_email(email, email)
        return jsonify({"message": "Installation instructions sent to email"}), 200

    except Exception as e:
        tb = traceback.format_exc()
        current_app.logger.error(f"Error sending install commands to {email}:\n{tb}")

       
        return jsonify({
            "error": "Internal Server Error",
            "details": str(e)
        }), 500



@app.route('/tryout', methods=['POST'])
def tryout():
    try:
        
        data = request.get_json()
        email = data.get('email', '').strip()
        name = data.get('name','').strip()
        if not email:
            return jsonify({"error": "No email provided"}), 400

        
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT email_id, verified FROM tryout_sessions WHERE email=%s", (email,))
        row = cur.fetchone()
        
        if row:
            email_id, verified = row
        else:
            cur.execute("INSERT INTO tryout_sessions (email, verified) VALUES (%s, %s) RETURNING email_id", (email, False))
            email_id = cur.fetchone()[0]
            conn.commit()
            verified = False

        if verified:
            return jsonify({"message": "Email already verified"}), 200

        
        username = generate_human_readable_username()
        password = generate_random_password()
        

        
        cur.execute("UPDATE tryout_sessions SET tryout_sent=true, tryout_sent_date=NOW(), username=%s,password=%s WHERE email=%s", (username, password, email)
                   )
        conn.commit()

        subject = "Your Tryout Session Credentials"
        

        send_tryout_email(subject, email, name, username,password)
        logging.info(f"Tryout session email sent to {email}: username={username}")

        return jsonify({
            "message": "Tryout session credentials sent",
            "username": username,
        }), 200

    except Exception as e:
        logging.error("Exception in /tryout endpoint: " + traceback.format_exc())
        return jsonify({"error": str(e)}), 500
    finally:
        try:
            cur.close()
            conn.close()
        except Exception:
            pass
    
    
# Price calculation and order functions removed for GitHub upload


# PayPal routes removed for GitHub upload



@app.route("/isverified", methods=["POST"])
def isverified():
    data = request.get_json()
    email = data.get('email', '').strip()

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT verified FROM email_addresses WHERE email_address=%s", (email,))
        result = cur.fetchone()

        if result:
            email_verified = result[0]
            if email_verified:
                print("DEBUG email verifed")
                response = {"verified": True, "message": "Email already verified."}
                status = 200 
            else:
                response = {"verified": False, "message": "Email found, but not verified."}
                status = 202
        else:
            cur.execute("INSERT INTO email_addresses(email_address, verified) VALUES (%s, %s)", (email, False))
            conn.commit()
            response = {"verified": False, "message": "Email added to database. Verification required."}
            status = 202

        cur.close()
        conn.close()
        return jsonify(response), status

    except Exception as e:
        logging.error(f"Database error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/send-code', methods=['POST'])
def send_code():
    data = request.get_json()
    email = data.get('email')
    if not email:
        return jsonify({"error": "No email provided"}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.callproc('check_email_address_exists', (email,))
        email_already_exists = cur.fetchone()[0]

        if not email_already_exists:
            cur.execute("INSERT INTO email_addresses (email_address, verified) VALUES (%s, %s)", (email, False))
            conn.commit()

        cur.execute("SELECT verified FROM public.email_addresses WHERE email_address=%s", (email,))
        result = cur.fetchone()
        email_already_verified = result[0]

        if email_already_verified:
            return jsonify({"verified": True, "message": "Email already verified"}), 200
        else:
            
            code = generate_code()  
            redis_key = f"verification_code:{email}"
           
            redis_client.set(redis_key, code, ex=300)

            send_email_code(email, code)

            cur.execute("""
                UPDATE email_addresses 
                SET verify_mail_sent=true, verify_mail_sent_date=NOW()
                WHERE email_address=%s
            """, (email,))
            conn.commit()

            logging.info(f"Email {email} not verified => code sent = {code}")
            return jsonify({"verified": False, "message": "Verification code sent to email"}), 202

    except Exception as e:
        logging.error(f"Error in /verify route: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()
        
                
@app.route('/verify-code', methods=['POST'])
def verify_code():
    data = request.get_json()
    email = data.get('email')
    code = data.get('code')
    
    if not email or not code:
        return jsonify({"error": "Email and code required"}), 400

    redis_key = f"verification_code:{email}"
    stored_code = redis_client.get(redis_key)
    
    if stored_code is None:
        return jsonify({"error": "Entered code is incorrect, please check the correct code input"}), 400

    if stored_code == code:
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("UPDATE email_addresses SET verified=true WHERE email_address=%s", (email,))
            conn.commit()
            cur.close()
            conn.close()

            redis_client.delete(redis_key)
            
            return jsonify({"verified": True, "message": "Email verified successfully"}), 200
        except Exception as e:
            logging.error(f"Error verifying code: {e}")
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Invalid code"}), 400

if __name__ == '__main__':
 
    app.run(port=8000, debug=True)

