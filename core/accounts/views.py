from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth import login
from django.contrib import messages
<<<<<<< Updated upstream
=======
from .forms import CustomSignupForm

>>>>>>> Stashed changes
# Create your views here.


class LoginView(LoginView):
<<<<<<< Updated upstream
    template_name = 'accounts/login.html'
    fields = "username","password"
=======
    fields = "username", "password"
>>>>>>> Stashed changes
    redirect_authenticated_user = True

    def get_success_url(self):
        messages.success(
            self.request, f"Hi {self.request.user.username} Logged in"
        )

        return reverse_lazy("todo:TaskListView")

    def form_invalid(self, form):
        # error message
        context = self.get_context_data(form=form)
        context["error_message"] = "The username or password is incorrect"
        return self.render_to_response(context)


class SignUpView(FormView):
<<<<<<< Updated upstream
    
    template_name = 'accounts/signup.html'
    form_class = UserCreationForm
=======

    template_name = "registration/signup.html"
    form_class = CustomSignupForm
>>>>>>> Stashed changes
    redirect_authenticated_user = True
    success_url = reverse_lazy("todo:TaskListView")

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
<<<<<<< Updated upstream
            messages.success(self.request, f'Hi {self.request.user.username} Welcome to my site')
        return super(SignUpView,self).form_valid(form)
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("task_list")
        return super(SignUpView, self).get(*args, **kwargs)    
=======
            messages.success(
                self.request,
                f"Hi {self.request.user.username} A code containing a recovery link has been sent to your email. Please verify your account first.",
            )
        return super(SignUpView, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("todo:TaskListView")
        return super(SignUpView, self).get(*args, **kwargs)

>>>>>>> Stashed changes
    def form_invalid(self, form):
        # error handling
        context = self.get_context_data(form=form)
        context["error_messages"] = form.errors
        return self.render_to_response(context)
