import django.dispatch

transaction_complete = django.dispatch.Signal()
preauth_received = django.dispatch.Signal()
capture_received = django.dispatch.Signal()
