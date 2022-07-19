from django.conf import settings

class NonPositiveBalanceError(Exception):
    pass

class GatewayError(Exception):
    def __str__(self):
        return self.message

    def __init__(self, message=None, instance=None):
        self.message = "Unable to reach the payment gateway."

        from django.core.mail import EmailMessage
        from django.template import loader, Context

        subject = "Payment error at %s" % instance.site.name
        template = loader.get_template('remittance/gateway_error_email.txt')
        email_context = dict(domain=instance.site.domain,
                             url=instance.purchase.get_absolute_url())
        managers = ["%s <%s>" % (m[0], m[1]) for m in settings.MANAGERS]

        email = EmailMessage(
            subject=subject,
            body=template.render(Context(email_context,)),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[instance.purchase.buyer.email,],
            bcc=managers,
        )
        email.send(fail_silently=False)



class InvalidGatewayError(GatewayError):
    pass

class MissingConfigurationError(Exception):
    pass

