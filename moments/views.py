from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse, JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from accounts.models import *
from .models import *
from .serializers import *
from rest_framework import generics

class MomentListAPI(generics.ListAPIView):
    """ 
    API endpoint for fetching all user feeds
    """
    queryset = Moment.objects.order_by('-id')
    serializer_class = MomentSerializer

class MomentView():
    @login_required
    def get(request):
        moments_obj = Moment.objects.all()
        context = {
            'page_title': "Moments",
            'user_profile': request.user,
            'moments': moments_obj,
        }
        return render(request, 'moments/content.html', context)
    
    @login_required
    def post(request, switch):
        if request.method == 'POST':
            images = request.FILES.getlist('moment_image')
            text = request.POST['moment_text']
            obj = Moment.objects.create(user=request.user, text=text)
            obj.save()
            for img in images:
                MomentImages.objects.create(moment=obj, image=img)
            moment = obj
            data = {
            'moment': moment,
            }
            if(switch == "i"):
                return render(request, 'moments/view/moment.html', data)
            return render(request, 'moments/moment.html', data)
        else:
            return JsonResponse({'scode': 403, 'message': 'Not Allowed'}, status=403)