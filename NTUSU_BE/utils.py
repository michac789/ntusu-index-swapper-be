from NTUSU_BE.settings import ses_client


DO_NOT_REPLY_MESSAGE = f'''
    <p style="color: red;">        
        This is a system generated email, please do <b>not</b> reply
        directly to this email. If you have any other enquiries regarding
        our IT services, please contact the mail su-itc@e.ntu.edu.sg
        (Student Union Information Technology Committee).
    </p>
'''


def send_email(subject, body, recipients: list, sender='do-not-reply@ntusu.org'):
    return ses_client.send_email(
        Source=sender,
        Destination={'ToAddresses': recipients},
        Message={
            'Subject': {
                'Data': subject,
            },
            'Body': {
                'Html': {
                    'Data': body,
                }
            },
        }
    )
