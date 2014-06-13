import os

def make_template_file(lstclassnames):
	pass

def make_forms_file(lstclassnames):
	retval = '''\
from django.forms import ModelForm
from {0}.models import {1}

class BaseForm(ModelForm):
	required_css_class='required'
	class Meta:
		abstract=True

'''.format(
		os.path.dirname(os.path.realpath(__file__)).split(os.sep)[-1], #should we use os.getcwd instead of dirname of realpath?
		', '.join(lstclassnames)
	)
	for iter in lstclassnames:
		retval = retval + '''\
class {0}Form(BaseForm):
	class Meta:
		model={0}

'''.format(iter)
	return retval

def make_views_file(lstclassnames):
	retval = '''
from django.http import HttpResponse, HttpResponseRedirect
from {0}.forms import {2}
from {0}.models import {1}
from django.shortcuts import render
from django.core.urlresolvers import reverse

def home(request):
	return HttpResponse('Home page under construction', mimetype='text/plain')

'''.format(
		os.path.dirname(os.path.realpath(__file__)).split(os.sep)[-1],
		', '.join(lstclassnames),
		'Form, '.join(lstclassnames)
	)
	for iter in lstclassnames:
		retval = retval + '''\
def {0}_edit(request):
	form=forms.{1}Form()
	return render(request, 'edit_{0}.html', locals())

def {0}_save(request):
	form=forms.{1}Form(request.POST)
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
	return retval

def make_urls_file(lstclassnames):
	retval = ''
	retval = retval + 'from {0} import views'.format(
		os.path.dirname(os.path.realpath(__file__)).split(os.sep)[-1]
	) + os.linesep
	retval = retval + '''\
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
'''
	for iter in lstclassnames:
		retval = retval + 'url(r\'^{0}/edit$\', views.{0}_edit),'.format(iter.lower()) + os.linesep
		retval = retval + 'url(r\'^{0}/index$\', views.{0}_list),'.format(iter.lower()) + os.linesep
		retval = retval + 'url(r\'^{0}/delete$\', views.{0}_remove),'.format(iter.lower()) + os.linesep
		retval = retval + os.linesep
	retval = retval + ')'
	return retval

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
	return retval

import re

#matchobj = re.search(r'pat', 'str')
#print(matchobj.group(0))

#match looks only at the beginning of the string
#search is a proper search

def writetofile(filename, content):
	f=open(filename, 'w')
	f.write(content)
	f.close()

def generate_code(modelsfile='models.py', viewsfile=None, urlsfile=None, adminfile=None, formsfile=None):
	cre = re.compile(r'class +(.*) *'+re.escape('('))
	modelsfile = open(modelsfile, 'r')
	lstclassnames = []
	for line in modelsfile:
		cap = cre.match(line)
		if not cap is None:
			classname = cap.group(1)
			if not classname.endswith('Base'): #ignore base classes
				lstclassnames.append(classname)
	if len(lstclassnames)>0:
		if not urlsfile is None:
			writetofile(urlsfile, make_urls_file(lstclassnames))
		if not viewsfile is None:
			writetofile(viewsfile, make_views_file(lstclassnames))
		if not adminfile is None:
			writetofile(adminfile, make_admin_file(lstclassnames))
		if not formsfile is None:
			writetofile(formsfile, make_forms_file(lstclassnames))
		pass
	modelsfile.close()

if __name__=='__main__':
	generate_code('models.py', 'views.py', 'urls.py', 'admin.py')