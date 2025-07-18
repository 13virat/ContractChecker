from django.urls import path
from .views import compare_view, download_report, history_view, comparison_detail_view

urlpatterns = [
    path('', compare_view, name='compare'),
    path('history/', history_view, name='history'),
    path('comparison/<int:pk>/', comparison_detail_view, name='comparison_detail'),
    path('comparison/<int:pk>/download/', download_report, name='download_report'),
    
]