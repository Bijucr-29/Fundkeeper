 def get(self,request,*args,**kwargs):

        form_instance=SummaryForm()

        current_month=timezone.now().month

        current_year=timezone.now().year

        expense_list=Expense.objects.filter(created_date_month=current_month,created_date_year=current_year,user_object=request.user)

        income_list=Income.objects.filter(created_date_month=current_month,created_date_year=current_year,user_object=request.user)

        # print(expense_list,income_list)

        expense_total=expense_list.values("amount").aggregate(total=Sum("amount"))

        income_total=income_list.values("amount").aggregate(total=Sum("amount"))

        print(expense_total,income_total)

        monthly_expenses={}

        monthly_incomes={}

        for month in range(1,13):

            start_date=datetime.date(current_year,month,1)
            if month==12:

                end_date=datetime.date(current_year+1,1,1)

            else:
              
                end_date=datetime.date(current_year,month+1,1)

            monthly_expense_total=Expense.objects.filter(user_object=request.user,created_date_gte=start_date,created_date_lte=end_date).aggregate(total=Sum('amount'))["total"]
            
            monthly_expenses[start_date.strftime('%B')]=monthly_expense_total if monthly_expense_total else 0

            monthly_income_total=Income.objects.filter(user_object=request.user,created_date_gte=start_date,created_date_lte=end_date).aggregate(total=Sum('amount'))["total"]
            
            monthly_incomes[start_date.strftime('%B')]=monthly_income_total if monthly_income_total else 0


        print("monthly expense: ",monthly_expenses,"monthly income: ",monthly_incomes)    
        

        return render(request,"dashboard.html",{"expense":expense_total,"income":income_total,"form":form_instance,"monthly_incomes":monthly_incomes,"monthly_expenses":monthly_expenses})    



     def post(self,request,*args,**kwargs): 

        form_instance=SummaryForm(request.POST)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            start_date=data.get("start_date")

            end_date=data.get("end_date")

            expense_list=Expense.objects.filter(user_object=request.user,created_date_gte=start_date,created_date_lte=end_date)

            income_list=Income.objects.filter(user_object=request.user,created_date_gte=start_date,created_date_lte=end_date)

             # print(expense_list,income_list)

            expense_total=expense_list.values("amount").aggregate(total=Sum("amount"))

            income_total=income_list.values("amount").aggregate(total=Sum("amount"))

            # print(expense_total,income_total)

            return render(request,"dashboard.html",{"expense":expense_total,"income":income_total,"form":form_instance})
