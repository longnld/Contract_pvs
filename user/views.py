from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.urls import reverse_lazy

# Introduce single page view
def index(request):
    return render(request,"index.html")

# Login view
class LoginViewMix(LoginView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                if request.user.hnkstaff:
                    return redirect("hnk_ticket:hnk_daily_ticket")
            except:
                return redirect("user:admin_board")
        else:
            return self.render_to_response(self.get_context_data())

    def get_success_url(self):
        user = self.request.user
        try:
            if user.hnkstaff:
                return reverse_lazy("hnk_ticket:hnk_daily_ticket")
        except:
            pass

        try:
            if user.customer:
                return reverse_lazy("user:admin_board")
        except:
            pass
        


# Admin Board
def admin_board(request):
    menu_home = "true"
    return render(request,"user/admin-board.html",{"user":request.user,"menu_home":menu_home})



# setting customer
def settings_customer(request):

    menu_account = "true"
    return render(request,"user/settings-customer.html",{"user":request.user,"menu_account":menu_account})


    