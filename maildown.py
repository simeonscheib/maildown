#coding: utf-8

import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

import markdown
import styles
from bs4 import BeautifulSoup

import html2text

class MDMailer:

    # store server data
    mymail = ""
    username = ""
    password = ""
    smtpserver = ""
    port = None

    # True if connected
    connected = False

    server = None
    html2text_ = html2text.HTML2Text()

    style = styles.github

    done = 0
    recipients_number = 0

    def __init__(self, mymail, smtpserver, port, username, password):
        self.mymail = mymail
        self.username = username
        self.password = password
        self.smtpserver = smtpserver
        self.port = port

        if (self.smtpserver != "" and
            self.port != None and
            self.username != ""):
            try:
                self.server = smtplib.SMTP(self.smtpserver, self.port)

                self.server.ehlo()
                self.server.starttls()
                self.server.ehlo()
                self.server.login(self.username, self.password)
                self.connected = True
                self.server.close()
            except Exception as e:
                print(e)
                return


    # TODO: raises exception????
    '''
    def __del__(self):
        if self.connected:
            self.server.quit()
    '''

    def connect(self):
        try:
            self.server = smtplib.SMTP(self.smtpserver, self.port)
            self.server.ehlo()
            self.server.starttls()
            self.server.ehlo()
            self.server.login(self.username, self.password)
            return True
        except Exception as e:
            print(e)
            return False

    # get text from markdown file
    def get_text(self, filename):
        file = open(filename, "r")
        text_md = file.read()
        file.close

        return text_md

    # convert markdown to html
    def get_html(self, text_md, subject):

        default_html_start = '<!doctype HTML><html><head><meta charset="utf-8"><title>' + subject + '</title>'
        default_html_start += "<style type='text/css'>" + self.style + styles.codehilite_css + styles.admonition + "</style>"
        default_html_start += "</head><body>"
        default_html_end = '</body></html>'

        default_extensions = ['markdown.extensions.extra', 'markdown.extensions.toc', 'markdown.extensions.smarty', 'markdown.extensions.nl2br', 'markdown.extensions.urlize', 'markdown.extensions.Highlighting', 'markdown.extensions.Strikethrough', 'markdown.extensions.markdown_checklist', 'markdown.extensions.superscript', 'markdown.extensions.subscript', 'markdown.extensions.codehilite', 'markdown.extensions.def_list', 'markdown.extensions.admonition']
        safe_extensions = ['markdown.extensions.extra', 'markdown.extensions.nl2br']

        # convert ...
        try:
            html_body = markdown.markdown(text_md, extensions=default_extensions)
        except:
            try:
                html_body = markdown.markdown(text_md, extensions=safe_extensions)
            except:
                html_body = markdown.markdown(text_md)

        # concatenate html
        html_ugly = default_html_start + html_body + default_html_end
        soup = BeautifulSoup(html_ugly, "lxml")

        # change inline images to absolute path "file:/home..."
        for img in soup.findAll('img'):
            img_path = img.get('src')
            if img_path == None:
                continue
            if os.path.exists(img_path):

                img['src'] = 'file:' + os.path.abspath(img_path)

        return soup.prettify()

    # send converted markdown to list or dict of recipients
    def send_mail(self, text_md, subject, recipients, files=None):

        html_message = self.get_html(text_md, subject)

        # change image paths to attachment and store image paths
        soup = BeautifulSoup(html_message, "lxml")
        images = []
        for img in soup.findAll('img'):
            img_path = img.get('src')
            if "file:" in img_path:
                images.append(img_path.replace("file:", ""))

                img['src'] = 'cid:' + os.path.basename(img_path)

        html_message = soup.prettify()

        # get plain text alternative
        plain_text = self.html2text_.handle(html_message)

        # make MIMEApplication for every attachment
        MIMEApplication_list = []
        for f in files or []:
            with open(f, "rb") as fil:
                MIMEApplication_list.append(
                    MIMEApplication(fil.read(), Name=os.path.basename(f))
                    )
            MIMEApplication_list[-1]['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(f)

        if not self.connect():
            return

        recipients_number = len(recipients)
        done = 0
        # iterate recipients
        for to_mail in recipients:

            msg = MIMEMultipart()
            msg['Subject'] = subject
            msg['From'] = self.mymail
            msg['To'] = to_mail

            if isinstance(recipients, dict):
                plain_text2, html_message2 = self.replace_placeholders(
                                    plain_text,
                                    html_message,
                                    recipients[to_mail],
                                    to_mail
                                    )
                if plain_text2 == None:
                    continue
            else:
                plain_text2 = plain_text
                html_message2 = html_message

            plain_part = MIMEText(plain_text2, 'plain')
            html_part = MIMEText(html_message2, 'html')

            alternative_mmp = MIMEMultipart("alternative")
            alternative_mmp.attach(plain_part)
            related_mmp = MIMEMultipart("related")
            related_mmp.attach(html_part)

            # attach inline images
            for f in images or []:
                with open(f, "rb") as fil:
                    part = MIMEApplication(fil.read(), Name=os.path.basename(f))
                part['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(f)
                part['Content-Id'] = '<%s>' % os.path.basename(f)
                related_mmp.attach(part)

            alternative_mmp.attach(related_mmp)
            msg.attach(alternative_mmp)

            for part in MIMEApplication_list:
                msg.attach(part)

            msg_str = msg.as_string()

            self.server.sendmail(self.mymail, to_mail.split(", "), msg_str)
            done += 1
            self.progress(done, recipients_number)

        self.server.close()

    # send .md file
    def send_md_file(self, filename, subject, recipients, files=None):
        self.send_mail(self.get_text(filename), subject, recipients, files)

    def replace_placeholders(self, plain_text, html_message, content, to_mail):
        plain_text2 = plain_text
        html_message2 = html_message

        if isinstance(content, list):
            # replace e.g. "§§0§§" by
            # recipients = {"email@example.com": [->"first"<-, "second"]}
            replacables = 0
            try:
                replacables = len(content)
            except:
                pass

            try:
                if (replacables > 0):
                    for i in range(replacables):
                        plain_text2 = plain_text2.replace("§§" + str(i) + "§§", content[i])
                        html_message2 = html_message2.replace("§§" + str(i) + "§§", content[i])
            except:
                print("could not replace placeholders for " + to_mail)
                print("skipping...")
                return None, None
        elif isinstance(content, dict):
            try:
                for i in content:
                    plain_text2 = plain_text2.replace("§§" + str(i) + "§§", content[i])
                    html_message2 = html_message2.replace("§§" + str(i) + "§§", content[i])
            except:
                print("could not replace placeholders for " + to_mail)
                print("skipping...")
                return None, None
        else:
            print("Unknown Type" + type(content))

        return plain_text2, html_message2

    def progress(self, done, recipients_number):
        print("Sent to " + done + " of " + recipients_number )
