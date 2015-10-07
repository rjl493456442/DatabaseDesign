#-*-coding:UTF-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
from Category import *
from django.contrib.auth.models import User
class Nationality(models.Model):
    Country = models.CharField(max_length = 2,
                               choices = NATIONALITIES,
                               default = 'CN')
    def __unicode__(self):
        return self.Country
class Province(models.Model):
    Province = models.CharField(max_length = 2,
                               choices = Province_Category,
                               default = 'zj')
    def __unicode__(self):
        return self.Province
class Person(models.Model):
    user = models.OneToOneField(User, primary_key = True, related_name = 'p_user')
    nationality = models.ForeignKey(Nationality, related_name = 'p_nationality')
    province = models.ForeignKey(Province, related_name = 'p_province')
    name = models.CharField(max_length = 100)
    sex = models.IntegerField(choices = Sex_Category, default = 0)
    age = models.IntegerField()
    height = models.IntegerField()
    weight = models.IntegerField()
    category = models.IntegerField(choices = PersonCategory,default = 0)
    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
        return "/userprofile/%s/" % self.user.username
class Athlete(Person):
    level = models.IntegerField(choices = Level_Judge, default  = 0)
    n_gold = models.IntegerField(default = 0)
    n_silver = models.IntegerField(default = 0)
    n_bronze = models.IntegerField(default = 0)
    def __unicode__(self):
        return self.name
class Judge(Person):
    level = models.IntegerField(choices = Level_Judge, default  = 0)
    def __unicode__(self):
        return self.name
class Event(models.Model):
    event_name = models.CharField(max_length = 100)
    event_category = models.IntegerField(choices = Event_Category)
    best_grade = models.FloatField(null =  True, blank = True)
    def __unicode__(self):
        return u"%s" % self.event_name
class Competition(models.Model):
    name = models.CharField(max_length = 100)
    level = models.IntegerField(choices = Competition_Level)
    internal = models.BooleanField()
    def __unicode__(self):
        return self.name
class CompetitionEvent(Event):
    competiton = models.ForeignKey(Competition, related_name = 'CE_competition')
    major_judge = models.ForeignKey(Judge, related_name = 'CE_majorJudge',null = True, blank = True)
    second_judge = models.ForeignKey(Judge, related_name = 'CE_secondJudge', null = True, blank = True)
    third_judge = models.ForeignKey(Judge, related_name = 'CE_thirdJudge', null = True, blank = True)
    date = models.DateTimeField()
    level = models.IntegerField(choices = Event_Level)
    status = models.IntegerField(choices = EventStatus,default = 0)
    com_grade = models.FloatField(null = True, blank = True)
    def __unicode__(self):
        level_str = ''
        for key,val in Event_Level:
            if key == self.level:
                    level_str = val
        return u"%s-%s-%s" % (self.competiton.name, self.event_name, level_str)
    def get_absolute_url(self):
        return "/event/%s" % self.id
class Attend(models.Model):
    athlete = models.ForeignKey(Athlete, related_name = 'a_athlete')
    event = models.ForeignKey(CompetitionEvent, related_name = 'a_event')
    isAll = models.BooleanField()
    grade = models.FloatField(blank = True, null = True)
    rank = models.IntegerField(blank = True, null = True)
    status = models.IntegerField(choices = EventStatus, default = 0)
    # 0 before 1 ing 2 finish
    def __unicode__(self):
        return u"%s-%s" % (self.athlete.name,self.event.__unicode__())
# relationship of Event and Competition
class E_C(models.Model):
    event = models.ForeignKey(Event, related_name = 'ec_event')
    competition = models.ForeignKey(Competition, related_name = 'ec_competition')
    best_grade = models.FloatField()
    def __unicode__(self):
        return u'%s-%s' % (self.event.__unicode__(), self.competition.name)
class Leader(Person):
    level = models.IntegerField(choices = Level_Judge)
    def __unicode__(self):
        return self.name
    # todo
class Team(models.Model):
    nationality = models.ForeignKey(Nationality, related_name = 't_nationality')
    province = models.ForeignKey(Province, related_name = 't_province')
    leader = models.ForeignKey(Leader, related_name = 't_leader',null = True ,blank = True)
    n_gold = models.IntegerField(default = 0)
    n_silver = models.IntegerField(default = 0)
    n_bronze = models.IntegerField(default = 0)
    def __unicode__(self):
        return u"%s-%s" % (self.nationality.__unicode__(), self.province.__unicode__())
    def get_absolute_url(self):
        return "/team/%s" % self.id
    def __cmp__(self,other):
        if self.n_gold != other.n_gold:
            return self.n_gold.__cmp__(other.n_gold)
        elif self.n_silver != other.n_silver:
            return self.n_silver.__cmp__(other.n_silver)
        else:
            return self.n_bronze.__cmp__(other.n_bronze)
class AthleteTeam(models.Model):
    team = models.ForeignKey(Team, related_name = 'at_team')
    athlete = models.ForeignKey(Athlete, related_name = 'at_athlete')
    def __unicode__(self):
        return u"%s-%s" % (self.team, self.athlete.name)
class PersonHistory(models.Model):
    athlete = models.ForeignKey(Athlete, related_name = 'ph_athlete')
    event = models.ForeignKey(Event, related_name = 'ph_event')
    attendtime = models.IntegerField(default = 0)
    personalBest = models.FloatField()
    metalCount = models.IntegerField(default = 0)
    goalCount = models.IntegerField(default = 0)
    def __unicode__(self):
        return u"%s-%s" % (self.athlete.name, self.event.__unicode__())
