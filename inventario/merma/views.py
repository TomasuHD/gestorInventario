from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegisterForm, ItemInventarioForm
from .models import ItemInventario, Category
from datetime import datetime
from inventario.settings import LOW_QUANTITY
from django.contrib import messages
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class Index(TemplateView):
    template_name = 'merma/index.html'

class Dashboard(LoginRequiredMixin, View):
    def get(self, request):
        items = ItemInventario.objects.filter(user=self.request.user.id).order_by('id')

        low_inventory = ItemInventario.objects.filter(user=self.request.user.id,
        quantity__lte=LOW_QUANTITY)

        if low_inventory.count() > 0:
            if low_inventory.count() >1:
                messages.error(request, f'Atención, a {low_inventory.count()} items le quedan pocas existencias!')
            else:
                messages.error(request, f'{low_inventory.count()} item le queda pocas existencias')

        low_inventory_ids = ItemInventario.objects.filter(
            user=self.request.user.id,
            quantity__lte=LOW_QUANTITY
        ).values_list('id', flat=True)

        return render(request, 'merma/panel.html', {'items': items, 'low_inventory_ids': low_inventory_ids})

class SignUpView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'merma/registro.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )

            login(request, user)
            return redirect('index')
        
        return render(request, 'merma/registro.html', {'form': form})
    
class AddItem(LoginRequiredMixin, CreateView):
    model = ItemInventario
    form_class = ItemInventarioForm
    template_name = 'merma/form_item.html'
    success_url = reverse_lazy('panel')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class EditItem(LoginRequiredMixin, UpdateView):
    model = ItemInventario
    form_class = ItemInventarioForm
    template_name = 'merma/form_item.html'
    success_url = reverse_lazy('panel')

class DeleteItem(LoginRequiredMixin, DeleteView):
    model = ItemInventario
    template_name = 'merma/eliminar_item.html'
    success_url= reverse_lazy('panel')
    context_object_name = 'item'

def GenerarReporte(request):
    # Obtener la fecha actual y formatearla
    fecha_actual = datetime.now()
    fecha_formateada = fecha_actual.strftime("%d%b%y").upper()

    # Crear el nombre del archivo con la fecha formateada
    filename = f"reporteInventario_{fecha_formateada}.pdf"

    # Crear un objeto HttpResponse con el contenido PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    p = canvas.Canvas(response, pagesize=letter)
    p.setFont("Helvetica", 12)

    p.drawString(200, 750, "Reporte de Inventario")

    p.drawString(50, 700, "ID")
    p.drawString(100, 700, "Nombre")
    p.drawString(300, 700, "Cantidad")
    p.drawString(400, 700, "Categoría")

    items = ItemInventario.objects.filter(user=request.user)
    y = 680
    for item in items:
        p.drawString(50, y, str(item.id))
        p.drawString(100, y, item.name)
        p.drawString(300, y, str(item.quantity))
        p.drawString(400, y, item.category.name)
        y -= 20

    p.showPage()
    p.save()
    return response