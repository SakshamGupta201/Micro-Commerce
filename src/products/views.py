from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import DetailView

from .models import Products
from .forms import ProductForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator


# class ProductCreateView(LoginRequiredMixin, CreateView):
#     model = Products
#     form_class = ProductForm
#     template_name = "products/create.html"
#     success_url = "/products/"

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)


def product_create_view(request):
    context = {}
    form = ProductForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        if request.user.is_authenticated:
            obj.user = request.user
            obj.save()
            return redirect("product-list")
        else:
            form.add_error(None, "You must be logged in to create a product.")
    context["form"] = form
    return render(request, "products/create.html", context)


def product_list_view(request):
    context = {}
    queryset = Products.objects.all()
    paginator = Paginator(queryset, 10)  # Show 10 products per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context["page_obj"] = page_obj
    return render(request, "products/list.html", context)


def product_detail_view(request, handle=None):
    product = get_object_or_404(Products, handle=handle)
    is_owner = product.user == request.user
    context = {
        "product": product,
    }
    if is_owner:
        form = ProductForm(request.POST or None, instance=product)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect("product-list")
        context["form"] = form
    return render(request, "products/detail.html", context)
