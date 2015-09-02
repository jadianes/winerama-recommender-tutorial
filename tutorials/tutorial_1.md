# A wine reviews website using Django and Bootstrap  
###### Building Data Products with Python  

With this tutorial, we start a series of tutorials about how to build data products with Python. As a *leitmotif* we want to build a web-based wine reviews and recommendations website using Python technologies such as Django and Pandas. We have chosen to build a wine reviews and recommendations website, but the concepts and the technology stack can be applied to any user reviews and recommendation product.

![](https://www.filepicker.io/api/file/4tFlIFhJQJuspZ57LN74)

We want this tutorial to leave you with a product that you can adapt and show to as part of your portfolio. With this goal in mind, we will explain how to set up a [Koding](https://koding.com) virtual machine and use it as a [Django](https://www.djangoproject.com/) and [Pandas](http://pandas.pydata.org/) + [Scikit-learn](http://scikit-learn.org/stable/index.html) Python development server. 

Then we will start a Django project and a Django app for our Wine recommender web application. It will be an incremental process that can be followed by checking out individual tags in our [GitHub repo](https://github.com/jadianes/winerama-recommender-tutorial). By doing so you can work in those individual tasks at a given stage that you find more interesting or difficult. 

In the next tutorial, we will add user management and, once we have users identified, proceed to generate user recommendations using machine learning.  

Remember that you can follow the tutorial at any development stage by forking [the repo](https://github.com/jadianes/winerama-recommender-tutorial) into your own GitHub account, and then cloning into your workspace and checking out the appropriate tag. By forking the repo you are free to change it as you like and experiment with it as much as you need. If at any point you feel like having a little bit of help with some step of the tutorial, or with making it your own, we can have a [1:1 Codementor session](https://www.codementor.io/jadianes) about it.  

Usually we will have deployed the latest stage of the app running [at Koding](http://jadianes.koding.io:8000/reviews/), including all the related tutorials updates. But let's start with our project from scratch!  

## Koding as a development server

[Koding](http://learn.koding.com/faq/what-is-koding/) is a cloud-based development environment complete with free virtual machines (VMs), an attractive IDE and sudo level terminal access. It can be used as a software development playground and everything you need to move your software development to the cloud! A Koding VM has many of the popular software packages and programming languages preinstalled so that you can focus on learning vs installing and configuring.  

We have used Koding while working in this tutorial, so it is a good option if you want to follow it. We even have the latest version of the website deployed in a test server running in our Koding VM (can be found [here](http://jadianes.koding.io:8000/reviews/)). However, this is not a requirement and you can work on the tutorial on your own machine or any other system that can install Python and the packages we need. About this, we recommend installing [Anaconda](http://continuum.io/downloads) that comes with all the analytics packages we will need in the later phases of the product.  

So if you want to follow our very same steps, the first thing is to [sign up for Koding](https://koding.com/R/jadianes). The only problem with the free account is that it comes with 3Gb diks space and we need at leat 4Gb. You will need to invite a couple of friend using your referral link so you can get more space. 

Once you have your Koding VM up and running, go to the Anaconda website and download+install the version of [Anaconda for your OS](http://continuum.io/downloads#all).  

Once this is done, the last bit is to install Django. What I did is to install it using the `pip` version that comes with Anaconda. That is, if you are at the root folder that contains your Anaconda installation, just type. 

```shell
./anaconda/bin/pip install django
```
## The GitHub repo  

One of the coolest things about this tutorial is that all the code is [available at GitHub](https://github.com/jadianes/winerama-recommender-tutorial), and that each section is tagged in a different tag (e.g. [stage-0](https://github.com/jadianes/winerama-recommender-tutorial/tree/stage-0) is the empty repo). So go to the repo and [fork it](https://help.github.com/articles/fork-a-repo/) to your GitHub account, and then clone it into your development server (Koding in our case).  

You can check out any tag and create a branch from that point, and then work in your changes. Or you can just work on your own and use the code in the repo to copy and paste and complete your files. For example, if we want to check out the first tag that has actually some work done, type from the root folder in the cloned repo:  

```bash
git checkout stage-0.1
```


## The core of our Django web application

A Django project lifecycle is managed by two commands. First we use `django-admin.py` to create a project. Then we use `python manage.py COMMAND` to do anything else. So let's start by creating a Django project.  

### Starting up the project with `startproject`

Create a directory folder where you want to place your Django project and move there using `cd`. Then run the `django-admin.py` command to create the project as follows.  

```bash
django-admin.py startproject winerama
```
Let’s look at what we just created by running the `startproject` command.

```bash
tree winerama  

winerama
|-- manage.py
`-- winerama
    |-- __init__.py
    |-- settings.py
    |-- urls.py
    `-- wsgi.py
```

This requires a bit of an explanation:  

- The `winerama/` root directory is a container for our project.  
- `manage.py` is a command-line utility that allows us to interact with our project in various ways. We will use it all the time so its purpose will be clear in a minute.
- The inner `winerama/` directory is the actual Python package for our project. Its name is also the Python package name for the project files.  
- `mysite/__init__.py` is an empty file that tells Python that this directory should be considered a Python package.  
- `mysite/settings.py` is the settings/configuration file for our project.  
- `mysite/urls.py` contains the URL declarations for this Django project.  
- `mysite/wsgi.py` is an entry-point for WSGI-compatible web servers to serve our project.  

### Running the server with `runserver`  

```bash
python manage.py runserver 0.0.0.0:8000
```
Then we can go to our Koding server public URL `http://KODING_USERNAME.koding.io:8000` where we replace `KODING_USERNAME` with our Koding user and check how the website looks so far.  

![enter image description here](https://www.filepicker.io/api/file/uVbVULd7QqWvZg1UGeje "enter image title here")  

### Database setup  

Now, open up `winerama/settings.py`. It’s a normal Python module with module-level variables representing Django settings.

By default, Django uses SQLite, and we will stick to it. SQLite is included in Python, so you won’t need to install anything else to support your database. If you plan to deploy this project into production, you better move to some production-ready database such as PostgreSQL to avoid database-switching headaches down the road.  

So we don't need to change anything in our settings file. If any, change `winerama /settings.py` to  set TIME_ZONE to your time zone.  

But in any case, some of the installed applications (more on this later) make use of at least one database table, though, so we need to create the tables in the database before we can use them. To do that, run the following command:

```bash
python manage.py migrate
```

### Apps vs Projects  

Now we are ready to start our wine reviews app. But wait, what is the difference between and app and a project? From the Django website:    

> What’s the difference between a project and an app? An app is a Web application that does something – e.g., a Weblog system, a database of public records or a simple poll app. A project is a collection of configuration and apps for a particular Web site. A project can contain multiple apps. An app can be in multiple projects. [...] Django apps are “pluggable”: You can use an app in multiple projects, and you can distribute apps, because they don’t have to be tied to a given Django installation.  

So in our case, our *Winerama* project will contain our first `reviews` app, that will allow users to add wine reviews. In order to do that, from the root `winerame` folder where `manage.py` is, we need to use the `startapp` command as follows.  

```bash
python manage.py startapp reviews
```  
This will create the following folder structure.  

```bash
tree reviews

reviews
|-- __init__.py
|-- admin.py
|-- migrations
|   `-- __init__.py
|-- models.py
|-- tests.py
`-- views.py
```

We will get to know those files in the following sections, while creating model entities, views, and setting up the admin interface.  

But first we need to activate our reviews app. Edit the `winerama/settings.py` file, and change the `INSTALLED_APPS` setting to include the string 'reviews' as follows.  

```python
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'reviews',
)

```

### Adding model entities  

In this first stage, our wine reviews app will contain two model entities: Wine and Review. A Wine has just a name. A Review has four fields: a name for the user that made the review, a wine rating, a publication date, and a text review. Additionally, each Review is associated with a Wine.   

These two entities are represented by Python classes that we add to the `reviews/models.py` file as follows.  

```python
from django.db import models
import numpy as np


class Wine(models.Model):
    name = models.CharField(max_length=200)
    
    def average_rating(self):
        all_ratings = map(lambda x: x.rating, self.review_set.all())
        return np.mean(all_ratings)
        
    def __unicode__(self):
        return self.name


class Review(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    wine = models.ForeignKey(Wine)
    pub_date = models.DateTimeField('date published')
    user_name = models.CharField(max_length=100)
    comment = models.CharField(max_length=200)
    rating = models.IntegerField(choices=RATING_CHOICES)
    
```

Each of our two model entities is represented by a class that subclasses `django.db.models.Model`. Each model class variable represents a database field in the model and is represented by an instance of a Field sub-class. This specifies what type of data each field holds. The field name is its code reference in machine-friendly format, and our database will use it as the column name.

You can use an optional first positional argument to a Field to designate a human-readable name. If this field isn’t provided, Django will use the machine-readable name.  

Some field classes have required and optional arguments, such as `max_length` for `CharField`, etc. That’s used both, in the database schema, and in validation.

Finally, we specify relationships between entities by using a `ForeignKey` field. That tells Django each `Review` is related to a single `Wine`.  

In Django, model classes can also define methods providing domain functionality. In our case, we have defined a method to get the average score for a given wine, based on all the reviews associated with it (i.e. the method `average_rating(self)`).  

Since we have made changes to our model, we need to propagate that to our database. We will do that by running the following command that creates migrations for our changes.  

```bash
python manage.py makemigrations reviews
```

And now we can aply our migrations to the data base as follows, without losing data.  

```bash
python manage.py migrate
```

This point of the project corresponds to the git tag [`stage-0.1`](https://github.com/jadianes/winerama-recommender-tutorial/tree/stage-0.1).  

### Providing an Admin Site  

First of all, we need to create an admin user by running the following command for the `winerama/` root folder that contains `manage.py`. 

```bash
python manage.py createsuperuser
```

You'll be prompted for a user name, email address, and password. Introduce those that work for you. You will use them to login and admin the system.  

The admin site is activated by default. Let's explore it. If your website is not up and running, use the following command.

```bash
python manage.py runserver 0.0.0.0:8000
```

And now you can navigate to `http://KODING_USERNAME:8000/admin/` (remember to replace KODING_USERNAME with your actual Koding username) and login with the user and password that you specified before.  

You will notice that our model entities are not modifiable in the admin site. In order for them to be there, we need to add them in the `reviews/admin.py` file so it looks like this.  

```python
from django.contrib import admin

from .models import Wine, Review

class ReviewAdmin(admin.ModelAdmin):
    model = Review
    list_display = ('wine', 'rating', 'user_name', 'comment', 'pub_date')
    list_filter = ['pub_date', 'user_name']
    search_fields = ['comment']
    
admin.site.register(Wine)
admin.site.register(Review, ReviewAdmin)
```

We are basically importing the model classes we just defined, and then using `register()` to the Django that we want wines and reviews to be available in the admin site.  

![enter image description here](https://www.filepicker.io/api/file/TkB8PydGQYOovzGElPXN "enter image title here")  

If we navigate again to the admin site, we will see a new *Reviews* section with a *Wines* and **Reviews** elements inside. These elements include two action buttons, **Add** and **Change**. Add can be used to introduce new wines or wine reviews. The forms are automatically generated from the `Wine` and `Review` models. 

But with wine reviews we have done a little extra work and defined a custom admin class. There are many things we can do with this class, but in our case we have specified:  

- what columns (and in what order) do we want to display in the entries list. That is, when using the **Change** button or when navigating to `admin/reviews/wine` or `admin/reviews/review`, we will see a list of all added entries. How the entries are listed when we go to the reviews section is specified by the `list_display` field in the `ReviewAdmin` class.  
- A list of filters that can be used to list reviews.  
- A list of fields that will be matched when using the search box.  

We suggest you experiment with this `ReviewAdmin` class (or create your own `WineAdmin` one) until you're happy with the results.  

We have accomplished a lot just by writing a few classes. Django is really powerful when it comes to providing an admin interface. In the next section, we will work on our actual user interface to add wine reviews.  

This stage of the project corresponds to the git tag [`stage-0.2`](https://github.com/jadianes/winerama-recommender-tutorial/tree/stage-0.2).  

## Adding Web Views  

In Django, a view is a type of Web page that generally serves a specific function and has a specific template. The concept is taken from the [Model-View-Controller](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller) architectural pattern so common in web application frameworks.  

In Django, a view is actually a Python function that delivers a web page (and other content). When a user navigates to a URL within our application, Django will choose a view by examining the URL that’s requested.

But let's show this in practice.    

First thing we need to do is to include our reviews app in the project urls. In order to do so, edit the `winerama/urls.py` file (not the reviews one, yet), and modify the `urlpatters` list there to look like the following.  

```python
urlpatterns = [
    url(r'^reviews/', include('reviews.urls', namespace="reviews")),
    url(r'^admin/', include(admin.site.urls)),
]
```

Basically we have added a new mapping specifying that all requests starting with `reviews/` will be passed to our reviews app url mapping under the namespace `reviews`.  

Mappings can extract parts of the url and pass it as a parameter to the handling view. For example, the mapping:  

```python
url(r'^review/(?P<review_id>[0-9]+)/$', views.review_detail, name='review_detail')  
```

extracts a number after the `reviews/review/` part and passes it to the `review_detail` function defined later on.  

So in order for this mapping to work, we need to add it in our `reviews/urls.py` file. Let's add some of them. Change the `reviews/urls.py` file to look as follows.   

```python
from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /
    url(r'^$', views.review_list, name='review_list'),
    # ex: /review/5/
    url(r'^review/(?P<review_id>[0-9]+)/$', views.review_detail, name='review_detail'),
    # ex: /wine/
    url(r'^wine$', views.wine_list, name='wine_list'),
    # ex: /wine/5/
    url(r'^wine/(?P<wine_id>[0-9]+)/$', views.wine_detail, name='wine_detail'),
]
```

The mapping structure is the same as before. For example, we specify that any request starting with an empty string (plus the `reviews/` prefix we added at the project level), will be handled by a function called `review_list` defined in our `reviews/views.py` file, and will be referenced within the local namespace (remember we gave the namespace `reviews` in the project `winerama/urls.py`) with the name `reviews_list`. 

So now we need the actual views. As we said these are just Python functions that deal with model entities is required and decide how to render the results (as an HTML page in our case). Modify the `reviews/views.py` file to look like the following.  

```python
from django.shortcuts import get_object_or_404, render

from .models import Review, Wine


def review_list(request):
    latest_review_list = Review.objects.order_by('-pub_date')[:9]
    context = {'latest_review_list':latest_review_list}
    return render(request, 'reviews/review_list.html', context)


def review_detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    return render(request, 'reviews/review_detail.html', {'review': review})


def wine_list(request):
    wine_list = Wine.objects.order_by('-name')
    context = {'wine_list':wine_list}
    return render(request, 'reviews/wine_list.html', context)


def wine_detail(request, wine_id):
    wine = get_object_or_404(Wine, pk=wine_id)
    return render(request, 'reviews/wine_detail.html', {'wine': wine})

```

There we have defined four different views for each of the four different url mappings we specified previously. Each function gets at least a `request` object parameter, and optionally more parameters as specified in the url mapping. For example, the `review_detail` function gets also a `review_id` parameter as we specified in the mapping.  

Once we are inside the view function, we normally do some model query, and create a context object with the results. Queries are normally performed by using the `.objects` attribute in the given domain entity class (e.g. `Review.objects`). We can apply different sorting methods, filters, etc. until we get the desired results (have a look [here](https://docs.djangoproject.com/en/1.8/ref/models/querysets/) for more about query sets). This context object is then passed to the `render` function together with the reference to the template file that will generate the resulting web page.  

In the order they appear in the file, the views are:  

- `review_list`: gets a list of the latest 9 reviews and renders it using `reviews/list.html'.  
- `review_detail`: gets a review given its ID and renders it using `review_detail.html`.  
- `wine_list`: gets all the wines sorted by name and passes it to `wine_list.html` to be rendered.   
- `wine_detail`: gets a wine from the DB given its ID and renders it using `wine_detail.html`.   

And now, we need to create the HTML templates that will generate the final pages. These are expressed in Django template language. This language allows us to put variable placeholders and control structures within HTML code in order to dynamically generate the final web page.   

![enter image description here](https://www.filepicker.io/api/file/ez0uKpkTgSqvvw7gNBhq "enter image title here")

For example, this is how the `review_list` view template looks like.  

```python
<h2>Latest reviews</h2>

{% if latest_review_list %}
<div>
    {% for review in latest_review_list %}
    <div>
        <h4><a href="{% url 'reviews:review_detail' review.id %}">
        {{ review.wine.name }}
        </a></h4>
        <h6>rated {{ review.rating }} of 5 by {{ review.user_name }}</h6>
        <p>{{ review.comment }}</p>
    </div>
    {% endfor %}
</div>
{% else %}
<p>No reviews are available.</p>
{% endif %}
```

This template makes use of some Django template language structures. All of them are enclosed within `{% ... %}` elements. For example, the `{% if latest_review_list %}{% else %}{% endif %}` directive is like any other if-else structure in computer programming. The first section will execute if the object `latest_review_list` exists, and the second section will do otherwise. The `latest_review_list` object is part of the context object we build and pass to `render` in the view function defined in `reviews/views.py`. The `for` block is equivalent to a programming for, and so on. Object methods and fields are accessed using the dot notation.  

Django also provides us with a `{% url ... %}` we can use together with namespaces in order not to hardcode urls within templates. We make use of that in our template as we can see.  

You can check how all the views look like in the `stage-0.3` of the project repo. We don't mean to explain all the details of the Django template language here. For the curious reader, have a look at the [official Django documentation](https://docs.djangoproject.com/en/1.8/topics/templates/).  

Therefore, adding new mappings is as easy as adding more elements to the `urlpatters` view. Once we do that, we need to add the appropriate function in `reviews/views.py` and create the HTML page that will render the results.  

We have added a couple of wines and reviews to the database, so you can navigate to `http://KODING_USERNAME:8000/reviews/` and see it in action. This is one of four possible web pages we can visit in our app. Are you able to check all of them using your browser from what we have seen in `reviews/urls.py`? Try to construct the urls.  

This point of the project corresponds to the git tag [`stage-0.3`](https://github.com/jadianes/winerama-recommender-tutorial/tree/stage-0.3).  

## Adding Reviews Using Forms  

In this section we will explain how one of our views will include a form that will be used to add wine reviews.  

![enter image description here](https://www.filepicker.io/api/file/jMjX2X5OQrOHstd79YEw "enter image title here")

This view is the wine detail view. Remember that when we show a wine's details, we also show some of its recent reviews. What we want to do is provide also an HTML form that can be used to add a new review for that particular wine.  

Let's start with the easy part. This is how the wine detail view including a form looks like.  

```python
<h2>{{ wine.name }}</h2>
<h5>{{ wine.review_set.count }} reviews ({{ wine.average_rating | floatformat }} average rating)</h5>


<h3>Recent reviews</h3>

{% if wine.review_set.all %}
<div>
    {% for review in wine.review_set.all %}
    <div>
        <em>{{ review.comment }}</em>
        <h6>Rated {{ review.rating }} of 5 by {{ review.user_name }}</h6>
        <h5><a href="{% url 'reviews:review_detail' review.id %}">
        Read more
        </a></h5>
    </div>
    {% endfor %}
</div>
{% else %}
<p>No reviews for this wine yet</p>
{% endif %}

<h3>Add your review</h3>
{% if error_message %}<p><strong>{{ error_message }}</strong></p>{% endif %}

<form action="{% url 'reviews:add_review' wine.id %}" method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="Add" />
</form>
```

You can see that we didn't really include any form fields there. What we are doing here is using Django template language to leave a `{{ form.as_p }}` object to be rendered with the appropriate fields (as `<p>` HTML elements). We define this form class as a [`ModelForm`](https://docs.djangoproject.com/en/1.8/topics/forms/modelforms/#modelform) in the file `reviews/forms.py` as follows.  

```python
from django.forms import ModelForm, Textarea
from reviews.models import Review


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['user_name', 'rating', 'comment']
        widgets = {
            'comment': Textarea(attrs={'cols': 40, 'rows': 15}),
        }
```

The `ReviewForm` class specifies the model object it's going to use as a base (i.e. `Review`), a selection of fields to use, and also what widget to use for one of them (the comment field).  

The first time we display the wine details, we need to pass a new empty form object. We add that in our `wine_detail` view function. We also add the `add_review` function view  in `reviews/views.py`. The file will look as follows.   

```python
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import Review, Wine
from .forms import ReviewForm
import datetime


def review_list(request):
    latest_review_list = Review.objects.order_by('-pub_date')[:9]
    context = {'latest_review_list':latest_review_list}
    return render(request, 'reviews/review_list.html', context)


def review_detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    return render(request, 'reviews/review_detail.html', {'review': review})


def wine_list(request):
    wine_list = Wine.objects.order_by('-name')
    context = {'wine_list':wine_list}
    return render(request, 'reviews/wine_list.html', context)


def wine_detail(request, wine_id):
    wine = get_object_or_404(Wine, pk=wine_id)
    form = ReviewForm()
    return render(request, 'reviews/wine_detail.html', {'wine': wine, 'form': form})


def add_review(request, wine_id):
    wine = get_object_or_404(Wine, pk=wine_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        rating = form.cleaned_data['rating']
        comment = form.cleaned_data['comment']
        user_name = form.cleaned_data['user_name']
        review = Review()
        review.wine = wine
        review.user_name = user_name
        review.rating = rating
        review.comment = comment
        review.pub_date = datetime.datetime.now()
        review.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('reviews:wine_detail', args=(wine.id,)))

    return render(request, 'reviews/wine_detail.html', {'wine': wine, 'form': form})
```

The `add_review` function is in charge of validating the form and creating the new review instance. The first thing it does is to use the request url wine ID to look for the wine we are going to add the review to. It will redirect the view to a 404 page if it doesn't find it. Otherwise, it will create a `ReviewForm` instance from the request POST data). 

We can validate the form with a single call to `form.isvalid()`. When the for is not valid, we will just render the wine detail page again, passing the original form so it can be corrected. If the form is indeed valid, we create the review object, save it, and redirect to the wine details page again. Here we don't render directly the page but internally navigate to the `wine_detail` view with the appropriate wine ID.   

Now we need to connect everything together. The action attribute in the `form` HTML element, specifies what url handles the post request once the form is submitted. Then, we need create the appropriate url mapping in `reviews/urls.py`. Modify that file that should look like the following.  

```python
from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /
    url(r'^$', views.review_list, name='review_list'),
    # ex: /review/5/
    url(r'^review/(?P<review_id>[0-9]+)/$', views.review_detail, name='review_detail'),
    # ex: /wine/
    url(r'^wine$', views.wine_list, name='wine_list'),
    # ex: /wine/5/
    url(r'^wine/(?P<wine_id>[0-9]+)/$', views.wine_detail, name='wine_detail'),
    url(r'^wine/(?P<wine_id>[0-9]+)/add_review/$', views.add_review, name='add_review'),
]
```

With this, we can navigate to any wine detail page (e.g. http://KODIG_USERNAME:8000/reviews/wine/1/) and add a new review. Don't worry too much about the page not being very attractive. We will solve this in the next two sections.  


![enter image description here](https://www.filepicker.io/api/file/jMjX2X5OQrOHstd79YEw "enter image title here")

This point of the project corresponds to the git tag [`stage-0.4`](https://github.com/jadianes/winerama-recommender-tutorial/tree/stage-0.4).  

## Template Reuse  

We have views that are useful. We can browse our wine and reviews, and we can add new reviews. Moreover, some views have links that allow us to navigate between them. However, we need some reference links that allow us to go to a couple of reference views, independently of where we are in the navigation flow. That is, we want a menu.  

An option would be to replicate a list of links in every single page we have (the four of them so far). But we know this is not very good practice. Fortunately, the Django template language allows us to extend templates. Thanks to this, we can define a base template containing the menu and the main page structure, and then make each of our four views extend this base template.  

This is how the `reviews/templates/reviews/base.html` template will look like.  

![enter image description here](https://www.filepicker.io/api/file/DRLpfsLCTDO6mc5Zxv1P "enter image title here")

```python
<div>
    <nav>
        <div>
            <a href="{% url 'reviews:review_list' %}">Winerama</a>
        </div>
        <div id="navbar">
            <ul>
                <li><a href="{% url 'reviews:wine_list' %}">Wine List</a></li>
                <li><a href="{% url 'reviews:review_list' %}">Home</a></li>
            </ul>
        </div>
    </nav>
    

    <h1>{% block title %}(no title){% endblock %}</h1>


    {% block content %}(no content){% endblock %}
</div>
```

There are three main sections in this base template. First we define a navitation bar between `<nav>` tags. There we have three links. the first one is the branding section that also acts as a home link. the other two are the menu elements. One of them gets the user to the wine list, and the other one is again the home link. The home page is the latest reviews view, as defined in our urls file.  

The other two sections define the strcuture for all our views. They are compones by a title block and a content block. We use the Django template language `{% block ... %}` directive for that purpose.  

Then we have to make each of the HTML templates we create for our views to do extend this base template. For example, the `review_list.html` template will look as follows.  

```python
{% extends 'reviews/base.html' %}

{% block title %}
<h2>Latest reviews</h2>
{% endblock %}

{% block content %}
{% if latest_review_list %}
<div>
    {% for review in latest_review_list %}
    <div>
        <h4><a href="{% url 'reviews:review_detail' review.id %}">
        {{ review.wine.name }}
        </a></h4>
        <h6>rated {{ review.rating }} of 5 by {{ review.user_name }}</h6>
        <p>{{ review.comment }}</p>
    </div>
    {% endfor %}
</div>
{% else %}
<p>No reviews are available.</p>
{% endif %}
{% endblock %}
```

The first line is always a `{% extends 'reviews/base.html' %}` directive that specifies that our template extends the base template. By doing this, our `review_list.html` will automatically include the navigation menu. Then we define the content of the two blocks we defined in the base template. Django will replace the base blocks with these we define here. 

Check the rest of the views in the tutorial repo. This point of the project corresponds to the git tag [`stage-0.5`](https://github.com/jadianes/winerama-recommender-tutorial/tree/stage-0.5).  

## Styling with Bootstrap  

[Bootstrap](http://getbootstrap.com/) is a popular HTML, CSS, and JS framework for developing responsive, mobile first projects on the web. Our web opages look rather dull and visually disorganised. We will use Bootstrap to make them provide a better user experience.  

The easiest (and cleanest) way to use Bootstrap for a Django project is to install and use the [Bootstrap 3 for Django](https://github.com/dyve/django-bootstrap3) app. Installation is as easy as going to our Koding terminal and running, **using the Anaconda pip command**, the following:  

```bash
pip install django-bootstrap3
``` 

Once we do that, we can change our Winerama project settings to include the Bootstrap 3 for Django apps by defining the `INSTALLED_APPS` list as follows.  

```python
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap3',
    'reviews',
)
```

Now we can use Bootstrap in our templates. First we add it to our `base.html` template to leave it like the following.  

```python
{% load bootstrap3 %}

{% bootstrap_css %}
{% bootstrap_javascript %}

{% block bootstrap3_content %}
<div class="container">
    <nav  class="navbar navbar-default">
        <div class="navbar-header">
            <a class="navbar-brand" href="{% url 'reviews:review_list' %}">Winerama</a>
        </div>
        <div id="navbar" class="navbar-collapse collapse">
            <ul class="nav navbar-nav">
                <li><a href="{% url 'reviews:wine_list' %}">Wine list</a></li>
                <li><a href="{% url 'reviews:review_list' %}">Home</a></li>
            </ul>
        </div>
    </nav>
    

    <h1>{% block title %}(no title){% endblock %}</h1>

    {% bootstrap_messages %}

    {% block content %}(no content){% endblock %}
</div>

{% endblock %}
```

We have modified the base template file following the [Bootstrap 3 for Django documentation](http://django-bootstrap3.readthedocs.org/en/latest/). Basically, we import some libraries and then assign some classes to different HTML elements. Nothing special here.  

The rest of the templates have little modification. We just add some Bootstrap classes where needed. The only one that has major modifications is the `wine_detail.html` template. It will look as follows:  

```python
{% extends 'reviews/base.html' %}
{% load bootstrap3 %}

{% block title %}
<h2>{{ wine.name }}</h2>
<h5>{{ wine.review_set.count }} reviews ({{ wine.average_rating | floatformat }} average rating)</h5>
{% endblock %}

{% block content %}
<h3>Recent reviews</h3>

{% if wine.review_set.all %}
<div class="row">
    {% for review in wine.review_set.all %}
    <div class="col-xs-6 col-lg-4">
        <em>{{ review.comment }}</em>
        <h6>Rated {{ review.rating }} of 5 by {{ review.user_name }}</h6>
        <h5><a href="{% url 'reviews:review_detail' review.id %}">
        Read more
        </a></h5>
    </div>
    {% endfor %}
</div>
{% else %}
<p>No reviews for this wine yet</p>
{% endif %}

<h3>Add your review</h3>
{% if error_message %}<p><strong>{{ error_message }}</strong></p>{% endif %}

<form action="{% url 'reviews:add_review' wine.id %}" method="post" class="form">
    {% csrf_token %}
    {% bootstrap_form form layout='inline' %}
    {% buttons %}
    <button type="submit" class="btn btn-primary">
      {% bootstrap_icon "star" %} Add
    </button>
    {% endbuttons %}
</form>
{% endblock %}
```

That results in the following web page.  

![enter image description here](https://www.filepicker.io/api/file/Kh3iK0jQQKevsgePLxpA "enter image title here")

See how first, we need to import `{% load bootstrap3 %}` in order to use Bootstrap 3 for Django tags (like the one we use in the form). Apart from classes added to divs, we have used the `{% bootstrap_form form layout='inline' %}` directive in order to render the form ala Bootstrap, including a button with a starred icon.  

This point of the project, the last stage for this part of the tutorial, corresponds to the git tag [`stage-1`](https://github.com/jadianes/winerama-recommender-tutorial/tree/stage-1). 

## Conclusions and Future Works

In this tutorial we have explained how to set up Koding as a Django/Pandas development server. Then we have started a Django project and a Django app for our Wine recommender web application. We have added some model entities, and explained how to create views and forms for them. We have closed this first part of the tutorial by adding some style by using Bootstrap.   

In the next part of the tutorial, we will add user management and, once we have users identified, proceed to generate user recommendations using machine learning.  

The whole tutorial can be followed by checking out individual tags in our [GitHub repo](https://github.com/jadianes/winerama-recommender-tutorial). By doing so you can work in those individual tasks at a given stage that you find more interesting or difficult.  And usually will have deployed the latest stage of the app running [at Koding](http://jadianes.koding.io:8000/reviews/).     
