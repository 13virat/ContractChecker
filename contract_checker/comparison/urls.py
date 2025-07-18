from django.urls import path
from .views import compare_view, download_report, history_view, comparison_detail_view, home_view, smart_contract_analyzer_view

urlpatterns = [
    path('', home_view, name='home'),
    path('compare/', compare_view, name='compare'),
    path('history/', history_view, name='history'),
    path('comparison/<int:pk>/', comparison_detail_view, name='comparison_detail'),
    path('comparison/<int:pk>/download/', download_report, name='download_report'),
    path('smart-analyze/', smart_contract_analyzer_view, name='smart_analyze'),

    
]