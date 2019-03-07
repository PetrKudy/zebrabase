from django.shortcuts import render
from management.models import Room,Rack,Position,Substock,Stock,Fishline
from management.forms import DetailFishForm
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db import connection
from django import forms
from django.http import HttpResponseRedirect



class Index(TemplateView):
    template_name = 'index.html'

class RoomView(ListView):
    template_name = 'rooms.html'
    model = Room
    context_object_name = 'rooms'

class AddRoomView(CreateView):
    template_name = 'room_add.html'
    model = Room
    fields = ['number','description']
    success_url = './'

class UpdateRoomView(UpdateView):
    template_name = 'room_update.html'
    model = Room
    fields = ['number','description']
    success_url = '../'

class DeleteRoomView(DeleteView):
    template_name = 'room_delete.html'
    model = Room
    success_url = '../'

    def delete(self, request, *args, **kwargs):
        data= Room.objects.filter(id=self.kwargs['pk'])
        data.delete()
        return HttpResponseRedirect("/rooms")

class SelectRackView(TemplateView):
    template_name = 'selectrack.html'

    def get(self, request, *args, **kwargs):
        rack = Rack.objects.filter(room_id=self.kwargs['pk'])
        return render(self.request,self.template_name,{'res': rack,
                                                        'room_id' : self.kwargs['pk']})

class RackView(TemplateView):
    template_name = 'rack.html'

    def get(self, request, *args, **kwargs):
        rack_lenght = Rack.objects.filter(id=kwargs['pk'])
        positions = Position.objects.filter(rack_id = kwargs['pk'])
        return render(self.request,self.template_name,{'res': rack_lenght,
                                                       'pos': positions,
                                                       'rack_pk':self.kwargs['pk']})

class AddRackView(CreateView):
    template_name = 'rack_add.html'
    model = Rack
    fields = ['name','column_max','row_max']
    def form_valid(self,form):
        data = form.cleaned_data
        rack_add =Rack(row_max = data['row_max'],
                    column_max = data['column_max'],
                    name = data['name'],
                    room_id = Room.objects.get(id = self.kwargs['pk']))
        rack_add.save()
        return HttpResponseRedirect('/rooms/'+str(self.kwargs['pk'])+"/rack/"+str(rack_add.id))

class UpdateRackView(UpdateView):
    template_name = 'rack_update.html'
    model = Rack
    fields = ['name','column_max','row_max']
    def form_valid(self,form):
        data = form.cleaned_data
        rack_edit = Rack.objects.get(id = self.kwargs['pk'])
        rack_edit.name = data['name']
        rack_edit.row_max = data['row_max']
        rack_edit.column_max = data['column_max']
        rack_edit.save()
        return HttpResponseRedirect('/rooms/'+str(self.kwargs['room_pk'])+"/rack/"+str(self.kwargs['pk']))

class DeleteRackView(DeleteView):
    template_name = 'rack_delete.html'
    model = Rack
    success_url = '../'

    def delete(self, request, *args, **kwargs):
        data= Rack.objects.filter(id=self.kwargs['pk'])
        data.delete()
        return HttpResponseRedirect("/fishdetail/"+str(self.kwargs['pk']))




class FishDetailView(TemplateView):
    template_name = 'fishdetail.html'

    def get(self, request, *args, **kwargs):
        queryset = Substock.objects.all().values("amount","stock__birthdate","stock__fishline__name","stock__fishline__description").filter(position_id = kwargs['pk'])
        return render(self.request,self.template_name,{"info":queryset,
                                                        "position":kwargs['pk']})


class AddFishDetailView(CreateView):
    template_name = 'fish_detail_add.html'
    form_class =  DetailFishForm


    def form_valid(self,form):
        data = form.cleaned_data
        pos = Position(row = self.kwargs['row'] ,column = self.kwargs['col'] , rack_id = Rack.objects.get(id = self.kwargs['rack']))
        pos.save()
        substoc = Substock(amount = data['amount'],position_id = Position.objects.get(id = pos.id) )
        substoc.save()
        sto = Stock(birthdate= data['birthdate'],substock_id= Substock.objects.get(id = substoc.id))
        sto.save()
        fish = Fishline( name = data['name'] ,description = data['description'],stock_id = Stock.objects.get(id = sto.id))
        fish.save()
        return HttpResponseRedirect("/fishdetail/"+str(pos.id))


class UpdateFishDetailView(UpdateView):
        template_name = 'fish_detail_update.html'
        model = Position
        form_class = DetailFishForm
        def get(self, request, *args, **kwargs):
            data = Substock.objects.all().values("amount","stock__birthdate","stock__fishline__name","stock__fishline__description").filter(position_id = kwargs['pk'])
            form = DetailFishForm(initial= {'name':data[0]['stock__fishline__name'],'amount': data[0]['amount'],'description': data[0]['stock__fishline__description'],'birthdate': data[0]['stock__birthdate']})
            return render(self.request,self.template_name,{'form': form})

        def form_valid(self,form):
            data = form.cleaned_data
            substock_edit = Substock.objects.get(position_id = self.kwargs['pk'])
            substock_edit.amount = data['amount']
            substock_edit.save()

            stock_edit = Stock.objects.get(substock_id = substock_edit.id)
            stock_edit.birthdate = data['birthdate']
            stock_edit.save()

            fishline_edit = Fishline.objects.get(stock_id = stock_edit.id)
            fishline_edit.name = data['name']
            fishline_edit.description = data['description']
            fishline_edit.save()

            return HttpResponseRedirect("/fishdetail/"+str(self.kwargs['pk']))


class DeleteFishDetailView(DeleteView):
    template_name = 'fish_detail_delete.html'
    model = Position
    success_url = '../'

    def delete(self, request, *args, **kwargs):
        data= Position.objects.filter(id=self.kwargs['pk'])
        data.delete()
        return HttpResponseRedirect("/fishdetail/"+str(self.kwargs['pk']))
