# -*- coding: utf-8 -*-


from datetime     import datetime
from dateutil     import rrule
from django.db    import models
from django.utils import timezone

from client.functions import normalize_time

from django.utils.translation import ugettext_lazy as _

class Schedule(models.Model):    
    destination    = models.ForeignKey('Destination', null=True)
    schedule_time  = models.DateTimeField(verbose_name=_("initial datetime"))
    rule           = models.ForeignKey('RRule',
                                       null=True,
                                       blank=True,
                                       verbose_name=_("rule"),
                                       help_text=_("Selecione '----' para um evento nao recorrente."))
    active         = models.BooleanField(default=True, verbose_name=_("active"))
    
    class Meta:
        app_label = 'client'
    
    def __unicode__(self):
        return u"%(destination_name)s%(rule)s@ %(schedule_time)s" % {
            'destination_name': self.destination.name,
            'rule': u' (%s) ' % self.rule if self.rule else ' ',
            'schedule_time':
                datetime.strftime(timezone.localtime(self.schedule_time),
                    '%H:%M' if self.rule else '%d/%m/%Y %H:%M')
        }
    
    def save(self, *args, **kwargs):
        self.schedule_time = normalize_time(self.schedule_time)
        return super(Schedule, self).save(*args, **kwargs)
    
    def last_run(self):
        return self.last_before(timezone.now())
    
    def next_run(self):
        return self.next_after(timezone.now())
    
    def last_before(self, dt):
        if self.rule is not None:
            return self.get_rule().before(normalize_time(dt), True)
        else:
            if self.schedule_time <= dt:
                return self.schedule_time
            else:
                return None
            
    def next_after(self, dt):
        print self.rule
        if self.rule is not None:
            return self.get_rule().after(normalize_time(dt), False)
        else:
            if self.schedule_time > dt:
                return self.schedule_time
            else:
                return None
    
    def trigger(self, dt):
        last_before = self.last_before(dt)
        if last_before is None:
            return False
        #return normalize_time(dt) == last_before
        return normalize_time(dt) >= last_before
    
    
    def get_rule(self):
        if self.rule is not None:
            p = {
                'dtstart' : self.schedule_time,
                'byhour'  : self.schedule_time.hour,
                'byminute': self.schedule_time.minute,
            }
            params = self.rule.get_params()
            params.update(p)
            frequency = 'rrule.%s' % self.rule.frequency
            return rrule.rrule(eval(frequency), **params)