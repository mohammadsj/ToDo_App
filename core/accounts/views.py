from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth import login
from django.contrib import messages
from .forms import UserCreationForm

# Create your views here.


class LoginView(LoginView):
    template_name = "accounts/login.html"
    fields = "username", "password"
    redirect_authenticated_user = True

    def get_success_url(self):
        messages.success(self.request, f"Hi {self.request.user.username} Logged in")

        return reverse_lazy("todo:TaskListView")

    def form_invalid(self, form):
        # error message
        context = self.get_context_data(form=form)
        context["error_message"] = "The username or password is incorrect"
        return self.render_to_response(context)


class SignUpView(FormView):

    template_name = "accounts/signup.html"
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("todo:TaskListView")

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
            messages.success(
                self.request, f"Hi {self.request.user.username} Welcome to my site"
            )
        return super(SignUpView, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("task_list")
        return super(SignUpView, self).get(*args, **kwargs)

    def form_invalid(self, form):
        # error handling
        context = self.get_context_data(form=form)
        context["error_messages"] = form.errors
        return self.render_to_response(context)
