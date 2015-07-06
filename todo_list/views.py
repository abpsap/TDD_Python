from django.shortcuts import redirect, render
from django.http import HttpResponse
from todo_list.models import Item, Profile

# Create your views here.
def home_page(request):
#    return HttpResponse('<html><title>Match Making Website</title></html>')

### We no longer need the below 3 lines, as view-profile and new_profile are doing that work now
###    if request.method == 'POST':
###        Item.objects.create(text=request.POST['item_text'])
###        return redirect('/todo_list/the-only-profile-in-the-world/')

#    return render(request, 'home.html', {
#        'new_item_text': request.POST.get('item_text', ''),
#    items = Item.objects.all()
    return render(request, 'home.html')

def view_profile(request, profile_id):
    profile_ = Profile.objects.get(id=profile_id)
    return render(request, 'profile.html', {'profile': profile_})


def new_profile(request):
    profile_ = Profile.objects.create()
    Item.objects.create(text=request.POST['item_text'], profile=profile_)
#    return redirect('/todo_list/the-only-profile-in-the-world/')
    return redirect('/todo_list/%d/' % (profile_.id,))

def add_item(request, profile_id):
    profile_ = Profile.objects.get(id = profile_id)
    Item.objects.create(text=request.POST['item_text'], profile=profile_)
    return redirect('/todo_list/%d/' % (profile_.id,))