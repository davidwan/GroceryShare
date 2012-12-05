# Create your views here.
#HP Django stuff
from django import forms
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext

#HP app-specific stuff
from app.models import *
from app.forms import *
import settings, urls

#HP everything else
import os, sys, datetime, json
import json_parser
import facebook

# from bootstrap.forms import BootstrapModelForm, Fieldset

#HP:
def hackpackify(request, context):
  '''
  Updates a view's context to include variables expected in base.html
  Intended to make boilerplate info conveyance and menu bars quick and easy.
  and returns a RequestContext of the resulting dict (which is usually better).
  '''
  pages = ['Home', 'Person']
  for urlpat in urls.urlpatterns:
    if urlpat.__dict__.__contains__('name'):
      if '(' not in urlpat.regex.pattern:
        pages.append({'name':urlpat.name, 'url':urlpat.regex.pattern.replace('^','/').replace('$','')})
  #HP project_name is used in navbar, copyright (footer), about page, and <title>
  project_name = "Foodsharer" 
  #HP project_description is used in <meta name="description"> and the about page.
  project_description = "PennApps 2012 Project by Vivian Clara Abhishek Defu"
  #HP Founder information is in popups linked from the footers, the about page, and <meta name="author">
  founders = [
    {'name':'Vivian Huang',
       'email':'vivhuang@seas.upenn.edu',
       'url':'www.vivhuang.com',
       'blurb':'Hi, I\'m Vivian.',
       'picture':'http://profile.ak.fbcdn.net/hprofile-ak-ash2/273392_515004220_1419119046_n.jpg'},
    {'name': 'Clara Wu',
      'email': 'scwu@seas.upenn.edu',
      'url': 'www.clarawu.com',
      'blurb':'Hi, I\'m Clara.',
    },
    {'name':'Abhishek Gadiraju',
       'email':'agadi@seas.upenn.edu',
       'url':'',
       'blurb':'I like data science. And history. And soccer.',
       'picture':'http://a0.twimg.com/profile_images/2429388907/image.jpg'},
    {'name':'Defu Wan',
       'email':'gterrono@seas.upenn.edu',
       'url':'http://twitter.com/',
       'blurb':'I\'m Defu. I like webdev and most things Boston. And Dogs.',
       'picture':'http://chucknorri.com/wp-content/uploads/2011/03/Chuck-Norris-14.jpg'},
    ]
  hackpack_context = {
      'pages': pages,
      'project_name': project_name,
      'founders': founders,
      'project_description': project_description,
      }
  if not context.__contains__('hackpack'):
    #HP add the hackpack dict to the page's context
    context['hackpack'] = hackpack_context

  return RequestContext(request, context) #HP RequestContext is good practice. (I think).

def index(request):
  context = {
    'thispage': 'Index',
  }
  return render_to_response('index.html', hackpackify(request, context))


def about(request):
  context = {
    'thispage':'About',
  }
  return render_to_response('about.html', hackpackify(request, context))

def user_login(request, context):
  print "user login"
  user = facebook.get_user_from_cookie(request.COOKIES, '438894882828939', 
    '484028122fe1f70d55ea6d9be63859f2')

  print "after user"
  if user:
    graph = facebook.GraphAPI(user["access_token"])
    print "after graph"
    profile = graph.get_object("me")
    print "after profile"
    context['id'] = profile['id']
    print "after id"
    context['name'] = profile['name']
    print "after name"
    context['picture'] = graph.get_object("me/picture", type='large')['url']
    print "after picture"
    context['location'] = 'Philadelphia, PA'
    print "after location"
    context['school'] = 'University of Pennsylvania'
    print "after school"
    if User.objects.filter(user=context['id']).exists():
        print "beginning of if"
        pass
    else:
        print "beginning of else"
        u = User(user = context['id'], email = context['id'] + "@example.com",
            current_city = context['location'], current_location = context['school'],
            image = context['picture'])
        print "before save"
        u.save()
    print "before return"
    return graph
  else:
    return redirect('/')


