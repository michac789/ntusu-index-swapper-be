from NTUSU_BE.utils import DO_NOT_REPLY_MESSAGE, send_email


def send_activation_token(email, token):
    # ACTIVATION_LINK = 'https://app.ntusu.org/sso/verify/'
    ACTIVATION_LINK = 'https://ntusu-itc-frontend-michac789.vercel.app/sso/verify/'
    ACTIVATION_EMAIL_SUBJECT = 'NTUSU Portal Activation Link'
    ACTIVATION_EMAIL_CONTENT = f'''
        Hi,
        <br><br>
        Thank you for registering to NTUSU Portal.
        <br>
        Please confirm your email address by clicking the link below.
        <br>
        <h2>
            <a href='{ACTIVATION_LINK}{token}/'>
                Validate Account
            </a>
        </h2>
        <p>
            If you never registered to NTUSU Portal, please ignore this email.
        </p>
        {DO_NOT_REPLY_MESSAGE}
    '''
    send_email(ACTIVATION_EMAIL_SUBJECT, ACTIVATION_EMAIL_CONTENT, [email])
