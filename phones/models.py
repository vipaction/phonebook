from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User


Phone_type = (
	('0', 'mobile'),
	('1', 'home'),
	)

class Consumer(models.Model):
	user = models.ForeignKey(User)
	first_name = models.CharField('First name', max_length=100)
	second_name = models.CharField('Second name', max_length=100, blank=True)
	last_name = models.CharField('Last name', max_length=100)
	def __unicode__(self):
		return self.all_names()
	def all_names(self):
		return u'%s %s %s' % (self.last_name, self.first_name, self.second_name)

class Phone(models.Model):

	consumer = models.ForeignKey(Consumer)
	number = models.CharField(max_length=15)
	type = models.CharField(max_length=1, choices=Phone_type)
	def __unicode__(self):
		return self.number

class RecordForm(ModelForm):
	class Meta:
		model = Consumer
		exclude = 'user'

