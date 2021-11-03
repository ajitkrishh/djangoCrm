from django.urls import path
from .views import AgentListView,AgentCreateView,AgentDetailView,AgentUpdateView,AgentDeleteView

urlpatterns = [
    # path('all/', LandingPageView.as_view(), name = "home"),
    path('', AgentListView.as_view(), name = "agent-list"),
    path('<int:pk>/', AgentDetailView.as_view(), name = "agent-detail"),
    path('create/', AgentCreateView.as_view(), name = "agent-create"),
    path('<int:pk>/update/', AgentUpdateView.as_view(), name = "agent-update"),
    path('<int:pk>/delete/', AgentDeleteView.as_view(), name = "agent-delete"),
    
  
]
