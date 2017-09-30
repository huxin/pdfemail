import argparse
import base64
import os
import sys
import time
import httplib2
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr
from apiclient import errors
import pytz
from datetime import datetime

def get_current_pst_time():
    utc = pytz.utc
    loc_dt = utc.localize(datetime.now())
    pacific = pytz.timezone('US/Pacific')
    fmt = '[%m/%d %H:%M %Z]'
    return loc_dt.astimezone(pacific).strftime(fmt)


parser = argparse.ArgumentParser(parents=[tools.argparser])
flags = parser.parse_args()
flags.noauth_local_webserver = True

SCOPES = "https://mail.google.com/"
CLIENT_SECRET_FILE = 'client_secret_monitor.json'
APPLICATION_NAME = 'monitor_pdf'
import getpass
user = getpass.getuser()

def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   APPLICATION_NAME + '.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.params['access_type'] = 'offline'
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store, flags)
        print 'Storing credentials to ' + credential_path
    return credentials


def create_text_message(sender_name, sender_email, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = formataddr((str(Header(sender_name, 'utf-8')), sender_email))
    message['subject'] = Header(subject, 'utf-8')
    return {'raw': base64.urlsafe_b64encode(message.as_string())}

def send_email(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        return message
    except errors.HttpError, error:
        print 'An error occured: %s' % error

    return "ERROR!"

def get_email_address(serivce):
    user_profile = serivce.users().getProfile(userId='me').execute()
    return user_profile['emailAddress']


credentials = get_credentials()
http = credentials.authorize(httplib2.Http())
service = discovery.build('gmail', 'v1', http=http)
sender_email = get_email_address(service)
print "Successfully get sender email: {}".format(sender_email)
to = 'huxinsmail@gmail.com'
history_file = "/tmp/prev_pdf_cnt"
def create_service_send_email(subject, body):
    message = create_text_message("GCPAlert", sender_email, to, subject, body)
    print "Send email to {}".format(to)
    print "subject:", subject
    print "Body:", body
    print send_email(service, "me", message)


def get_pdf_cnt(d):
    cnt = 0
    for f in os.listdir(d):
        if f.endswith('.pdf'):
           cnt += 1
    return cnt


def get_history_cnt():
    if not os.path.exists(history_file):
        return -1, -1, []

    p = open(history_file).readline().strip().split()
    if len(p) == 2:
        alert_times = []
    else:
        alert_times = [int(t) for t in p[2:]]

    return int(p[0]), int(p[1]), alert_times

def save_history_cnt(cnt, alert_times):
    with open(history_file, 'w') as f:
        print >> f, int(time.time()), cnt,
        for t in alert_times:
            print >>f, t,



def main():
    pdf_dir = "/home/huxin/Downloads"
    if len(sys.argv) > 1:
        pdf_dir = sys.argv[1]

    cur_cnt = get_pdf_cnt(pdf_dir)
    cur_ts = int(time.time())

    prev_ts, prev_cnt, alert_times = get_history_cnt()

    print "Previous: {} pdfs at {} [{}]".format(prev_cnt, prev_ts, time.ctime(prev_ts))
    print "Current:  {} pdfs at {} [{}]".format(cur_cnt, prev_ts, time.ctime(cur_ts))


    # determine if we want to send out an alert
    if prev_cnt == cur_cnt:
        # send out an alert
        if len(alert_times) > 0 and (cur_ts - sorted(alert_times)[-1] < 3600):
            print "Already alerted within last hour, do not alert"
        else:
            diff = cur_ts-prev_ts
            subject = "{} ({}) No new pdf for {} seconds".format(get_current_pst_time(), cur_cnt, diff)
            body = "[Alert] there is no new pdf generated in {} seconds\n".format(diff)
            body += "Previous: {} pdfs at {} [{}]\n".format(prev_cnt, prev_ts, time.ctime(prev_ts))
            body += "Current:  {} pdfs at {} [{}]\n".format(cur_cnt, prev_ts, get_current_pst_time())
            body += "Alert history: {}\n".format(alert_times)
            create_service_send_email(subject, body)
            alert_times.append(cur_ts)
            save_history_cnt(cur_cnt, alert_times)
    else:
        print "PDF count changed, No alert sent!"
        save_history_cnt(cur_cnt, [])



if __name__ == "__main__":
    print
    print time.ctime()
    try:
        main()
    except Exception as e:
        import traceback
        subject = "Exception in PDFmonitor:" + str(e) + ' @ ' + get_current_pst_time()
        body = traceback.format_exc()
        create_service_send_email(subject, body)



