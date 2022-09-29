import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from project.logger.logger_util import get_logger_instance


class EmailNotifier:
    def __init__(self, **kwargs):
        """
        Initialize the send mail the data
        """
        self.logger = get_logger_instance()
        self.to_list = kwargs.get('to_list')
        self.msg = MIMEMultipart()
        self.admin = ''
        self.msg['Subject'] = ''
        self.msg['From'] = 'oap.support@intel.com'
        self.message = ""
        self.password_reset_link = kwargs.get('password_reset_link')
        self.oap_user = kwargs.get('oap_user')
        self.oap_user_password = kwargs.get('oap_user_password')
        self.oap_user_fullname = kwargs.get('oap_user_fullname')

        self.oap_req_id = kwargs.get('oap_req_id')
        self.oap_provision_type = kwargs.get('oap_provision_type')
        self.oap_tws_link = kwargs.get('oap_tws_link')
        self.notification_type = kwargs.get('notification_type')
        self.oap_sut = kwargs.get('oap_sut')
        self.oap_provision_status = kwargs.get('oap_provision_status')

        self.server = smtplib.SMTP('ecsmtp.pdx.intel.com')
        self.logger.info("Server : {}".format(self.server))
        self.email_footer = "\n\nBest Regards, \nOneAutomationPortal Team"

    def send_email(self):
        """
        Send email via smtp server
        """
        self.logger.info("Sending Email..")
        self.msg['To'] = self.to_list + ',' + self.admin
        print("Recipient List: ", self.msg['To'])
        self.server.sendmail(self.msg['From'], self.msg['To'].split(','), self.msg.as_string())
        self.server.quit()
        self.logger.info("Email sent successfully..")

    def set_subject(self):
        self.msg['Subject'] = 'One Automation Portal- New User Registration'

    def set_body(self):
        """
        set body for email(plain/html)
        """
        self.message = " Hello {} ,\n".format(self.oap_user_fullname)
        self.message += "\nGreetings from OAP Team , You have been successfully registered to One Automation Portal.\n"
        self.message += "\nusername - {}\n".format(self.oap_user)
        self.message += "password - {}\n".format(self.oap_user_password)
        self.message += "One Automation Portal link - https://one-automation-portal.apps1-fm-int.icloud.intel.com/\n"
        self.message += "\nWe recommend you to change your password by using below link-\n"
        self.message += "\npassword reset link - {}".format(self.password_reset_link)
        self.message += "\n\nFor Any Queries or Suggestion , Please connect with us at oneautomationportalteam@intel.com.\n"
        self.message += self.email_footer
        self.msg.attach(MIMEText(self.message, 'plain'))

    def set_body_status_notification(self):
        self.msg['Subject'] = '[{}] OAP {} Execution Completed on {}'.format(self.oap_provision_status,
                                                                             self.oap_provision_type, self.oap_sut)

        self.message = "OAP Manual Provisioning Trigger with Request ID -{} ,\n".format(
            self.oap_req_id)
        self.message += "\nRequest Triggered By - {}\n".format(self.oap_user_fullname)
        self.message += "\nOn system {} for {} has been moved to {} state.\n".format(
            self.oap_sut, self.oap_provision_type, self.oap_provision_status)
        self.message += "\nFor More Details , Follow below Tws Result Link - {}\n".format(self.oap_tws_link)
        self.message += "\n\nFor Any Queries or Suggestion , Please connect with us at oneautomationportalteam@intel.com.\n"
        self.message += self.email_footer
        self.msg.attach(MIMEText(self.message, 'plain'))

    def trigger_email_notification(self):
        if self.notification_type == 'new_user':
            self.set_subject()
            self.set_body()
            self.send_email()
        elif self.notification_type == 'trigger_status':
            self.set_body_status_notification()
            self.send_email()
