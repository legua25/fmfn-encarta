# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from apps.fmfn.forms import UserCreationForm, BasicEditForm, AdminEditForm, UserViewForm
from django.shortcuts import render_to_response, redirect, RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy
from apps.fmfn.decorators import role_required, ajax_required
from django.contrib.auth import get_user_model
from django.http import HttpResponseForbidden
from apps.fmfn.models import ActionLog
from django.views.decorators.cache import cache_page
from django.views.generic import View
from django.http import JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

__all__ = [
	'create',
	'edit'
]
User = get_user_model()

class CreateUserView(View):

	@method_decorator(login_required)
	@method_decorator(role_required('user manager'))
	def get(self, request):

		form = UserCreationForm()
		return render_to_response('users/create.html', context = RequestContext(request, locals()))
	@method_decorator(login_required)
	@method_decorator(role_required('user manager'))
	def post(self, request):

		# Create and validate the form
		form = UserCreationForm(request.POST, request.FILES)
		if form.is_valid():

			# Retrieve the user, set the password, and create him/her
			user, password = form.instance, form.cleaned_data['password']
			user.save()

			user.refresh_from_db()
			grades = form.cleaned_data['grades']

			user.grades = grades
			user.set_password(password)
			user.save()

			# Redirect to user list
			return redirect(reverse_lazy('users:list'))

		return render_to_response('users/create.html',
			context = RequestContext(request, locals()),
		    status = 401
		)

create = CreateUserView.as_view()

class EditUserView(View):
	"""
		Class responsible to handle user requests to edit user profiles:
			Receives the logged user request containing the target user profile id to edit.
				It evaluates if the user according to its role should be allowed or denied the edit to the target user profile
			Returns the target user profile edit form on success, 40X otherwise.
	"""
	@method_decorator(login_required)
	@method_decorator(role_required('teacher'))
	def get(self, request, user_id = 0):

		try: u = User.objects.active().get(id = user_id)
		except User.DoesNotExist:

			ActionLog.objects.log_account('Invalid user profile information request : (user_id: %s)' % user_id, user = request.user, status = 401)
			return HttpResponseForbidden()
		else:

			if request.user.belongs_to('user manager'): form = AdminEditForm(instance = u)
			else:

				if request.user.id == int(user_id): form = BasicEditForm(instance = u)
				else:

					ActionLog.objects.log_account('Attempted to view user profile information without enough privileges : (user_id: %s)' % user_id, user = request.user, status = 401)
					return HttpResponseForbidden()

		return render_to_response('users/edit.html', context = RequestContext(request, locals()))
	@method_decorator(csrf_protect)
	@method_decorator(login_required)
	@method_decorator(role_required('teacher'))
	def post(self, request, user_id = 0):

		try: u = User.objects.active().get(id = user_id)
		except User.DoesNotExist:

			ActionLog.objects.log_account('User requested to edit does not exist: (user_id: %s)' % user_id, user = request.user, status = 401)
			return HttpResponseForbidden()
		else:

			if request.user.belongs_to('user manager'): form = AdminEditForm(request.POST, request.FILES, instance = u)
			else:
				if request.user.id == int(user_id): form = BasicEditForm(request.POST, request.FILES, instance = u)
				else:

					ActionLog.objects.log_account(
						'Attempted to edit user profile information without enough privileges : (user_id: %s)' % user_id,
						user = request.user,
						status = 401
					)
					return HttpResponseForbidden()

		# Validate the form and, if valid, save the user
		if form.is_valid():

			user = form.instance
			ActionLog.objects.log_account('Edited user profile information (email address: %s)' % user.email_address, user = request.user)
			form.save(commit = True)

			return redirect(reverse_lazy('users:view', kwargs = { 'user_id': user.id }))

		# Log the error and resend the form
		ActionLog.objects.log_account('Attempted to edit user profile information with invalid detail(s) (email address: %s)' % u.email_address, user = request.user, status = 401)
		return render_to_response('users/edit.html', context = RequestContext(request, locals()))

	@method_decorator(ajax_required)
	@method_decorator(login_required)
	@method_decorator(csrf_protect)
	@method_decorator(role_required('user manager'))
	def delete(self, request, user_id = 0):

		#Fetch the user to delete
		try: u = User.objects.active().get(id = user_id)

		#It either does not exist or it is inactive
		except User.DoesNotExist:

			ActionLog.objects.log_account('Attempted to delete user account', user = request.user, status = 401)
			return HttpResponseForbidden()

		else:
			u.delete()
			ActionLog.objects.log_account('Deleted user account (email address: %s)' % u.email_address, user = request.user)

			return JsonResponse({
				'version': '1.0.0',
				'status': 200
			})

