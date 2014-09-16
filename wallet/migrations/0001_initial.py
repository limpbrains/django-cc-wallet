# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cc', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProxyWallet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('wallet', models.ForeignKey(to='cc.Wallet')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
