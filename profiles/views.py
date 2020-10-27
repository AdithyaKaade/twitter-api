from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse ,Http404, JsonResponse
from django.contrib.auth  import get_user_model
# Create your views here.
from .models import Profile
from .serializers import PublicSerializer
from rest_framework.response import Response 
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

User = get_user_model()

@api_view(['GET', 'POST'])
def profile_detail_api_view(request, username, *args, **kwargs):
    # get the profile for the passed username
    qs = Profile.objects.filter(user__username=username)
    if not qs.exists():
        return Response({"detail": "User not found"}, status=404)
    profile_obj = qs.first()
    data = request.data or {}
    if request.method == "POST":
        me = request.user
        action = data.get("action")
        if profile_obj.user != me:
            if action == "follow":
                profile_obj.followers.add(me)
            elif action == "unfollow":
                profile_obj.followers.remove(me)
            else:
                pass
    serializer = PublicSerializer(instance=profile_obj)#, context={"request": request})
    return Response(serializer.data, status=200)
