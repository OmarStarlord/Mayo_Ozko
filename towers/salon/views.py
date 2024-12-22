from django.shortcuts import render

# Create your views here.
#empty view
def salon_view(request):
    return render(request, 'salon.html')