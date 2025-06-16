from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import ChatGroup
from .forms import ChatmessageCreateForm

@login_required
def chat_view(request):
    chat_group = get_object_or_404(ChatGroup, group_name="masyopnetinternshipGroup")
    chat_messages = chat_group.chat_messages.all().order_by('created')[:30]  # Oldest at top
    form = ChatmessageCreateForm()

    if request.htmx:
        form = ChatmessageCreateForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.group_name = chat_group  # ⚠️ Match the field name exactly as in your model
            message.save()
            context = {
                'message' : message,
                'user' :request.user
            }
            return render(request, 'a_rtchat/partials/chat_message_p.html',context)

    return render(request, 'a_rtchat/chat.html', {
        'chat_messages': chat_messages,
        'form': form,
    })
