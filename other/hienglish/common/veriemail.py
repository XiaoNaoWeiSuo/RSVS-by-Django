import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(mail,code):
    smtp_server = "smtp-mail.outlook.com"#smtp服务器地址，本案例使用outlook邮箱
    port = 587#端口
    sender_email = ""#登录邮箱
    password = ""#登录密码
    receiver_email = mail
    verification_code = code
    # 创建邮件对象
    message = MIMEMultipart()
    message["From"] = f"ANT Fund <{sender_email}>"
    message["To"] = receiver_email
    message["Subject"] = "Your verification code"
    # 添加HTML格式的邮件正文
    body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
        <div style="max-width: 600px; margin: auto; background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
            <h1 style="color: #333333; text-align: center;">Verification Code</h1>
            <p style="font-size: 16px; color: #666666;">Hello,</p>
            <p style="font-size: 16px; color: #666666;">Your verification code is:</p>
            <p style="font-size: 36px; color: #333333; text-align: center; margin: 20px 0;"><strong>{verification_code}</strong></p>
            <p style="font-size: 16px; color: #666666;">Thank you for using our service.</p>
            <p style="font-size: 16px; color: #666666;">Best regards,<br>ANT Fund</p>
        </div>
    </body>
    </html>
    """
    message.attach(MIMEText(body, "html"))
    try:
        # 连接到SMTP服务器并发送邮件
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo('example.com')  # 使用有效的域名
            server.starttls()
            server.ehlo('example.com')  # 再次使用有效的域名
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        return "Email success."
        #print("Email sent successfully")
    except Exception as e:
        return "Email failed."
        # print(f"Failed to send email: {e}")

