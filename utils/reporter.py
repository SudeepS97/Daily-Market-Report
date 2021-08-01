import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


class Reporter(object):
    def __init__(self, sender, password, receiver, host, port, subject='[REPORT]'):
        self.sender = sender
        self.password = password
        self.receiver = receiver
        self.host = host
        self.port = port
        self.subject = subject
        self.msgRoot = None

    def build_message(self, preamble='End of Message'):
        self.msgRoot = MIMEMultipart('related')
        self.msgRoot['Subject'] = self.subject
        self.msgRoot['From'] = self.sender
        self.msgRoot['To'] = self.receiver
        self.msgRoot.preamble = preamble

    def add_css(self, css_file='utils/style.css'):
        if css_file:
            with open(css_file,'r') as css:
                css_txt = ''.join([line.strip() for line in css.readlines()])
            self.add_HTML(css_txt)

    def add_HTML(self, html):
        txt = MIMEText(html, 'html')
        self.msgRoot.attach(txt)

    def add_image(self, cid, img_path):
        with open(img_path, 'rb') as fp:
            img_data = fp.read()
        msg_image = MIMEImage(img_data, 'png')
        msg_image.add_header('Content-ID', f'<image{str(cid)}>')
        self.msgRoot.attach(msg_image)

    def build_image_grid(self, image_list, img_path, cols=3, offset=0):
        html = "<div class='imgContainer'><img src='cid:image0'></div>"
        html += "<p><div class='row'>"
        col_dict = {}
        for col_num in range(cols):
            col_dict[col_num] = []
        for img_num in range(len(image_list)):
            col_dict[img_num % cols].append(f"<img src='cid:image{img_num+offset}'>")
        for col_num in range(cols):
            html += "<div class='imgContainer'>"
            for img_src in col_dict[col_num]:
                html += img_src
            html += "</div>"
        html += "</div></p>"
        self.add_HTML(html)
        self.add_image(0, f"{img_path}stats_table.png")
        for i, img_path in enumerate(image_list):
            self.add_image(i+offset, img_path)

    def send_message(self):
        context = ssl.create_default_context()
        with smtplib.SMTP(self.host, self.port) as server:
            server.starttls(context=context)
            server.login(self.sender, self.password)
            server.sendmail(self.sender, self.receiver, self.msgRoot.as_string())

