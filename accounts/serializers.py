from rest_framework.serializers import ModelSerializer
from .models import Profile

class ProfileSerializer(ModelSerializer):
    class Meta:
        Model = Profile
        fields =  ("id", "user", "plans")