# Adding user management  

This is the second tutorial on our series on how to build data products with Python. Remember that as a *leitmotif* we want to build a web-based wine reviews and recommendations website using Python technologies such as Django and Pandas. We have chosen to build a wine reviews and recommendations website, but the concepts and the technology stack can be applied to any user reviews and recommendation product.

We want these tutorials to leave you with a product that you can adapt and show as part of your portfolio. With this goal in mind, we will explain how to set up a [Koding](https://koding.com) virtual machine and use it as a [Django](https://www.djangoproject.com/) and [Pandas](http://pandas.pydata.org/) + [Scikit-learn](http://scikit-learn.org/stable/index.html) Python development server. 

In the first tutorial, we started a Django project and a Django app for our Wine recommender web application. The whole thing will be an incremental process that can be followed by checking out individual tags in our [GitHub repo](https://github.com/jadianes/winerama-recommender-tutorial). By doing so you can work in those individual tasks at a given stage that you find more interesting or difficult. 

In this second tutorial, we will add user management. This is an important part. Once we are able to identify individual users, we will be ready to generate user recommendations through machine learning. 

![](https://www.filepicker.io/api/file/U0kzq3UnQqA7RmXBtSIW) 

Remember that you can follow the tutorial at any development stage by forking [the repo](https://github.com/jadianes/winerama-recommender-tutorial) into your own GitHub account, and then cloning it into your workspace and checking out the appropriate tag. By forking the repo you are free to change it as you like and experiment with it as much as you need. If at any point you feel like having a little bit of help with some step of the tutorial, or with making it your own, we can have a [1:1 codementor session](https://www.codementor.io/jadianes) about it.  

So let's continue with our project!  

## Configuring Django Authentication  

From the very moment we created our project using `django-admin startproject`, all the modules for user authentication were activated. These consist of two items listed in our `INSTALLED_APPS` in `settings.py`:

- `django.contrib.auth` contains the core of the authentication framework, and its default models.  
- `django.contrib.contenttypes` is the Django content type system, which allows permissions to be associated with models you create.  

and these items in your `MIDDLEWARE_CLASSES` setting:  

- `SessionMiddleware` manages sessions across requests.  
- `AuthenticationMiddleware` associates users with requests using sessions.  
- `SessionAuthenticationMiddleware` logs users out of their other sessions after a password change.  

With these settings in place, when we ran the command `manage.py migrate` we already created the necessary database tables for authentication related models and permissions for any models defined in our installed apps. In fact, we can see them in the admin site, in the Users section.  

But we want to do at least two things. First we want to require authentication for some of the actions in our web app (e.g. when adding a new wine review). Second we want users to be able to sign up and sign in using our web app (and not through the admin site).  

## Limiting access to logged-in users  

By now, let's accept that we can just create users by using the admin interface. Go there and create a user that we will use in this section. If we have been using the admin interface recently, we will probably continue to be logged in as the admin. That's ok for now. 

The next thing we want to do is to limit the access to our `add_review` view so only logged-in users can use it.  

The clean and elegant way of limiting access to views is by using the `@login_required` annotation. Modify the `add_review` function in `reviews/views.py` so it looks like this:  

```python
@login_required
def add_review(request, wine_id):
    wine = get_object_or_404(Wine, pk=wine_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        rating = form.cleaned_data['rating']
        comment = form.cleaned_data['comment']
        user_name = form.cleaned_data['user_name']
        user_name = request.user.username
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

We have done two modifications. The first one is to add the `@login_required` annotation. By doing so we allow access to this view function just to logged in users. The second is to use `request.user.username` as the user name for our reviews. The request object has a reference to the active user, and this instance has a `username` field that we can use as needed.  

Since we don't need the user name field in the form anymore, we can change that form class in `reviews/forms.py` as follows.  

```python
class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': Textarea(attrs={'cols': 40, 'rows': 15}),
        }
```

![enter image description here](https://www.filepicker.io/api/file/8BxGwNsRFyj6ovKVhU8w "enter image title here")  

If the user is not logged in, the user will be redirected to a login page. You can try this by logging out from the admin page and then attempting to add a wine review.

If you try that, you will see a `Page not found (404)` error since we did not define a URL mapping to the login page request and also did not define a template for it. Also notice that the URL you are redirected to includes a `next=...` param that will be the destination page after we login properly.  

### Login views  

Django provides several views that you can use for handling login, logout, and password management. We will use them here. So first things first. Change the `urlpatterns` list in `winerama/urls.py` and leave it as follows.  

```python
urlpatterns = [
    url(r'^reviews/', include('reviews.urls', namespace="reviews")),
    url(r'^admin/', include(admin.site.urls)),
    url('^accounts/', include('django.contrib.auth.urls'))
]
```

We just imported all the mappings from `django.contrib.auth.urls`. Now we need templates for different user management web pages. They need to be placed in `templates/registration` in the root folder for our Django project. 

For example, create there a `login.html` template with the following code:

```python
{% extends 'base.html' %}
{% load bootstrap3 %}


{% block title %}
<h2>Login</h2>
{% endblock %}

{% block content %}
<form action="{% url 'auth:login' %}" method="post" class="form">
    {% csrf_token %}
    {% bootstrap_form form layout='inline' %}
    {% buttons %}
    <button type="submit" class="btn btn-primary">
      {% bootstrap_icon "user" %} Login
    </button>
    {% endbuttons %}
</form>
{% endblock %}
```

In order for our templates to be available, we need to change the `TEMPLATES` list in `winerama/settings.py` to include that folder.  

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

![enter image description here](https://www.filepicker.io/api/file/GIDUizvWRYeA8zRPiWzS "enter image title here")

We need to create templates for each user management view. In this section we will just provide two: `templates/registration/login.html` and 'templates/registration/logged_out.html'. We will also move the `reviews/templates/reviews/base.html` template to the main `templates/base.html` folder so it can be used all across the project. Therefore we need to update all the template directives {% extend ... %} that were making use of it. 

Check the [GitHub repo](https://github.com/jadianes/winerama-recommender-tutorial/tree/stage-1.1) to see how the html templates need to look like.  

### Adding session controls 

The next thing we need to do is to provide the login and logout buttons in our menu. Go to `templates/base.html` and modify the `<nav>` element in the template that contains the navigation menu so it looks like the following.  

```python
<nav class="navbar navbar-default">
    <div class="navbar-header">
        <a class="navbar-brand" href="{% url 'reviews:review_list' %}">Winerama</a>
    </div>
    <div id="navbar" class="navbar-collapse collapse">
        <ul class="nav navbar-nav">
            <li><a href="{% url 'reviews:wine_list' %}">Wine list</a></li>
            <li><a href="{% url 'reviews:review_list' %}">Home</a></li>
        </ul>
        <ul class="nav navbar-nav navbar-right">
        {% if user.is_authenticated %}
            <li><a href="{% url 'auth:logout' %}">Logout</a></li>
            {% else %}
            <li><a href="{% url 'auth:login' %}">Login</a></li>
            {% endif %}
        </ul>
    </div>
</nav>
``` 

The important part here is how we make use of the context object `user.is_authenticated` within a `{% if %}` expression in order to show the right menu elements. When the user is logged in, we show the logout button and vice versa.  

If you gave it a try, you probably noticed that, when logging in through the menu, we'd get a 404 error when we try to navigate to the user profile page. That's fine. We haven't provided a user profile page yet. We will solve this issue in the next section. 

Again, this point of the project corresponds to the git tag [`stage-1.1`](https://github.com/jadianes/winerama-recommender-tutorial/tree/stage-1.1). 

## User Profile Page

Actually our user profile will consist of a list of reviews by the logged in user. In order to accomplish that, we will need a few things:  

- We need to define the default mapping for the landing page after login (when a `next` param is not provided).  
- Then we need to define a mapping for the new view we are going to add.  
- We need to define a view function that returns reviews given by a user.  
- We need to define a template to render the result of the previous view. 
- We need to create a menu item for this.   

Let's start by defining the default mapping. This is done at project configuration level. Go to `winerama/settings.py` and add the following line.  

```python
LOGIN_REDIRECT_URL = '/reviews/review/user'
```

Now we need to define the mappings in `reviews/urls.py` as follows.  

```python
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
    # ex: /review/user - get reviews for the logged user
    url(r'^review/user/(?P<username>\w+)/$', views.user_review_list, name='user_review_list'),
    url(r'^review/user/$', views.user_review_list, name='user_review_list'),   
]
```

We specify two mappings. One is used when a username is passed, and the other one when it is not. The new view needs a function in `reviews/views.py`, names `user_review_list` as defined in the url mapping. Add the following to your view file.  

```python
def user_review_list(request, username=None):
    if not username:
        username = request.user.username
    latest_review_list = Review.objects.filter(user_name=username).order_by('-pub_date')
    context = {'latest_review_list':latest_review_list, 'username':username}
    return render(request, 'reviews/user_review_list.html', context)
```

As you see, we just added a filter to the code we used in the latest reviews list, and then we used a new template name `user_review_list.html`. We could have used the existing template for `review_list.html`, but we want to change the title to something more user-specific. Finally, we can decide whether or not to require users to login for this view. If not (like we did), user reviews are public, so users who are not logged in can view them as well.   

Next, we need to create the template as follows.  

```python
{% extends 'reviews/review_list.html' %}

{% block title %}
<h2>Reviews by {{ user.username }}</h2>
{% endblock %}
```  

That is, we extend the `review_list.html` template and just define the `{% block title %}` in order to replace the title with the one including the user name.  

Finally, let's add the menu item for the new view. We want a link that says **Hello USER_NAME** next to the **logout** menu item. Go and change the `<nav>` element in `templates/base.html` so it looks like the following.   

```python  
<nav class="navbar navbar-default">
    <div class="navbar-header">
        <a class="navbar-brand" href="{% url 'reviews:review_list' %}">Winerama</a>
    </div>
    <div id="navbar" class="navbar-collapse collapse">
        <ul class="nav navbar-nav">
            <li><a href="{% url 'reviews:wine_list' %}">Wine list</a></li>
            <li><a href="{% url 'reviews:review_list' %}">Home</a></li>
        </ul>
        <ul class="nav navbar-nav navbar-right">
        {% if user.is_authenticated %}
            <li><a href="{% url 'reviews:user_review_list' user.username %}">Hello {{ user.username }}</a></li>
            <li><a href="{% url 'auth:logout' %}">Logout</a></li>
            {% else %}
            <li><a href="{% url 'auth:login' %}">Login</a></li>
            {% endif %}
        </ul>
    </div>
</nav>
```    

![center](https://www.filepicker.io/api/file/o36iZvM4RcPjrbFeUOSV "enter image title here")

Finally, we want to be able to navigate to other users reviews pages. For example, when we see the name of a user under a wine review, we want to be able to click the name and go to that user reviews page. This means that we need to update `review_list.html` and `review_detail.html` templates and replace the user name text with a `<a>` element as follows (this is the `reviews_detail.html` template).

```python
{% extends 'base.html' %}

{% block title %}
<h2><a href="{% url 'reviews:wine_detail' review.wine.id %}">{{ review.wine.name }}</a></h2>
{% endblock %}

{% block content %}
<h4>Rated {{ review.rating }} of 5 by <a href="{% url 'reviews:user_review_list' review.user_name %}" >{{ review.user_name }}</a></h4>
<p>{{ review.pub_date }}</p>
<p>{{ review.comment }}</p>
{% endblock %}
```

You can go to the [`stage-1.2`](https://github.com/jadianes/winerama-recommender-tutorial/tree/stage-1.2) to see how these files look like after the updates.  

And that's it. We have created a proper user landing page. It is the same as the reviews list but filtered to include just this user reviews. This view can also be used to check a specific user reviews. This point of the project corresponds to the git tag [`stage-1.2`](https://github.com/jadianes/winerama-recommender-tutorial/tree/stage-1.2). 

## Registration page

We already have the capability to create users, but only through the admin interface (or using code). What we want is for an unregistered user to be able to sign up and create their own user account. We could create forms and views to do this, but there is a very nice [Django registration app](https://github.com/macropin/django-registration) that we can install and use for this.   

Let's start by installing the application package using our Anaconda pip as follows. Assuming we are at the folder containing the anaconda installation:    

```bash
./anaconda/bin/pip install django-registration-redux
```

If everything goes well, we need to add the app to the `INSTALLED_APPS` list in `winerama/settings.py` as follows:  

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
    'registration',
)
```

Add also the following values to the settings file.  

```python
ACCOUNT_ACTIVATION_DAYS = 7 # One-week activation window
REGISTRATION_AUTO_LOGIN = True # Automatically log the user in.
```

Once we have done this, we need to install the model used by the default setup. From the terminal at the project root, run the following.  

```bash
python manage.py makemigrations
```

And then  

```bash
pythonmanage.py migrate
```

The application includes different user management views, but we want to use just the registration ones. Set the following in the `winerama/urls.py` file.  

```python
urlpatterns = [
    url(r'^reviews/', include('reviews.urls', namespace="reviews")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls', namespace="auth")),
    
]
```

We need to provide two templates that will replace the default ones. We want ours to be more in line with our site's style. They are `templates/registration/registration_form.html' and 'templates/registration/registration_complete.html'. The first one looks like this.  

```python
{% extends 'base.html' %}
{% load bootstrap3 %}


{% block title %}
<h2>Register</h2>
{% endblock %}

{% block content %}
<form method="post" class="form">
    {% csrf_token %}
    {% bootstrap_form form layout='inline' %}
    {% buttons %}
    <button type="submit" class="btn btn-primary">
      {% bootstrap_icon "user" %} Register
    </button>
    {% endbuttons %}
</form>
{% endblock %}
```
![enter image description here](https://www.filepicker.io/api/file/sR5EY4BpQk6WoGqGT0Jr "enter image title here")

There we just follow the same structure that we used for the login template. Nothing special. The one for registration complete looks like this.  

```python
{% extends 'base.html' %}
{% load bootstrap3 %}


{% block title %}
<h2>Register</h2>
{% endblock %}

{% block content %}
Thanks for registering!
{% endblock %}
```
![enter image description here](https://www.filepicker.io/api/file/vWFOpYyBTZCIzE5bGJEK "enter image title here")

They have to be named that way and be located in the main `templates/registration` folder for `django-registration` to find them.  

We have just used the simplest approach to building a user registration feature. If you are interested in a more complex (and production-ready) approach, for example sending activation/confirmation emails to the user or password recovery/reset views, have a look at the [Django registration docs](https://django-registration-redux.readthedocs.org/en/latest/index.html). The main issue with using them in this tutorial is that they involve using an email server and that's not very related with what we want to teach here.  

This point of the project corresponds to the git tag [`stage-2`](https://github.com/jadianes/winerama-recommender-tutorial/tree/stage-2) of the project repo. 


## Conclusions  

In this part of the tutorial, we have introduced users and user management into our Django app. By requiring users to register, we will be able to gather better user statistics, and this is a fundamental step into building a user-based recommender.  

However our user management was very naive and simple. There are many issues we would need to tackle if we want to take this system into production, such as providing a two-step activation process for user accounts, checking whether an email has been previously used, or even allowing users to sign up with their social accounts.  

But what we did so far is enough for our final goal, that is to show how a web site can include a recommender system and what is its workflow when gathering user data. Our ultimate goal is to build models to provide recommendations. This is going to be the purpose of the third and last part of our tutorial.  

Remember that you can follow the tutorial at any development stage by forking [the repo](https://github.com/jadianes/winerama-recommender-tutorial) into your own GitHub account, and then cloning into your workspace and checking out the appropriate tag. By forking the repo you are free to change it as you like and experiment with it as much as you need. If at any point you feel like having a little bit of help with some step of the tutorial, or with making it your own, we can have a [1:1 Codementor session](https://www.codementor.io/jadianes) about it.
