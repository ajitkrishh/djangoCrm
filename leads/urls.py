from django.urls import path
from .views import (LandingPageView,LeadListView,
                    LeadDetailView,LeadCreateView,
                    LeadUpdateView,LeadDeleteView,
                    AssignAgenttoLead,CategoryView,
                    CategoryDetailView
                    )
urlpatterns = [
    # path('all/', LandingPageView.as_view(), name = "home"),
    path('', LeadListView.as_view(), name = "lead-list"),
    path('<int:pk>/', LeadDetailView.as_view(), name = "lead-detail"),
    path('create/', LeadCreateView.as_view(), name = "lead-create"),
    path('category/', CategoryView.as_view(), name = "category-list"),
    path('category/<int:pk>', CategoryDetailView.as_view(), name = "category-detail"),
    # path('category/<int:pk>/update', LeadCategoryUpdate.as_view(), name = "category-update"),
    path('<int:pk>/update/', LeadUpdateView.as_view(), name = "lead-update"),
    path('<int:pk>/delete/', LeadDeleteView.as_view(), name = "lead-delete"),
    path('<int:pk>/assign-agent/', AssignAgenttoLead.as_view(), name = "assign_agent"),
]
