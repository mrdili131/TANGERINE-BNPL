from django.shortcuts import render, redirect
from .models import *
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import ClientForm, UpdateClientForm
from django.db.models import Q
from django.utils import timezone
from datetime import datetime
from django.http import JsonResponse


class IndexView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'index.html')
    
class ContractView(LoginRequiredMixin,View):
    def get(self,request,contract_id):
        contract = Contract.objects.get(id=contract_id)
        return render(request,'contract.html',{"contract":contract})

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
    
class EditClientView(LoginRequiredMixin,View):
    def get(self,request,client_id):
        client = Client.objects.get(id=client_id)
        form = UpdateClientForm(instance=client)
        return render(request,'edit-client.html',{"client":client,"form":form})
    
    def post(self,request,client_id):
        client = Client.objects.get(id=client_id)
        form = UpdateClientForm(request.POST,instance=client)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.full_name = f"{form.cleaned_data["last_name"]} {form.cleaned_data["first_name"]} {form.cleaned_data["middle_name"]}"
            new_form.save()
            return redirect('client',id=client.id)
        return render(request,'edit-client.html',{"client":client,"form":form})
        



@login_required
def get_numbers(request,client_id):
    data = {}
    numbers = PhoneNumber.objects.filter(client_id=client_id).order_by('id')
    for i in numbers:
        data[i.id] = {
            "id":i.id,
            "number":i.number,
            "name":i.name,
        }
    return JsonResponse(data)

@login_required
def delete_number(request,id):
    try:
        number = PhoneNumber.objects.get(id=id)
        number.delete()
        return JsonResponse({"status":True})
    except:
        return JsonResponse({"status":False})

@login_required   
def add_number(request):
    if request.method == "POST":
        client_id = request.POST.get("client_id")
        name = request.POST.get("name")
        number = request.POST.get("number")
        if (client_id,name,number):
            try:
                phone_number = PhoneNumber(
                    client = Client.objects.get(id=client_id),
                    name = name,
                    number = number
                )
                phone_number.save()
                return JsonResponse({"status":True})
            except:
                return JsonResponse({"status":False})
        else:
            return JsonResponse({"status":False})
    return JsonResponse({"status":False})

@login_required
def create_contract(request,client_id):
    contract = Contract(client=Client.objects.get(id=client_id))
    contract.save()
    return redirect('contract',contract_id=contract.id)

