import random

from django.shortcuts import render
from . import util
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    if request.method == "POST":
        if 'edit' in request.POST and request.POST['edit'] != "":
            return render(request, "encyclopedia/newpage.html", {
                "edit": True,
                "title": title,
                "content": util.get_entry(title)
            })

    return render(request, "encyclopedia/entry.html", {
           "content": util.get_entry(title),
           "title": title
    })


def search(request):
    if request.GET['q'] != "":
        value = request.GET['q'].strip()
    if util.get_entry(value) != None:
        return HttpResponseRedirect(reverse("entry", kwargs={'title': value}))
    else:
        result = []
        en_list = util.list_entries()
        for element in en_list:
            if value.lower() in element.lower():
                result.append(element)
        return render(request, "encyclopedia/index.html", {
                "entries": result,
                "search": True,
                "value": value
                })

def newpage(request):
    exists = False
    if request.method == "POST":
        if 'title' in request.POST and 'content' in request.POST:
            if request.POST['title'].strip() != "" and request.POST['content'].strip() != "":
                if request.POST['title'].strip() in util.list_entries() and request.POST['content'] == "":
                    exists = True
                else:
                    util.save_entry(request.POST['title'].strip(), request.POST['content'].strip())

    return render(request, "encyclopedia/newpage.html",
                  {
                    "exists": exists
                  })

def randompage(request):
    if request.GET['name'] == "randompg":
        title = random.choice(util.list_entries())
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": util.get_entry(title),
        })



