from django.views.generic import View
from django.shortcuts import render_to_response, RequestContext, redirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from apps.fmfn.models import Profile
from apps.fmfn.forms import ProfileForm

class EditProfileView(View):

	@method_decorator(login_required)
	def get(self, request, username = '', password = ''):

		form = ProfileForm(request.user)
		return render_to_response('edit_profile.html', context = RequestContext(request, locals()))

	@method_decorator(csrf_protect)
	def user(self, request, username = ''):

		Profile.objects.filter(username = username).update(**{
			'username': request.POST['username'],
			'email': request.POST['email'],
			'password': request.POST['password']
		})

		return redirect(reverse_lazy('view_profile', kwargs = { 'username': username }))

edit_profile = EditProfileView.as_view()