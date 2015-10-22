# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import redirect, render_to_response, RequestContext
from apps.fmfn.decorators import role_required, ajax_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as login_to_site
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy
from apps.fmfn.models import Material, ActionLog, Comment,Rating
from apps.fmfn.forms import MaterialForm
from apps.fmfn.decorators import role_required
from django.views.generic import View
from django.http import JsonResponse

__all__ = [ 'create']

class CreateCommentView(View):
    """ This view handles creation of Comments
    """

    """
        This method is called when the user posts a comment on a material detail view.
        It validates that the user has already rated such material and that the comment's length is lower than 500 chars
    """
    @method_decorator(login_required)
    @method_decorator(ajax_required)
    def post(self,request, material_id = 0,content = ''):
        user_id = request.user
        if len(Rating.objects.get(material_id = 1, user = user_id)) > 0:
            if len(content) < 500:
                ActionLog.objects.log_content('Registered new comment on material %s: %s' % (material_id, content),
                                              user = request.user, status = 200)
                Comment.objects.create(material=material_id,user = user_id, content = content)
                return JsonResponse({
                        'version': '1.0.0',
                        'status': 200,
                        'data': { 'content': content, 'user': user_id, 'material': material_id }
                    }, status = 200)
            ActionLog.objects.log_content('Failed to register comment on material %s' % material_id, user = user_id, status = 200)
            return JsonResponse({
                    'version': '1.0.0',
                    'status': 400
                }, status = 400)
        else:
            ActionLog.objects.log_content('Failed to register comment on material %s. The user has not rated this material.'
                                          % material_id, user = user_id, status = 200)
            return JsonResponse({
                    'version': '1.0.0',
                    'status': 400
                }, status = 400)
create = CreateCommentView.as_view()