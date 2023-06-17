from NTUSU_BE.settings import ses_client


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
