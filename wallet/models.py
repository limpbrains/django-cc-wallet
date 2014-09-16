from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from cc.models import Wallet

class ProxyWallet(models.Model):
    user = models.ForeignKey(User)
    wallet = models.ForeignKey(Wallet)

    def get_absolute_url(self):
        return reverse('wallet_detail', kwargs={'pk': self.pk})
