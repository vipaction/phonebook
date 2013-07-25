from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.forms.models import inlineformset_factory, modelformset_factory
from django.core.urlresolvers import reverse
from phones.models import Consumer, Phone, RecordForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


@login_required

def list(request):
    consumer_list = Consumer.objects.order_by('last_name')
    context = {'consumer_list': consumer_list}
    return render(request,'phones/list.html', context)

def only_view(request, id_record):
	consumer = get_object_or_404(Consumer, id=id_record)
	phones = Phone.objects.filter(consumer_id=id_record)
	context = {'consumer': consumer, 'phones': phones}
	return render(request,'phones/only_view.html', context)

def view_record(request, id_record):
	record = get_object_or_404(Consumer, id=id_record)
	if record.user_id != request.user.id:
		return only_view(request, id_record)
	name = RecordForm(instance=record)
	phone_formset = inlineformset_factory(Consumer, Phone, extra=1)
	if request.method == 'POST':
		formset = phone_formset(request.POST,instance=record)
		form = RecordForm(request.POST, instance=record)
		if request.POST.get('cancel') != 'cancel':
			if formset.is_valid() and form.is_valid():
				form.save()
				formset.save()
		return HttpResponseRedirect(reverse('list'))
	else:
		formset = phone_formset(instance=record)
	return render(request,'phones/view_record.html', {'formset': formset, 'title_record': record.all_names, 'name': name})

def new_record(request):
	name = RecordForm()
	phone_formset = inlineformset_factory(Consumer, Phone, extra=1, can_delete=False)
	if request.method == 'POST':
		form = 	RecordForm(request.POST)
		user_id=request.user.id
		formset = phone_formset(request.POST)
		if request.POST.get('cancel') != 'cancel':
			if formset.is_valid() and form.is_valid():
				cons=form.save(commit=False)
				cons.user_id=user_id
				cons.save()
				phones=phone_formset(request.POST, instance=Consumer.objects.get(id=cons.id))
				phones.save()
		return HttpResponseRedirect(reverse('list'))
	else:
		formset = phone_formset()
	return render(request,'phones/view_record.html', {'formset': formset, 'title_record': 'New record', 'name': name})

def delete_records(request):
	Consumer.objects.filter(id__in=request.POST.getlist('del'), user_id=request.user.id).delete()	
	return HttpResponseRedirect(reverse('list'))

def new_user(request):
	user_name=request.POST.get('username','')
	user_password=request.POST.get('password','')
	isset_user=User.objects.filter(username=user_name)
	if user_name != '' and user_password != '':		
		user=authenticate(username=user_name, password=user_password)
		if isset_user:			
			if user is not None:
				login(request, user)
			return HttpResponseRedirect(reverse('list'))
		new_user=User.objects.create_user(username=user_name, password=user_password)
		new_user.save()
		user=authenticate(username=user_name, password=user_password)
		login(request, user)
	return HttpResponseRedirect(reverse('list'))
