from django.shortcuts import render, HttpResponse
from django.views.generic import View


class UserViews(View):
    def get(self, request, *args, **kwargs):
        pass