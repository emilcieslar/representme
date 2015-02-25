from django.db import models

# Create your models here.

class Law(models.Model):
    name = models.CharField(max_length=15, unique=True)
    text = models.TextField()
    topic = models.CharField(max_length=128)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    def __unicode__(self):
        return self.name

class Topic(models.Model):
    """
    represents topic for a law
    """
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True)

    def __unicode__(self):
        return self.name


class Party(models.Model):
    """
    represents party
    """
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField()
    colour = models.CharField(max_length=10, null=True)

    def __unicode__(self):
        return self.name


class Constituency(models.Model):
    """
    represents a constituency
    """
    parent = models.ForeignKey('self', default=0, null=True)
    name = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return self.name

class User(models.Model):
    username = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=50, unique=True)
    postcode = models.CharField(max_length=8)
    msptype = models.BooleanField(default=False)
    email = models.CharField(max_length=128, null=True)

    def __unicode__(self):
        return self.username


class UserVote(models.Model):
    """
    represents an msp's vote for a division
    """
    YES = 1
    NO = 2
    ABSTAIN = 3
    ABSENT = 4
    VOTES = (
        (YES, 'Yes'),
        (NO, 'No'),
        (ABSTAIN, 'Abstain'),
        (ABSENT, 'Absent')
    )

    user = models.ForeignKey(User)
    law = models.ForeignKey(Law)
    vote = models.CharField(max_length=1, choices=VOTES, null=True)

    def __unicode__(self):
        return self.vote


class MSP(models.Model):
    """
    reprezents msps, stores presence, rebellions and status
    """

    foreignid = models.PositiveIntegerField(max_length=8, unique=True)
    constituency = models.ForeignKey(Constituency)
    party = models.ForeignKey(Party)
    firstname = models.CharField(max_length=128)
    lastname = models.CharField(max_length=128)
    img = models.CharField(max_length=256)
    presence = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    def __unicode__(self):
        return u'%s %s' % (self.firstname, self.lastname)


class MSPVote(models.Model):
    """
    represents an msp's vote for a division
    """
    YES = 1
    NO = 2
    ABSTAIN = 3
    ABSENT = 4
    VOTES = (
        (YES, 'Yes'),
        (NO, 'No'),
        (ABSTAIN, 'Abstain'),
        (ABSENT, 'Absent')
    )

    msp = models.ForeignKey(MSP)
    law = models.ForeignKey(Law)
    vote = models.CharField(max_length=1, choices=VOTES, null=True)

    def __unicode__(self):
        return self.vote

class Comment(models.Model):
    user = models.ForeignKey(User)
    law = models.ForeignKey(Law)
    time = models.DateField()
    text = models.TextField()

    def __unicode__(self):
        return self.title


