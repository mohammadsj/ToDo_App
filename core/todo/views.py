from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView , CreateView , DeleteView
from .models import Task
from django.views import View
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.



class TaskListView(LoginRequiredMixin,ListView):
    model = Task
    context_object_name = 'tasks'
    template_name='todo/task_form.html'
    ordering = '-updated_date'
    
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    
    
class TaskCreate(LoginRequiredMixin, CreateView):
    
    model= Task
    fields = ["title"]
    success_url= reverse_lazy("todo:TaskListView")
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate,self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # اضافه کردن لیست تمام تسک‌ها به context
        context['tasks'] = Task.objects.filter(user=self.request.user).order_by('-updated_date')
        return context
    
    
    
class TaskComplete(LoginRequiredMixin,View):
    model = Task
    success_url = reverse_lazy("todo:TaskListView")

    def get(self, request, *args, **kwargs):
        object = Task.objects.get(id=kwargs.get("pk"))
        object.complete = True
        object.save()
        return redirect(self.success_url)
    
    
class ReturnTaskComplete(LoginRequiredMixin, View):
    model = Task
    success_url = reverse_lazy("todo:TaskListView")

    def get(self, request, *args, **kwargs):
        object = Task.objects.get(id=kwargs.get("pk"))
        object.complete = False
        object.save()
        return redirect(self.success_url)
    
    
class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    fields = ["title"]
    success_url = reverse_lazy("todo:TaskListView")
    template_name= "todo/TaskUpdate.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # اضافه کردن لیست تمام تسک‌ها به context
        context['tasks'] = Task.objects.filter(user=self.request.user).order_by('-updated_date')
        return context


class TaskDelete(LoginRequiredMixin,DeleteView):
    model = Task
    context_object_name = "task" 
    success_url = reverse_lazy("todo:TaskListView")
     
    def get(self, request, *args, **kwargs):
        task = get_object_or_404(Task, id=kwargs.get('pk'))
        task.delete()
        return redirect('todo:TaskListView')

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)