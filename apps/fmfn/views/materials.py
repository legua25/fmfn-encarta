# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import redirect, render_to_response, RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as login_to_site
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy
from apps.fmfn.models import Material, ActionLog, Comment
from apps.fmfn.forms import MaterialForm
from apps.fmfn.decorators import role_required, ajax_required
from django.views.generic import View
from django.http import JsonResponse
from django.http import HttpResponseBadRequest

__all__ = [ 'create', 'edit','view' ]

class CreateMaterialView(View):
    """ This view handles list, create, read, update and delete operations on Materials
    """

    @method_decorator(login_required)
    @method_decorator(role_required('content manager'))
    def get(self, request):

        form = MaterialForm(initial = { 'user': request.user })
        return render_to_response('materials/create.html', context = RequestContext(request, locals()))

    @method_decorator(login_required)
    @method_decorator(role_required('content manager'))
    @method_decorator(csrf_protect)
    def post(self, request):

        form = MaterialForm(request.POST, request.FILES, initial = { 'user': request.user })

        if form.is_valid():

            material = form.instance
            form.save()
            ActionLog.objects.log_content('Registered new material entry (id: %s)' % material.id, user = request.user, status = 201)
            return redirect(reverse_lazy('content:view', kwargs = { 'content_id': material.id }))

        ActionLog.objects.log_content('Failed to register new material entry', user = request.user, status = 401)

        return render_to_response('materials/create.html',
            context = RequestContext(request, locals()),
            status = 401
        )

create = CreateMaterialView.as_view()

class EditMaterialView(View):

    @method_decorator(login_required)
    @method_decorator(role_required('content manager'))
    def get(self, request, content_id = 0):
        material = Material.objects.get(id = content_id)
        form = MaterialForm(instance = material, initial = {'user': request.user })

        return render_to_response('materials/edit.html', context = RequestContext(request, locals()))

    @method_decorator(login_required)
    @method_decorator(role_required('content manager'))
    @method_decorator(csrf_protect)
    def post(self, request, content_id = 0):

        material = Material.objects.get(id = content_id)
        form = MaterialForm(request.POST, request.FILES,
            instance = material,
            initial = { 'user': request.user }
        )
        #TODO: prepopulate form (checkboxes)
        if form.is_valid():

            material = form.instance
            form.save()
            ActionLog.objects.log_content('Edited material entry (id: %s)' % content_id, user = request.user, status = 200)

            return redirect(reverse_lazy('content:view', kwargs = { 'content_id': material.id }))

        ActionLog.objects.log_content('Attempted to edit material entry (id: %s)' % content_id, user = request.user, status = 401)
        return render_to_response('materials/edit.html', context = RequestContext(request, locals()))

    @method_decorator(login_required)
    @method_decorator(role_required('content manager'))
    @method_decorator(csrf_protect)
    def delete(self, request, content_id = 0):

        material = Material.objects.get(id = content_id)

        ActionLog.objects.log_content('Deleted material (id: %s)' % material.id, status = 200, user = request.user)
        material.delete()

        return JsonResponse(data = {
            'version': '1.0.0',
            'status': 200,
            'material': { 'id': material.id, 'status': 'delete' }
        }, content_type = 'application/json')

edit = EditMaterialView.as_view()

class MaterialDetailView(View):

    @method_decorator(login_required)
    def get(self, request, content_id = 0):
        material = Material.objects.get(id=content_id)
        #TODO: redirect to error page if material is null
        ActionLog.objects.log_content('Viewed material (id: %s)' % material.id, status = 200, user = request.user)
        return render_to_response('materials/detail.html', context = RequestContext(request, locals()))


    @method_decorator(login_required)
    @method_decorator(ajax_required)
    @method_decorator(role_required('teacher'))
    def post(self,request, content_id = 0):
        form = request.POST
        user_id = request.user
        if form['content'] is not None and len(form['content']) <= 500 and form['rating_value'] is not None:
            ActionLog.objects.log_content('Registered new comment on material %s: %s' % (content_id, form['content']),
                                          user = request.user, status = 200)
            comm = Comment.objects.create(material=content_id,user = user_id, content = form['content'],rating_value = form['rating_value'])
            return JsonResponse({
                    'version': '1.0.0',
                    'status': 200,
                    'data':{'content':comm.content,'time':comm.date_created}
                }, status = 200)

        ActionLog.objects.log_content('Failed to register comment on material %s' % content_id, user = user_id, status = 400)
        return HttpResponseBadRequest()

view = MaterialDetailView.as_view()