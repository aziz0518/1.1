from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView




from django.http import HttpResponse

def home_view(request):
    return HttpResponse("Bosh sahifa! sizdi dasturingiz ishlayabdi")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/token/', TokenObtainPairView.as_view()),  # Faqat JWT login

    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('', home_view),  # Bosh sahifa uchun yo‘nalish
]

