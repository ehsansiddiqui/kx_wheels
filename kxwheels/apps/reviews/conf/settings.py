from django.conf import settings

RECAPTCHA_PUBLIC_KEY = getattr(settings, 'RECAPTCHA_PUBLIC_KEY', '6LdLtMQSAAAAAMzOGkiFGuaaexpSLuagoqxoWZ1L')
RECAPTCHA_PRIVATE_KEY = getattr(settings, 'RECAPTCHA_PRIVATE_KEY', '6LdLtMQSAAAAADMrSTJ8f6ggN6ZEj_Sgw-UwI1RD')

RATING_CHOICES = (
    (1, 'Sucks'),
    (2, 'Meh'),
    (3, 'OK-ish blah blah blah'),
    (4, 'Good'),
    (5, 'Dope'),
)
BUY_AGAIN_CHOICES = (
    (0, 'Definitely'),
    (1, 'May Be'),
    (2, 'Not Likely'),
    (3, 'Not a Chance'),
)

RECOMMEND_CHOICES = (
    (0, 'Definitely'),
    (1, 'May Be'),
    (2, 'Not Likely'),
    (3, 'Not a Chance'),
)

IS_MODERATION_REQUIRED = True

FLAG_THRESHOLD = 10