edit = EditUserView.as_view()

class ViewUserView(View):
	"""
		Class responsible to handle user requests inquiring about user profiles:
			Receives the logged user request containing the target user profile id to display.
				It evaluates if the user according to its role should be allowed or denied access to the target user profile
			Returns the target user profile view on success, 40X otherwise.
	"""
	@method_decorator(login_required)
	@method_decorator(role_required('teacher'))
	def get(self, request, user_id = 0):

		try: u = User.objects.get(id = user_id)
		except User.DoesNotExist:

			ActionLog.objects.log_account('Invalid user profile information request : (user_id: %s)' % user_id, user = request.user, status = 401)
			return HttpResponseForbidden()
		else:
			if request.user.belongs_to('user manager'): form = UserViewForm(instance = u)
			else:
				if request.user.id == int(user_id): form = UserViewForm(instance = u)
				else:
					ActionLog.objects.log_account('Attempted to view user profile information without enough privileges : (user_id: %s)' % user_id, user = request.user, status = 401)
					return HttpResponseForbidden()
		ActionLog.objects.log_account('Displayed user profile information (email address: %s)' % u.email_address, user = request.user)
		return render_to_response('users/view.html', context = RequestContext(request, locals()))


view = ViewUserView.as_view()

class SearchView(View):
	@method_decorator(login_required)
	@method_decorator(role_required('parent'))
	def get(self, request):
		users = User.objects.all()
		return render_to_response('users/list.html', context = RequestContext(request, locals()))

	# @method_decorator(login_required)
	# @method_decorator(ajax_required)
	# @method_decorator(role_required('parent'))
	# @method_decorator(cache_page(300))
	# def post(self, request):
	#
	# 	# Filter material based on query
	# 	query = User.objects.active()
	# 	filters = request.POST.get('filter', None)
	#
	# 	if bool(filters) is not False:
	#
	# 		# Preload related elements and perform matching queries against every one of them
	# 		params = Q(first_name__icontains = filters) | Q(father_family_name__icontains = filters) | Q(mother_family_name_icontains = filters)
	#
	# 		query = query.filter(params)
	#
	#
	# 	# Paginate the results and serialize the response
	# 	paginator = Paginator(query, request.GET.get('page_size', 25))
	# 	page = request.GET.get('page', 1)
	#
	# 	try: users = paginator.page(page)
	# 	except EmptyPage: users = paginator.page(paginator.num_pages)
	# 	except PageNotAnInteger: users = paginator.page(1)
	#
	# 	ActionLog.objects.log_content('Queried for users (filters: %s)' % filters, user = request.user, status = 302)
	# 	return JsonResponse({
	# 		'version': '1.0.0',
	# 		'status': 302,
	# 		'pages': {
	# 			'prev': users.previous_page_number() if users.has_previous() else None,
	# 			'next': users.next_page_number() if users.has_next() else None,
	# 			'current': page,
	# 			'total': paginator.num_pages,
	# 			'count': query.count(),
	# 			'page_size': paginator.per_page
	# 		},
	# 		'results': [ {
	# 			'id': u.id,
	# 			'name': u.name,
	# 			'father_family_name': u.father_family_name,
	# 			'mother_family_name': u.mother_family_name,
	# 			'email': u.email,
	# 			'campus': u.campus
	# 		} for u in users ]
	# 	})

search = SearchView.as_view()
