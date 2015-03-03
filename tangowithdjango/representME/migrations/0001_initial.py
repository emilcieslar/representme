# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateField()),
                ('text', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Constituency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('parent', models.ForeignKey(default=0, to='representME.Constituency', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Law',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=15)),
                ('text', models.TextField()),
                ('topic', models.CharField(max_length=128)),
                ('score', models.DecimalField(null=True, max_digits=5, decimal_places=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MSP',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('foreignid', models.PositiveIntegerField(unique=True, max_length=8)),
                ('firstname', models.CharField(max_length=128)),
                ('lastname', models.CharField(max_length=128)),
                ('img', models.CharField(max_length=256)),
                ('presence', models.DecimalField(null=True, max_digits=5, decimal_places=2)),
                ('score', models.DecimalField(null=True, max_digits=5, decimal_places=2)),
                ('constituency', models.ForeignKey(to='representME.Constituency')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MSPVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vote', models.CharField(max_length=1, null=True, choices=[(1, b'Yes'), (2, b'No'), (3, b'Abstain'), (4, b'Absent')])),
                ('law', models.ForeignKey(to='representME.Law')),
                ('msp', models.ForeignKey(to='representME.MSP')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Party',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('description', models.TextField()),
                ('colour', models.CharField(max_length=10, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('description', models.TextField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(unique=True, max_length=128)),
                ('password', models.CharField(unique=True, max_length=50)),
                ('postcode', models.CharField(max_length=8)),
                ('msptype', models.BooleanField(default=False)),
                ('email', models.CharField(max_length=128, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vote', models.CharField(max_length=1, null=True, choices=[(1, b'Yes'), (2, b'No'), (3, b'Abstain'), (4, b'Absent')])),
                ('law', models.ForeignKey(to='representME.Law')),
                ('user', models.ForeignKey(to='representME.User')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='msp',
            name='party',
            field=models.ForeignKey(to='representME.Party'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='law',
            field=models.ForeignKey(to='representME.Law'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(to='representME.User'),
            preserve_default=True,
        ),
    ]
