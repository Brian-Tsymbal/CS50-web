from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from django.utils.html import strip_tags
from django import forms

from markdown2 import Markdown
import markdown2

import random

from . import util


# variables
new_list_entries = util.list_entries()

# classes


class NewWikiForm(forms.Form):
    title = forms.CharField(label="Title")
    body = forms.CharField(
        label="Content", widget=forms.Textarea())


class UpdateFile(forms.Form):
    body = forms.CharField(label="Content", widget=forms.Textarea())


class Search_Wikis(forms.Form):
    search = forms.CharField(label="Search encyclopedia")


# functions

# functions for side bar

def search_func(request):
    name = request.GET.get("q")
    name = name.capitalize()
    if name in new_list_entries:
        return visit(request, name)
    elif name.upper() in new_list_entries:
        return visit(request, name.upper())
    else:
        return render(request, "encyclopedia/search.html", {
            "entries": new_list_entries,
            "name": name,
            "names": name.capitalize() or name.upper() or name.lower() or name
        })


def new_wiki(request):
    if request.method == "POST":
        form = NewWikiForm(request.POST)
        if form.is_valid():
            form.title = form.cleaned_data['title']
            form.body = form.cleaned_data['body']
            if form.title in new_list_entries:
                return render(request, "encyclopedia/Exisits.html")
            else:
                util.save_entry(form.title, form.body)
                new_list_entries.append(form.title)
                return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "encyclopedia/create.html", {
                "form": form
            })
    else:
        return render(request, "encyclopedia/create.html", {
            "form": NewWikiForm()
        })


def random_search(request):
    return visit(request, random.choice(new_list_entries))


# functions for main body of html


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def visit(request, name):
    if name in new_list_entries:
        return render(request, "encyclopedia/General.html", {
            "name": name,
            "content": markdown2.markdown(util.get_entry(name)),
        })
    else:
        return render(request, "encyclopedia/Error_Page.html")


def update(request, names):
    get = util.get_entry(names)
    edit_form = UpdateFile()
    edit_form.fields['body'].initial = get
    if request.method == "POST":
        edit_form = UpdateFile(request.POST)
        if edit_form.is_valid():
            edit_form_body = edit_form.cleaned_data['body']
            util.save_entry(names, edit_form_body)
            return HttpResponseRedirect(reverse("visit", args=(names,)))
        else:
            return render(request, "encyclopedia/update.html", {
                "form": edit_form,
                "names": names
            })
    else:
        return render(request, "encyclopedia/update.html", {
            "form": edit_form,
            "names": names
        })


"""
# function for development purpose,


def dev_page(request):
    return render(request, "encyclopedia/hyper.html", {
        "entries": util.list_entries(),
        "lists": new_list_entries,
        "length": len(new_list_entries),
    })
"""
