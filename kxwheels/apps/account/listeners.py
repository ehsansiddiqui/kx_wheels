from django.db.models import signals
from kxwheels.apps.account.models import Profile
from kxwheels.apps.account import signals as account_signals

def check_profile_existence(sender, instance, **kwargs):
    #print "You don't seem to have a profile. Would you like to create one?"
    pass

def set_preferred_profile(sender, insprtance, **kwargs):
    """docstring for set_preferred_profile"""
    profile = instance
    if not profile.is_preferred_profile:
        return True
    
    other_profiles = Profile.objects.filter(user=profile.user).exclude(name=profile.name)
    for profile in other_profiles:
        profile.is_preferred_profile = False
        profile.save()
        
    return True    

def start_listening():
    """Add required listeners"""
    account_signals.user_authenticated.connect(check_profile_existence)
    #signals.post_save.connect(set_preferred_profile, sender=Profile)
