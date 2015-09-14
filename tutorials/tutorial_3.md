# Providing wine suggestions  

This is the third part of our tutorial on how to build a web-based wine review and recommendation system using Python technologies such as [Django](https://www.djangoproject.com/), [Pandas](http://pandas.pydata.org/), [SciPy](http://www.scipy.org/), and [Scikit-learn](http://scikit-learn.org/). 

In the [first tutorial](https://www.codementor.io/python/tutorial/get-started-with-django-building-recommendation-review-app), we started a Django project and a Django app for our Wine recommender web application. The whole thing will be an incremental process that can be followed by checking out individual tags in our [GitHub repo](https://github.com/jadianes/winerama-recommender-tutorial). By doing so, you can work in those individual tasks at a given stage that you find more interesting or difficult. 

In this [second tutorial](https://www.codementor.io/python/tutorial/build-data-product-django-user-management), we added user management. This was an important part. Now we are able to identify individual users, and we are finally ready to generate user recommendations through machine learning. 

So this third part will show how to use machine learning to provide wine recommendations for our website users. In the first section, we will use Pandas to load data from CSV files. By doing so, we will have some pre-generated data we will use to create our models. Then, in the second section, we will use a naive recommendation criteria so we can better concentrate on building the views and models needed to provide recommendations. We will finish the tutorial by using [K-means](https://en.wikipedia.org/wiki/K-means_clustering) clustering as a machine learning model that makes use of user similarity in order to provide better wine recommendations.  

Remember that you can follow the tutorial at any development stage by forking [the repo](https://github.com/jadianes/winerama-recommender-tutorial) into your own GitHub account, and then cloning it into your workspace and checking out the appropriate tag. By forking the repo, you are free to change it as you like and experiment with it as much as you need. If at any point you feel like having a little bit of help with some step of the tutorial, or with making it your own, we can have a [1:1 Codementor session](https://www.codementor.io/jadianes) about it.  

## Importing data from CSV using Pandas  

In this section, we will use Pandas to load data from CSV files. By doing so, we will have some pre-generated data we will use to create our models. We will use up to three different CSV files and their respective importers. They will deal with users, wines, and reviews respectively.  

Data files are just comma-separated files or CSV. For example, this is how the `reviews.csv` file looks like:  

```
id,username,wine_id,rating,comment
0,jadianes,0,4,Beautiful Manzanilla. Great price.
1,jadianes,1,3,Classy Rose. Not great.
2,jadianes,3,4,This can be great with time.
3,jadianes,9,2,Drinkable...
4,jadianes,10,5,A treasure of a wine
5,john,0,2,Tastes like old wine
6,john,1,4,Love it... Luxury!
7,john,3,2,Not a big fan of sweets
8,john,9,3,Could drink this more often... Love the fruit.
9,john,10,2,"too strong, sorry"
10,john,7,4,Powerful and elegant. Masculine.
11,mari,0,3,It reminds me of Sanlucar :)
12,mari,1,2,Not a big fan of bubbles
13,mari,3,5,Love sweets!
14,mari,4,5,The best white wine I ever had.
15,yasset,0,4,It is good
16,yasset,1,2,I don't like champagne
17,yasset,3,1,I don't like sweet wine
18,yasset,4,4,Very good wine.
19,yasset,6,5,So good wine
20,carlos,0,4,Se sale
21,carlos,3,4,Viva Malaga
22,carlos,7,5,Wonderful
23,teus,0,4,This is very special wine
24,teus,10,5,Wow!
25,teus,3,5,"Hey, this is great stuff!"
26,teus,5,4,This is going to be in my memory for a very long time
27,lluis,0,4,"Chalk, almonds, rain"
28,lluis,2,4,"Dry fruit, lead, iron, dry flowers."
29,lluis,5,5,"Rioja, rioja, rioja"
30,lluis,8,4,"God!"
31,pepe,10,5,"Jooe!"
32,pepe,6,4,"Vega Siclia..."
33,pepe,0,4,"Esto y unas gambitas!"
34,pepe,1,2,"No esta mal"
35,pepe,2,4,"Muy bueno"
```

The file should be self-explanatory, since the first row contains the field names. Each file row is a wine review that we want to put into our database. We have a review ID, a name for the user making this review, a wine id (that cross-links with the file `wine.csv`), a rating, and a comment.  

In order to read the file we use [Pandas](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_csv.html) dataframe method `read_csv`. Then we will use [`apply`](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.apply.html) over each row in the data frame and create a `Review` instance using our review model objects. But we better have a look at the code.  

```python
import sys, os 
import pandas as pd
import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "winerama.settings")

import django
django.setup()

from reviews.models import Review, Wine 


def save_review_from_row(review_row):
    review = Review()
    review.id = review_row[0]
    review.user_name = review_row[1]
    review.wine = Wine.objects.get(id=review_row[2])
    review.rating = review_row[3]
    review.pub_date = datetime.datetime.now()
    review.comment = review_row[4]
    review.save()
    
    
# the main function for the script, called by the shell    
if __name__ == "__main__":
    
    # Check number of arguments (including the command name)
    if len(sys.argv) == 2:
        print "Reading from file " + str(sys.argv[1])
        reviews_df = pd.read_csv(sys.argv[1])
        print reviews_df

        # apply save_review_from_row to each review in the data frame
        reviews_df.apply(
            save_review_from_row,
            axis=1
        )

        print "There are {} reviews in DB".format(Review.objects.count())
        
    else:
        print "Please, provide Reviews file path"

```

The script starts by checking the argument length and then creating the dataframe using `read_csv` as described. Then, we print the data frame contents and apply the `save_review_from_row` function over `axis=1` (per row). The function is defined before, and basically uses `review.models.Review` to create a new review instance from the row data. Pay attention to how we use the wine id to look for the wine instance in `Wine.objects.get(id=review_row[2])`. This means that we need to load wines before we load reviews. We should also load users before the reviews, but since we aren't referencing User objects from reviews but using user names directly, this is not mandatory.  

The other two data files and scripts are equivalent, and it is better if you have a look at the repo and understand them. Put the three scripts at the root of the project (side by side with `manage.py`) and the data files in a folder named `data` under the project root. Then we need to run each script as follows.  

```bash
python load_users.py data/users.csv
```

```bash
python load_wines.py data/wines.csv
```

```bash
python load_reviews.py data/reviews.csv
```

If everything goes well (you will see some warnings), the last lines of each script prints the number of entries in the database. There should be consistent with the number of entries in the `csv` files, plus one user because of the `admin` user.  

This stage of the project corresponds to the tag [stage-2.1](https://github.com/jadianes/winerama-recommender-tutorial/tree/stage-2.1).  

## Creating a Recommendations View with a Base Model  

In this section, we are going to do two things. First we will create a Django view to obtain a list of wine recommendations for a given user. This view will require users to be logged in. Secondly, we will define a very basic model to generate these recommendations that simply returns wines not reviewed by that user. Once we have these two things in place, we will have the basic structure to implement more complex models.  

### A recommendations view  

We have done these several times. Just go to `views.py` and add the following function.  

```python

@login_required
def user_recommendation_list(request):
    return render(request, 'reviews/user_recommendation_list.html', {'username': request.user.username})

```

As you see, this view just renders the template `reviews/user_recommendation_list.html` and passes the request username. The template we render is just an extension of the wine list one as you can see.  

```python
{% extends 'reviews/wine_list.html' %}

{% block title %}
<h2>Recommendations for {{ username }}</h2>
{% endblock %}

```

We just redefine the title of the original wine list template to render the username. Later on, we will modify the view function to also pass a wine list so the template can render it. But first let's add a URL mapping in `reviews/urls.py` so it looks as follows.  

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
    # ex: /review/user - get reviews for the logged user
    url(r'^review/user/(?P<username>\w+)/$', views.user_review_list, name='user_review_list'),
    # ex: /review/user - get reviews for the user passed in the url
    url(r'^review/user/$', views.user_review_list, name='user_review_list'),
    # ex: /recommendation - get wine recommendations for the logged user
    url(r'^recommendation/$', views.user_recommendation_list, name='user_recommendation_list'),
]
```

Our new mapping maps the URL `recommendation/` to the view we have just defined in `views.py`.  

Finally, let's add a link in the menu bar so a logged user can go to its recommendations. Go and change the `<nav>`  element in `templates/base.html` to look like the following.  

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
                <li><a href="{% url 'reviews:user_recommendation_list' %}">Wine suggestions</a></li>
                <li><a href="{% url 'auth:logout' %}">Logout</a></li>
                {% else %}
                <li><a href="{% url 'auth:login' %}">Login</a></li>
                <li><a href="/accounts/register">Register</a></li>
                {% endif %}
            </ul>
        </div>
    </nav>
```

![enter image description here](https://www.filepicker.io/api/file/JVXNJ4cLRlyvU9v123Ay "enter image title here")

We have added a new link to be displayed when a user is logged in. If that is the case, a **Wine suggestions** menu item will allow the user to navigate to the view we have just implemented.  

This stage of the project corresponds to the tag [stage-2.2](https://github.com/jadianes/winerama-recommender-tutorial/tree/stage-2.2).  

### Returning wines not reviewed by the user  

A first, a not very clever recommendation engine can just return wines a user has never reviewed before. It will be the equivalent to a totally ignorant wine store clerk who, when asked to recommend a wine for tonight's dinner, first inquires what have we tried and then suggests something with a different name without really considering the wine style or our taste.  

We can do this very easily within our `user_recommendation_list` as follows.  

```python
@login_required
def user_recommendation_list(request):
    # get this user reviews
    user_reviews = Review.objects.filter(user_name=request.user.username).prefetch_related('wine')
    # from the reviews, get a set of wine IDs
    user_reviews_wine_ids = set(map(lambda x: x.wine.id, user_reviews))
    # then get a wine list excluding the previous IDs
    wine_list = Wine.objects.exclude(id__in=user_reviews_wine_ids)

    return render(
        request, 
        'reviews/user_recommendation_list.html', 
        {'username': request.user.username,'wine_list': wine_list}
    )
```

This requires a bit of explanation. First we create a query set for all the reviews for the current user. We also prefetch wine objects in order to avoid successive queries for each review, since we will need to access these wine objects (more about [`prefetch_related`](https://docs.djangoproject.com/en/1.8/ref/models/querysets/#prefetch-related)). Then we create a set of all the different wine IDs using `map` to apply a lambda expression to each review in the previous result and get the wine ID. And finally, we create a new query set of `Wine` excluding all the previous IDs. The important bit here is how we subfixed the `id` field with `__in` in order to implement the SQL `IN` functionality. More on this [here](https://docs.djangoproject.com/en/1.8/ref/models/querysets/#in). The resulting list is what we pass to our template rendering. Powerful, isn't it?  


## Using k-means clustering to provide better recommendations  

What we have done so far in terms of wine recommendations is not especially impressive. Any of us can try to impress a friend by recommending a wine we recently tried and she did not. Many times we do that without really knowing our friend's preferences and therefore without really knowing if she will enjoy our recommendations. 

There are at least two other ways we can make recommendations that improve the previous naive approach. Both of them require us to know our friend's preferences. In the first approach, we ask her to tell us a few wines she liked and, based on our knowledge about these wines, we recommend her wines that are similar. This requires a good amount of knowledge about wine. It is what a good and experienced wine store owner would do, and suggestions are hard to improve by a computer that follows the same approach due to many unknown factors that are involved in this kind of customer relationship.   

There is a second approach that doesn't require any knowledge about wine, but one only needs to know what other people like and dislike (and not just that of our friend/customer). With that knowledge, we just try to find a person with similar preferences to our friend. Then we ask that second person for her favourite wines and suggest them to our first friend, not including those that our first friend have already tried. We just act as an intermediary, and a computer system here can do the job better than any human being since it can "ask" millions of people in short time.  

This is what our system will do, and we will use clustering for that. Why? Simple. Instead of trying to compare our user to every other user in the system every time recommendations are needed, we will pre-cluster all the users in the system by its wine reviews scores. By doing so we will have groups of similar users. Then, when a user asks for recommendations, we will look for them just in the cluster this user is clustered in. Since we know all the users in that cluster have a similar taste (they scored similarly the same wines, for good or bad), this greatly reduces the search space.  

Of course there are more sophisticated recommender systems (e.g. collaborative filtering using ALS), but this one is easy to understand in terms of its meaning and makes use of some machine learning techniques we already know about.  

This stage of the project corresponds to the tag [stage-2.3](https://github.com/jadianes/winerama-recommender-tutorial/tree/stage-2.3).  


### Creating a model object to store clustering information  

In order to implement the previously mentioned approach, we need to keep track of the cluster a user belongs to. By doing so, we will be able to filter the view we already have (the one returning wines not reviewed by the user) by cluster ID and sort them by score. If we assume the cluster ID has been previously assigned by our clustering algorithm, this whole process will give us wine suggestions that satisfy two conditions:  

- The requesting user has never reviewed those wines.  
- The wines have been reviewed positively by users within our cluster, that tend to score wines the same way we do (have similar taste).  

We could store this together with the rest of the user's information, but in order to do that we would need to provide a custom user object. In addition, if we do so we'd need to reconstruct all the database tables related to authentication (this process doesn't support migrations) and this is a major restructuration of our system. So, as a workaround we will create a new model object `UserCluster` that stores references to the user objects.  

Go to our `reviews/models.py` and add the following class.  

```python
class Cluster(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User)

    def get_members(self):
        return "\n".join([u.username for u in self.users.all()])
```

For a cluster, we store a name and a list of users. We leave the door open for users to belong to more than one cluster by using that `ManyToManyField`. We also define a method to get all the member user names `get_memebers`.  

Since we have modified our model layer, we need to migrate the database tables. From the project root folder run the following two commands.  

```bash
python manage.py makemigrations
```

and  

```bash
python manage.py migrate
```  

And although it won't be the main tool to manage cluster information, we are goind to add the model class to our admin interface. Edit the `reviews/admin.py` file so it looks like the following.  

```python
from django.contrib import admin

from .models import Wine, Review, Cluster

class ReviewAdmin(admin.ModelAdmin):
    model = Review
    list_display = ('wine', 'rating', 'user_name', 'comment', 'pub_date')
    list_filter = ['pub_date', 'user_name']
    search_fields = ['comment']
    

class ClusterAdmin(admin.ModelAdmin):
    model = Cluster
    list_display = ['name', 'get_members']

    
admin.site.register(Wine)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Cluster, ClusterAdmin)
```

We have just imported and registered the model class `Cluster`, and associated a `ClusterAdmin` class that will better visualise cluster information (name and members) in the admin interface. So, go to the admin interface and create three clusters with the following members from the users we have available:  

- 1: jadianes, carlos, and lluis  
- 2: john, teus, yasset  
- 3: pepe, mari  

If you have problems with this, just checkout the tag for this stage of the project that is [stage-2.4](https://github.com/jadianes/winerama-recommender-tutorial/tree/stage-2.4) and contains all the previous code and the information in the database.  

### Making use of cluster information in the recommendations view  

Now is time to change our `user_recommendation_list` view so it makes use of the cluster information.  

```python
@login_required
def user_recommendation_list(request):
    
    # get request user reviewed wines
    user_reviews = Review.objects.filter(user_name=request.user.username).prefetch_related('wine')
    user_reviews_wine_ids = set(map(lambda x: x.wine.id, user_reviews))

    # get request user cluster name (just the first one righ now)
    user_cluster_name = \
        User.objects.get(username=request.user.username).cluster_set.first().name
    
    # get usernames for other members of the cluster
    user_cluster_other_members = \
        Cluster.objects.get(name=user_cluster_name).users \
            .exclude(username=request.user.username).all()
    other_members_usernames = set(map(lambda x: x.username, user_cluster_other_members))

    # get reviews by those users, excluding wines reviewed by the request user
    other_users_reviews = \
        Review.objects.filter(user_name__in=other_members_usernames) \
            .exclude(wine__id__in=user_reviews_wine_ids)
    other_users_reviews_wine_ids = set(map(lambda x: x.wine.id, other_users_reviews))
    
    # then get a wine list including the previous IDs, order by rating
    wine_list = sorted(
        list(Wine.objects.filter(id__in=other_users_reviews_wine_ids)), 
        key=lambda x: x.average_rating, 
        reverse=True
    )

    return render(
        request, 
        'reviews/user_recommendation_list.html', 
        {'username': request.user.username,'wine_list': wine_list}
    )
```

There is a lot going on here:  

1.  First we get a list of wine IDs reviewed by the requester user, like we did before.  
2.  Then we obtain the name of the cluster the user belongs to. We do this through the `User.objects.get(..).cluster_set` field that references the user side of the many-to-many relationship we have with clusters. We also exclude the requester user from that list. This is not strictly needed because of what we are going to do next, but might reduce query time.    
3.  Then we use the previous list of names to get reviews for those users in the cluster, excluding those reviews referring to the wines we got in step 1. From the result, we get a list of wine IDs.    
4.  Finally, we use the previous list of IDs to retrieve all the wines and sort them by average rate.  

We are ready now to navigate to our wine suggestions page and see something that makes use of user similarity. We just need to generate these clusters using k-means and not manually, and we are done!  

This stage of the tutorial corresponds to the tag [stage-2.5](https://github.com/jadianes/winerama-recommender-tutorial/tree/stage-2.4).  


### Clustering users    

So this is the last step in order to make our system provide suggestions based on user similarity. Regarding the user interface, we have everything in place thanks to the previous sections' work. We just need to tweak the view layer a little in order to decide when to perform the k-means clustering, and then we need to write the actual clustering code. If you want to learn more about k-means clustering in Python, have a look at our tutorial on [how to do it with R and Python](https://www.codementor.io/python/tutorial/data-science-python-pandas-r-dimensionality-reduction).    

So first things first. When do we compute which cluster a user belongs to? Let's put at least a couple of restrictions:  

- We want to compute new cluster assignments when new user preferences (wine reviews) comes into the system.  
- We don't want to update cluster assignments too often. This website of ours is one with potentially many users adding wine reviews. If we compute new clusters with every new review coming in, we are going to have scalability problems. Therefore, we must find some kind of tradeoff between using recent information and not stressing the system too much.  

The first restriction can be satisfied if we call for cluster assignments update within the view that handles adding wine reviews. So let's edit the `reviews/views/py` file so the `add_review` method looks like the following.  

```python
@login_required
def add_review(request, wine_id):
    wine = get_object_or_404(Wine, pk=wine_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        rating = form.cleaned_data['rating']
        comment = form.cleaned_data['comment']
        user_name = request.user.username
        review = Review()
        review.wine = wine
        review.user_name = user_name
        review.rating = rating
        review.comment = comment
        review.pub_date = datetime.datetime.now()
        review.save()
        update_clusters()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('reviews:wine_detail', args=(wine.id,)))
    
    return render(request, 'reviews/wine_detail.html', {'wine': wine, 'form': form})
    
```

If we compare with the previous version, we can see that we have just added a call to `update_clusters()`. This is a new function we will define in a separate `reviews/suggestions.py` file, and we need to import it. Therefore, add the following import in `reviews/views.py`.  

```python
from .suggestions import update_clusters
```

And then create and edit the file `reviews/suggestions.py` so it looks as follows.  


```python
from .models import Review, Wine, Cluster
from django.contrib.auth.models import User
from sklearn.cluster import KMeans
from scipy.sparse import dok_matrix, csr_matrix
import numpy as np

def update_clusters():
    num_reviews = Review.objects.count()
    update_step = ((num_reviews/100)+1) * 5
    if num_reviews % update_step == 0: # using some magic numbers here, sorry...
        # Create a sparse matrix from user reviews
        all_user_names = map(lambda x: x.username, User.objects.only("username"))
        all_wine_ids = set(map(lambda x: x.wine.id, Review.objects.only("wine")))
        num_users = len(all_user_names)
        ratings_m = dok_matrix((num_users, max(all_wine_ids)+1), dtype=np.float32)
        for i in range(num_users): # each user corresponds to a row, in the order of all_user_names
            user_reviews = Review.objects.filter(user_name=all_user_names[i])
            for user_review in user_reviews:
                ratings_m[i,user_review.wine.id] = user_review.rating

        # Perform kmeans clustering
        k = int(num_users / 10) + 2
        kmeans = KMeans(n_clusters=k)
        clustering = kmeans.fit(ratings_m.tocsr())
        
        # Update clusters
        Cluster.objects.all().delete()
        new_clusters = {i: Cluster(name=i) for i in range(k)}
        for cluster in new_clusters.values(): # clusters need to be saved before referring to users
            cluster.save()
        for i,cluster_label in enumerate(clustering.labels_):
            new_clusters[cluster_label].users.add(User.objects.get(username=all_user_names[i]))
```

Let's explain the clustering process. The `update_clusters` function performs cluster assignment in three steps, and only updates if the number of total reviews in the system satisfies a certain equation (more on that later on):  

1. Create a sparse matrix using user reviews ratings. This matrix is needed to perform k-means clustering. In order to build the matrix we need to obtain:  
  - Get a list of user names. We will have a row for each user in our matrix.  
  - Get a list of unique wine IDs. We will have a column for each wine in our matrix.  
  - Each element (i,j) in our matrix contains the rating of user i for wine j. The username for user i will be given by the position of that name in our user names list.  
  - Notice that we make use of the class [`dok_matrix`](http://docs.scipy.org/doc/scipy-0.15.1/reference/generated/scipy.sparse.dok_matrix.html) from `scipy` in order to easily build a sparse matrix. Read the documentation if you want to learn more about it. Our code is not complex at all and just inits the matrix with the right dimensions and then assigns the ratings to the right elements.    
2.  Perform k-means clustering. Some remarks:  
  - Here we use some magic numbers in order to have at least three clusters or more. The total number will depend on how many users divided by 10 we have in the system. This is far from being based on actual cluster structure, and should be improved in a production system. We are just assuming that the more users we have, the more likely they will have different tastes. 
  - Notice also that we convert our `dok_matrix` into a [`csr_matrix`](http://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csr_matrix.html) that is better for the calculations needed in k-means clustering.  
3.  Finally, we update cluster assignments in our database. In order to do that:  
  - First we delete all the previous clusters.  
  - Then we create and save new clusters, with no user assignments. We need them saved if we want to instantiate many-to-many relationships with the users in the next step.  
  - For each label assignment in the k-means clustering results, we add a user to the right cluster. Django will automatically save the [many-to-many relationship](https://docs.djangoproject.com/en/1.8/topics/db/examples/many_to_many/).   

We are almost there. We just need a small update in our "get suggestions" view. In the case where no cluster assignment has been done (e.g. a new user is registered into the system), we need to catch that situation and call our new `update_clusters` method. Go and edit `reviews/views.py` so the method `user_recommendation_list` looks like the following:  

```python
@login_required
def user_recommendation_list(request):
    
    # get request user reviewed wines
    user_reviews = Review.objects.filter(user_name=request.user.username).prefetch_related('wine')
    user_reviews_wine_ids = set(map(lambda x: x.wine.id, user_reviews))

    # get request user cluster name (just the first one righ now)
    try:
        user_cluster_name = \
            User.objects.get(username=request.user.username).cluster_set.first().name
    except: # if no cluster has been assigned for a user, update clusters
        update_clusters()
        user_cluster_name = \
            User.objects.get(username=request.user.username).cluster_set.first().name
    
    # get usernames for other memebers of the cluster
    user_cluster_other_members = \
        Cluster.objects.get(name=user_cluster_name).users \
            .exclude(username=request.user.username).all()
    other_members_usernames = set(map(lambda x: x.username, user_cluster_other_members))

    # get reviews by those users, excluding wines reviewed by the request user
    other_users_reviews = \
        Review.objects.filter(user_name__in=other_members_usernames) \
            .exclude(wine__id__in=user_reviews_wine_ids)
    other_users_reviews_wine_ids = set(map(lambda x: x.wine.id, other_users_reviews))
    
    # then get a wine list including the previous IDs, order by rating
    wine_list = sorted(
        list(Wine.objects.filter(id__in=other_users_reviews_wine_ids)), 
        key=lambda x: x.average_rating, 
        reverse=True
    )

    return render(
        request, 
        'reviews/user_recommendation_list.html', 
        {'username': request.user.username,'wine_list': wine_list}
    )

```

Basically, we have added a `try-except` clause in order to deal with non existing cluster assignments for a user when getting the first cluster. In that case, we first call `update_clusters` and then retrieve the cluster again.  

So we are ready to give it a try. Our approach has some limitations. One of them being that if a user has more than one review for the same wine, only one of them will be used. Another limitation is that the whole thing works better if there are a few wines that have been reviewed by as many users as possible. They will be the equivalent to very popular wines that most people know about, or very popular classic movies if we were building a movies site. Actually, if you have ever used sites like Netflix, you would have noticed that they make you go though a series of movies for you to rate even before completing your registration process. In our case we will just load more data using our data loading scripts. We have added a bunch more reviews into our `data/reviews.csv` file. Either you check out the latest tag in the repo [stage-3](https://github.com/jadianes/winerama-recommender-tutorial/tree/stage-3) - and in that case you will have the data in the database already - or you get (even copy and paste will work) [that individual file](https://github.com/jadianes/winerama-recommender-tutorial/blob/stage-3/winerama/data/reviews.csv) to replace the previous `data/reviews/csv`. If you do that, you will also need to load the data by running:  

```bash
python load_reviews.py data/reviews.csv
```

This stage of the tutorial corresponds to the tag [stage-3](https://github.com/jadianes/winerama-recommender-tutorial/tree/stage-3).  


## Conclusions

So that is it for today. In this third tutorial, we explained how to provide wine recommendations for our website users. We have done so by incrementally building the required models and views around a very basic recommendations engine. Then we used K-means clustering as a machine learning model that made use of user similarity in order to provide better wine recommendations. Our model will perform better with more user reviews, so build yours and add friends to it to see how it behaves. By doing so, you will be able to overcome its limitations, improve its accuracy, and learn a lot!    

Maybe K-means is not the most usual machine learning model when building recommendation systems. However, it has some good characteristics. It is a fast clustering algorithm that has parallel and scalable implementations (e.g. see [Spark](http://spark.apache.org/docs/latest/mllib-clustering.html)). And overall, it is very easy to understand what K-means does and how it works. A user cluster is just a group of users close to each other based on how they rated items. For more sophisticated and popular alternatives, see our tutorial on [Spark and collaborative filtering](https://www.codementor.io/spark/tutorial/building-a-recommender-with-apache-spark-python-example-app-part1).  

Remember that you can follow the tutorial at any development stage by forking [the repo](https://github.com/jadianes/winerama-recommender-tutorial) into your own GitHub account, and then cloning it into your workspace and checking out the appropriate tag. By forking the repo you are free to change it as you like and experiment with it as much as you need. If at any point you feel like having a little bit of help with some step of the tutorial, or with making it your own, we can have a [1:1 Codementor session](https://www.codementor.io/jadianes) about it!  

