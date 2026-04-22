from django.shortcuts import render, redirect
from .models import *
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ClientForm
from django.db.models import Q
from django.utils import timezone
from datetime import datetime
from django.http import JsonResponse


class IndexView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'index.html')
    
class ContractsView(LoginRequiredMixin,View):
    def get(self,request):
        start_date = request.GET.get('start_date', '')
        end_date = request.GET.get('end_date', '')
        status = request.GET.get('status' ,'')
        pinfl = request.GET.get('pinfl' ,'')

        try:
            start_date_valid = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date_valid = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            start_date_valid = timezone.now().date()
            end_date_valid = timezone.now().date()

        print(start_date_valid,end_date_valid)

        contracts = Contract.objects.filter(
            Q(client__passport_pinfl__icontains=pinfl)
        )
        contracts = contracts.filter(
            date__gte=start_date_valid,
            date__lte = end_date_valid
        )
        return render(request,'contracts.html',{"contracts":contracts,"start_date":start_date_valid,"end_date":end_date_valid,"pinfl":pinfl})
    

class AllClientsView(LoginRequiredMixin,View):
    def get(self,request):
        clients = Client.objects.all()
        query = request.GET.get('pinfl','')
        clients = clients.filter(
            Q(passport_pinfl__icontains=query)
        )
        return render(request,'clients.html',{"clients":clients,"query":query})
    

class AddClientView(LoginRequiredMixin,View):
    def get(self,request):
        form = ClientForm()
        return render(request,'add-client.html',{"form":form})
    
    def post(self,request):
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save()
            return redirect('client',id=client.id)
        else:
            return render(request,'add-client.html',{"form":form,"msg":"Ma‘lumotlarda xatolik"})

class ClientView(LoginRequiredMixin,View):
    def get(self,request,id):
        client = Client.objects.get(id=id)
        return render(request,'client.html',{"client":client})    



def get_numbers(request,client_id):
    numbers = PhoneNumber.objects.filter(client_id=client_id)
    return JsonResponse(numbers.data(),safe=False)