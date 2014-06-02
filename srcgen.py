import os

def make_template_file(lstclassnames):
	pass

def make_views_file(lstclassnames):
	retval = ''
	for iter in lstclassnames:
		retval = retval + '''\
def {0}_edit(request):
	form=forms.TransactionForm()
	return render(request, 'edit_{0}.html', locals())

def {0}_save(request):
	form=forms.TransactionForm(request.POST)
	if form.is_valid():
		form.save()
		return HttpResponseRedirect(reverse('list_{0}'))
	else:
		return render(request, 'edit_{0}.html', locals())
	
def {0}_list(request):
	return render(request, 'list_{0}.html', {{'data': models.{1}.objects.all()}})
	
def {0}_remove(request):
	pass
	\
'''.format(iter.lower(), iter)
	print(retval)

def make_urls_file(lstclassnames):
	retval = ''
	for iter in lstclassnames:
		retval = retval + 'url(r\'^{0}/edit$\', views.{0}_edit),'.format(iter.lower()) + os.linesep
		retval = retval + 'url(r\'^{0}/index$\', views.{0}_list),'.format(iter.lower()) + os.linesep
		retval = retval + 'url(r\'^{0}/delete$\', views.{0}_remove),'.format(iter.lower()) + os.linesep
		retval = retval + os.linesep
	print(retval)

def make_admin_file(lstclassnames):
	retval = '''\
from django.contrib import admin
from {0}.models import {1}

classes=[{1}]

for iterclass in classes:
	admin.site.register(iterclass)\
'''.format(
		os.path.dirname(os.path.realpath(__file__)).split(os.sep)[-1], #should we use os.getcwd instead of dirname of realpath?
		', '.join(lstclassnames)
	)
	print(retval)

import re

#matchobj = re.search(r'pat', 'str')
#print(matchobj.group(0))

#match looks only at the beginning of the string
#search is a proper search

cre = re.compile(r'class +(.*) *'+re.escape('('))
modelfile = open('models.py', 'r')
lstclassnames = []
for line in modelfile:
	cap = cre.match(line)
	if not cap is None:
		classname = cap.group(1)
		if not classname.endswith('Base'): #ignore base classes
			lstclassnames.append(classname)
if len(lstclassnames)>0:
	#make_urls_file(lstclassnames)
	make_views_file(lstclassnames)
	#make_admin_file(lstclassnames)
	pass
modelfile.close()