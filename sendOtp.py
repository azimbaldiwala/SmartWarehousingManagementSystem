import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random


def sendOtp(receiver_email):
    otp = random.randint(1111, 9999)
    sender = 'smartwarehousingdfyproject@gmail.com'
    password = 'project@dfy'
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "OTP FROM SMART WAREHOUSING SYSTEM"
    msg['From'] = sender
    msg['To'] = receiver_email

    html1 = """<html> <head> <style> .banner-color { background-color: #eb681f; } .title-color { color: #0066cc; } 
    .button-color { background-color: #0066cc; } @media screen and (min-width: 500px) { .banner-color { 
    background-color: #0066cc; } .title-color { color: #eb681f; } .button-color { background-color: #eb681f; } } 
    </style> </head> <body> <div style="background-color:#ececec;padding:0;margin:0 
    auto;font-weight:200;width:100%!important"> <table align="center" border="0" cellspacing="0" cellpadding="0" 
    style="table-layout:fixed;font-weight:200;font-family:Helvetica,Arial,sans-serif" width="100%"> <tbody> <tr> <td 
    align="center"> <center style="width:100%"> <table bgcolor="#FFFFFF" border="0" cellspacing="0" cellpadding="0" 
    style="margin:0 auto;max-width:512px;font-weight:200;width:inherit;font-family:Helvetica,Arial,sans-serif" 
    width="512"> <tbody> <tr> <td bgcolor="#F3F3F3" width="100%" 
    style="background-color:#f3f3f3;padding:12px;border-bottom:1px solid #ececec"> <table border="0" cellspacing="0" 
    cellpadding="0" style="font-weight:200;width:100%!important;font-family:Helvetica,Arial,
    sans-serif;min-width:100%!important" width="100%"> <tbody> <tr> <td align="left" valign="middle" 
    width="50%"><span style="margin:0;color:#4c4c4c;white-space:normal;display:inline-block;text-decoration:none;font
    -size:12px;line-height:20px"></span></td> <td valign="middle" width="50%" align="right" style="padding:0 
    0 0 10px"><span style="margin:0;color:#4c4c4c;white-space:normal;display:inline-block;text-decoration:none;font
    -size:12px;line-height:20px"></span></td> <td width="1">&nbsp;</td> </tr> </tbody> 
    </table> </td> </tr> <tr> <td align="left"> <table border="0" cellspacing="0" cellpadding="0" 
    style="font-weight:200;font-family:Helvetica,Arial,sans-serif" width="100%"> <tbody> <tr> <td width="100%"> 
    <table border="0" cellspacing="0" cellpadding="0" style="font-weight:200;font-family:Helvetica,Arial,sans-serif" 
    width="100%"> <tbody> <tr> <td align="center" bgcolor="#8BC34A" style="padding:20px 48px;color:#ffffff" 
    class="banner-color"> <table border="0" cellspacing="0" cellpadding="0" 
    style="font-weight:200;font-family:Helvetica,Arial,sans-serif" width="100%"> <tbody> <tr> <td align="center" 
    width="100%"> <h1 style="padding:0;margin:0;color:#ffffff;font-weight:500;font-size:20px;line-height:24px">Smart 
    Warehouse</h1> </td> </tr> </tbody> </table> </td> </tr> <tr> <td align="center" style="padding:20px 0 10px 0"> 
    <table border="0" cellspacing="0" cellpadding="0" style="font-weight:200;font-family:Helvetica,Arial,sans-serif" 
    width="100%"> <tbody> <tr> <td align="center" width="100%" style="padding: 0 15px;text-align: justify;color: rgb(
    76, 76, 76);font-size: 12px;line-height: 18px;"> <h3 style="font-weight: 600; padding: 0px; margin: 0px; 
    font-size: 16px; line-height: 24px; text-align: center;" class="title-color">
    """
    html2 = f'Hi {receiver_email},'
    html3 = """
    </h3> <p style="margin: 20px 0 30px 0;font-size: 15px;text-align: center;">Please find you OTP here, 
    <b>
    """

    html4 = f'{otp}'

    html5 = """
    </b></p> </td> </tr> </tbody> </table> </td> </tr> <tr> </tr> <tr> </tr> </tbody> </table> </td> </tr> 
    </tbody> </table> </td> </tr> <tr> <td align="left"> <table bgcolor="#FFFFFF" border="0" cellspacing="0" 
    cellpadding="0" style="padding:0 24px;color:#999999;font-weight:200;font-family:Helvetica,Arial,sans-serif" 
    width="100%"> <tbody> <tr> <td align="center" width="100%"> <table border="0" cellspacing="0" cellpadding="0" 
    style="font-weight:200;font-family:Helvetica,Arial,sans-serif" width="100%"> <tbody> <tr> <td align="center" 
    valign="middle" width="100%" style="border-top:1px solid #d9d9d9;padding:12px 0px 20px 
    0px;text-align:center;color:#4c4c4c;font-weight:200;font-size:12px;line-height:18px">Regards, <br><b>The Awesome 
    Team</b> </td> </tr> </tbody> </table> </td> </tr> <tr> <td align="center" width="100%"> <table border="0" 
    cellspacing="0" cellpadding="0" style="font-weight:200;font-family:Helvetica,Arial,sans-serif" width="100%"> 
    <tbody> <tr> <td align="center" style="padding:0 0 8px 0" width="100%"></td> </tr> </tbody> </table> </td> </tr> 
    </tbody> </table> </td> </tr> </tbody> </table> </center> </td> </tr> </tbody> </table> </div> </body> </html> 
    """
    html = html1 + html2 + html3 + html4 + html5

    part2 = MIMEText(html, 'html')
    msg.attach(part2)
    # Send the message via local SMTP server.
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(sender, password)
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    server.sendmail(sender, receiver_email, msg.as_string())
    server.quit()
    return otp

#sendOtp('196330307005.azim.baldiwala@gmail.com')