def home(request):
  user = facebook.get_user_from_cookie(request.COOKIES, '438894882828939', '484028122fe1f70d55ea6d9be63859f2')
  context = {
    'thispage':'Home',
  }
  if user:
    graph = facebook.GraphAPI(user["access_token"])
    profile = graph.get_object("me")
    context['id'] = profile['id']
    context['email'] = profile['id']
    context['name'] = profile['name']
    context['picture'] = graph.get_object("me/picture", type='large')['url']
    context['location'] = 'Philadelphia, PA'
    context['school'] = 'University of Pennsylvania'
    if User.objects.filter(full_name=context['name']).exists():
        pass
    else:
        u = User(user = context['id'], full_name=context['name'], email = context['email'],
            current_city = context['location'], current_location = context['school'],
            image = context['picture'])
        u.save()
  else:
    return redirect('/')
  return render_to_response('home.html', hackpackify(request, context))

def match(request):
    all_users = User.objects.filter(current_location = 'University of Pennsylvania')
    graph = facebook.GraphAPI(user["access_token"])
    profile = graph.get_object("me")
    context['id'] = profile['id']
    recipe_self = User_Recipes.objects.filter(user=context['id]).filter(field__lookup=value)[0]
    for users in all_users:
        other_users = Users.objects.exclude(user = context['id']

    for o_user in other_users:
        id = User.objects.get().user
        recipe_other = User_Recipes.objects.filter(user=id).filter(field__lookup=value)[0]
        ingredients_other = Recipe.objects.filter(recipe_name=recipe_other).ingredients
        ingredients_self = Recipe.objects.filter(recipe_name=recipe_self).ingredients
        relations = {}
        list = []
        for ingre_o in ingredients_other:
            for ingre_s in ingredients_self:
                if ingre_o == ingre_s:
                    list.append(ingre_o)
        relations[User.objects.get().full_name] = list


    all_recipes_self = User_Recipes.objects.filter(user=context['id'])
    for recipe_self in all_recipes_self:
        ingredients_self = Recipe.objects.filter(recipe_name=recipe_self).ingredients
    for o_user in other_users:
        id = User.objects.get().user
        recipes_other = User_Recipes.objects.filter(user=id)
        for recipe_other in recipes_other:
            ingredients_other = Recipe.objects.filter(recipe_name=recipe_other).ingredients


def search(request):
  context = {
    'thispage': 'Search',
  }
  if 'query' in request.POST:
    results = list()
    dictionary = json_parser.get_recipe(str(request.POST['query']))
  else:
    dictionary = {}
    message = 'You submitted an empty form. Please go back to the search page'
  return render_to_response('results.html', { "vals" : dictionary.values})

def search(request):
  context = {
    'thispage': 'Search',
  }

  if 'query' in request.POST:
    results = list()
    recipes = json_parser.get_recipe(str(request.POST['query'])).values()
  else:
    recipes = []
    message = 'You submitted an empty form. Please go back to the search page'
  recipes = [{'recipe': recipe, 'json': json.dumps(recipe)} for recipe in recipes]
  return render_to_response('results.html', { "vals" : recipes})


def login(request):
  context = {
    'thispage': 'Login', 
    'STATIC_URL':'127.0.0.1:8000'
  }
  return render_to_response('login.html', hackpackify(request, context))


def addrecipe(request):
  print "add recipe getting called"
  context = {
    'thispage': 'Add Recipe', 
  }

  print "after context"

  graph = user_login(request, context)

  print "before if statement"
  if 'query' in request.GET:
    print "right before json"
    temp = json_parser.get_recipe(str(request.GET['query']))
    print "right after json"
    materials = ",".join(temp['ingredients'])
    
    current_recipe = Recipe(recipe_name = temp['title'], recipe_url = temp['link'], 
      ingredients = materials)
    print "after current recipe"
    current_recipe.save()
    print 'after one save'
    relational = User_Recipes(user_id = context['id'], recipe_name_id = current_recipe)
    relational.save()
    print "after saves"
  else:
    print "empty request"
    message = 'You submitted an empty form. Please go back to the search page'

  print "completes without throwing an exception"


