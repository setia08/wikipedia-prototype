import random
from turtle import title
from django.shortcuts import render
from django import forms

from . import util
from markdown2 import Markdown

markdowner=Markdown()

class NewTaskForm(forms.Form):
    Title=forms.CharField(label='Title', max_length=100)
    Content=forms.CharField(widget=forms.Textarea(attrs={'rows':4, 'cols':5}))

class search_data(forms.Form):
    search_title=forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder': 'Search'}))


class Edit(forms.Form):
    textarea = forms.CharField(widget=forms.Textarea(attrs={'rows':4, 'cols':5}), label='')

def create(request):
    if request.method=="POST":
        form=NewTaskForm(request.POST)
        if form.is_valid():
                    title=form.cleaned_data["Title"]
                    content=form.cleaned_data["Content"]
                    enteries=util.list_entries()
                    if title in enteries:
                        return render(request,"encyclopedia/add.html",{
                            "message":"Page Already Exist",
                            "form":form
                        })
                    else:
                        util.save_entry(title,content)
                        page=util.get_entry(title)
                        page_converted=markdowner.convert(page)
                        return render(request,"encyclopedia/random_page.html",{
                            "title":title,
                            "enteries":page_converted
                        })
    else: 
        return render(request,"encyclopedia/add.html",{
         "form":NewTaskForm
        })

def random1(request):
    enteries=util.list_entries()
    hello = random.randint(0,len(enteries)-1)
    page_random=enteries[hello]
    entry=util.get_entry(page_random)
    converted_page=markdowner.convert(entry)
    return render(request,"encyclopedia/random_page.html",{ 
        "page":page_random,
        "enteries":converted_page,
        "title":page_random
    })

def index(request):
    form2=search_data(request.POST)
    if request.method=="POST" and form2.is_valid():
            title=form2.cleaned_data['search_title']
            enteries=util.list_entries()
            for i in enteries:
                if title in enteries:
                    page=util.get_entry(title)
                    converted_page=markdowner.convert(page)
                    return render(request,"encyclopedia/random_page.html",{
                        "enteries":converted_page,
                        "form1":search_data()
                    })
                else:
                    return render(request,"encyclopedia/index.html",{
                    "form1":search_data(),
                    "entries": util.list_entries(),
                    "message":"Searched page not found"
                    })
    else:
        return render(request,"encyclopedia/index.html",{
            "form1":search_data(),
            "entries": util.list_entries()
        })

def search1(request,name):
    if name in util.list_entries():
        page=util.get_entry(name)
        converted_page=markdowner.convert(page)
        return render(request,"encyclopedia/random_page.html",{
                        "page":name,
                        "enteries":converted_page,
                        "form1":search_data()
                    })

def edit(request,toedit):
    if request.method=="POST":
        form = Edit(request.POST) 
        if form.is_valid():
            textarea = form.cleaned_data["textarea"]
            util.save_entry(toedit,textarea)
            page = util.get_entry(toedit)
            page_converted = markdowner.convert(page)

            context = {
                'page': page_converted,
                'title': toedit
            }

            return render(request, "encyclopedia/entry.html", context)

    else:
        return render(request,"encyclopedia/edit.html",{
            "editpage":toedit,
            'edit': Edit(initial={'textarea': util.get_entry(toedit)})
        })
