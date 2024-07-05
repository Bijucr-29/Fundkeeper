from django.urls import path

from api import views

from rest_framework.routers import DefaultRouter

from rest_framework.authtoken.views import ObtainAuthToken

router=DefaultRouter()

router.register("incomes",views.IncomeViewSet,basename="income")
router.register("expenses",views.ExpenseViewSet,basename="expense")

urlpatterns=[
        path("register/",views.UserCreationView.as_view()),
        path("income/summary/",views.IncomeSummaryView.as_view()),
        path('token/',ObtainAuthToken.as_view()),
        path('expense/summary/',views.ExpenseSummaryView.as_view())
        
] +router.urls