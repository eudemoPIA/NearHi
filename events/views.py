from django.shortcuts import render, redirect
from .forms import EventForm

def filtered_events(request, category):
    context = {'category': category}
    return render(request, 'events/filtered_events.html', context)


def post_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm()
    
    return render(request, 'events/post_event.html', {'form': form})
