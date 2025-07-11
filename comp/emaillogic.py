import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import env
class EmailLogic:
    def __init__(self):
        self.smtp_host = env.SMTP_HOST
        self.smtp_port = env.SMTP_PORT
        self.smtp_user = env.SMTP_USER
        self.smtp_pass = env.SMTP_PASS
        self.sender = env.SMTP_SENDER
        self.appnameme = env.APP_NAME
        
    def send_verification_email(self, to_email, verification_code):
        """
        发送验证码邮件
        
        Args:
            to_email: 收件人邮箱
            verification_code: 验证码
            
        Returns:
            bool: 发送成功返回True，否则返回False
        """
        try:
            # 创建邮件对象
            message = MIMEMultipart()
            message['From'] = self.sender
            message['To'] = to_email
            message['Subject'] = Header(f'{self.appnameme} 验证码', 'utf-8')
            
            # 邮件正文内容
            html_content = f"""
            <div style="background-color:#f7f7f7;padding:20px;">
                <div style="max-width:600px;margin:0 auto;background-color:white;padding:20px;border-radius:5px;box-shadow:0 0 10px rgba(0,0,0,0.1);">
                    <h2 style="color:#333;text-align:center;">{self.appnameme} 验证码</h2>
                    <p>您好，</p>
                    <p>您的验证码是：</p>
                    <div style="text-align:center;margin:20px 0;">
                        <span style="font-size:24px;font-weight:bold;background-color:#f2f2f2;padding:10px 20px;border-radius:4px;letter-spacing:5px;">{verification_code}</span>
                    </div>
                    <p>验证码有效期为10分钟，请勿将验证码泄露给他人。</p>
                    <p>如果您没有请求此验证码，请忽略此邮件。</p>
                    <p style="color:#999;font-size:12px;margin-top:30px;text-align:center;">此邮件由系统自动发送，请勿回复</p>
                </div>
            </div>
            """
            
            message.attach(MIMEText(html_content, 'html', 'utf-8'))
            
            # 连接SMTP服务器并发送邮件
            with smtplib.SMTP_SSL(self.smtp_host, self.smtp_port) as server:
                server.login(self.smtp_user, self.smtp_pass)
                server.sendmail(self.smtp_user, to_email, message.as_string())
                
            print(f"验证码邮件已发送至 {to_email}")
            return True
            
        except Exception as e:
            print(f"发送邮件失败: {str(e)}")
            return False