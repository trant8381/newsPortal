from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse, Http404
from news.models import News
from datetime import datetime
from collections import OrderedDict

class CreateView(View):
    def get(self, request, *args, **kwargs):
        return render(
            request, 'news/create.html', context={}
        )

    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        text = request.POST.get('text')
        our_news.add_news(
            {
                "created": str(datetime.now()),
                "text": text,
                "title": title,
                "link": lambda x: len(our_news.links)+1
                if (len(our_news.links)+1) not in our_news.links else our_news.get_link()
            }
        )
        return redirect("/news/")


class SpecificNewsView(View):
    def get(self, request, link, *args, **kwargs):
        x = int(link)
        context = {}
        for _news in our_news.news:
            if _news["link"] == x:
                context = {
                    'specific_news': _news
                }
        if len(context) == 0:
            return HttpResponse('')
        return render(
            request, 'news/news_template.html', context=context
        )


class NewsView(View):
    def get(self, request, *args, **kwargs):
        x = our_news.get_sorted_by_date()
        t = tuple()
        title = request.GET.get('q')
        m = OrderedDict()
        g = []
        if title is None:
            context = {
                'News': x
            }
        else:
            for key, value in x.items():
                for char in value:
                    if title in char['title']:
                        g += [char]
                        print(True)
                if len(g) == 0:
                    g = []
                    continue
                m[key] = g
                g = []
            context = {
                'News': m
            }
        return render(
                request, 'news/news.html', context=context
            )



class MainView(View):
    def get(self, request, *args, **kwargs):
        return redirect('/news/')


our_news = News()

# test1 = SpecificNewsView()
# test1.get("200", 1)

# test2 = NewsView()
# test2.get("200")

# test3 = CreateView()
# test3.post("200")