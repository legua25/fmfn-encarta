# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http.multipartparser import MultiValueDict
from django.http import QueryDict

class HttpMethodMiddleware(object):

	def process_request(self, request):

		request.PUT = QueryDict('')
		request.DELETE = QueryDict('')
		request.PATCH = QueryDict('')

		method = request.META.get('REQUEST_METHOD', '').upper()

		if method == 'PUT': HttpMethodMiddleware._handle_put_request(request)
		elif method == 'DELETE': HttpMethodMiddleware._handle_delete_request(request)
		elif method == 'PATCH': HttpMethodMiddleware._handle_patch_request(request)

	@staticmethod
	def _handle_patch_request(request): request.PATCH, request._files = HttpMethodMiddleware._parse_request(request)
	@staticmethod
	def _handle_put_request(request): request.PUT, request._files = HttpMethodMiddleware._parse_request(request)
	@staticmethod
	def _handle_delete_request(request): request.DELETE, request._files = HttpMethodMiddleware._parse_request(request)
	@staticmethod
	def _parse_request(request):

		if request.META.get('CONTENT_TYPE', '').startswith('multipart'): return request.parse_multipart_data(request.META, request)
		else: return [ QueryDict(request.body), MultiValueDict() ]
