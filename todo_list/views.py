from django.shortcuts import redirect, render
from django.http import HttpResponse
from todo_list.models import Item

# Create your views here.
def home_page(request):
#    return HttpResponse('<html><title>Match Making Website</title></html>')
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/todo_list/the-only-profile-in-the-world/')

#    return render(request, 'home.html', {
#        'new_item_text': request.POST.get('item_text', ''),
#    items = Item.objects.all()
    return render(request, 'home.html')

def view_list(request):
    items = Item.objects.all()
    return render(request, 'profile.html', {'items': items})

