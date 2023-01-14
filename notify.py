import smtplib, ssl

def sendEmail(destEmail, message):
#     Format for message =>
#     message = """\
# Subject: Insurance Plan Updated

# This message is sent from CureNsure."""
    try:
        port = 587  # For SSL
        password ='Project=$'
        smtp_server="smtp-mail.outlook.com"
        sender_email="curensure@hotmail.com"
        
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls(context=context)
            server.login(sender_email, password)
            context = ssl.create_default_context()
            server.sendmail(sender_email, destEmail, message)
    except Exception as e: 
        return f'Exception {e} occured while sending the email', 401