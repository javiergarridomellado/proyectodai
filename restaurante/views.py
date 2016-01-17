from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from restaurante.models import Bar, Tapa
#from restaurante.forms import UserForm, UserProfileForm
from restaurante.forms import UserForm,login_form, BarForm, TapaForm
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse


def index(request):
	bar_list = Bar.objects.order_by('nombre')[:5] #orden ascendente a-z, orden descendente z-a con ('-nombre')
	top_bares = Bar.objects.order_by('-numerovisitas')[:3]
	top_tapas = Tapa.objects.order_by('-votos')[:3]
	context_dict = {'bares': bar_list, 'TopBar': top_bares, 'TopTapa': top_tapas}
	#context_dict = {'bares': bar_list}
	# Render the response and send it back!
	return render(request, 'restaurante/index.html', context_dict)
	#context_dict = {'boldmessage': "I am bold font from the context"}

    #return HttpResponse("Rango says: Hello world! <br/> <a href='/restaurante/about'>About</a>")
	#return render(request, 'restaurante/index.html', context_dict)

def about(request):
	mensaje = {'contacto': "Informatica-Esp.Tecnologias de la Informacion"}
	
    #return HttpResponse("About  <a href='/restaurante/'>Index</a>")
	return render(request, 'restaurante/about.html', mensaje)

def menu(request):
	context_dict = {'variable_name': "Pescado"}
	return render(request, 'restaurante/menu.html', context_dict)

def login(request):
	
	return render(request, 'restaurante/login.html')

def add_tapa(request):
	
	return render(request, 'restaurante/add_tapa.html')

def add_bar(request):
	
	return render(request, 'restaurante/add_bar.html')

def bar(request, bar_name_slug):

    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}

    try:
        # Can we find a tapa name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        bar = Bar.objects.get(slug=bar_name_slug)
        context_dict['bar_name'] = bar.nombre
        context_dict['bar_dire']=bar.direccion
        bar.numerovisitas = bar.numerovisitas+1
        context_dict['bar_nume']=bar.numerovisitas
        bar.save()
        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        tapas = Tapa.objects.filter(bar=bar)

        # Adds our results list to the template context under name pages.
        context_dict['tapas'] = tapas
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['bar'] = bar
    except Bar.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass

    # Go render the response and return it to the client.
    #context_dict = {'bares': bar_list, 'TopBar': top_bares, 'TopTapa': top_tapas}
    return render(request, 'restaurante/bar.html', context_dict)



####
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
#from restaurante.forms import register_form

def register(request):	
	form = UserForm()
	context = { 'mensaje': 'Estamos en  Registro', 'form': form,}

	if request.method == 'POST':
		form = UserForm(request.POST)
		if form.is_valid():		
			# Save the user's form data to the database.
			user = form.save()
                       # Now we hash the password with the set_password method.
                       # Once hashed, we can update the user object.
			user.set_password(user.password)
			user.save()						
			context['mensaje'] =  u'Registrado como  %s' % (user.username)		
		else:
			context['form'] = form
	   	
	return render (request, 'restaurante/registro.html', context)


def login_view(request):	# no se llama 'login'
	form = login_form()
	context = { 'form': form, 'mensaje':'Logueandose',}

	if request.method == 'POST':		
		form = login_form(request.POST)		
		usuario = request.POST.get('username')
		contrase = request.POST.get('password')
		# Hacer el login
		user = authenticate(username=usuario, password=contrase)
		if user is not None and user.is_active:
			login(request, user)
			context['mensaje'] =  u'Logueado como  %s, contrasena ****' % (usuario)
		else:
			context['mensaje'] =  u'No usuario  o contrasena incorrecta'
	   	
	return render (request, 'restaurante/login.html', context)

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")


#para anadir tapa poner un decorador de login_required


# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/restaurante/')


@login_required
def add_bar(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = BarForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = BarForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'restaurante/add_bar.html', {'form': form})

@login_required
def add_tapa(request, bar_name_slug):

    try:
        bar = Bar.objects.get(slug=bar_name_slug)
    except Bar.DoesNotExist:
                bar = None

    if request.method == 'POST':
        form = TapaForm(request.POST)
        if form.is_valid():
            if bar:
                tapa = form.save(commit=False)
                tapa.bar = bar
                tapa.votos = 0
                tapa.save()
                # probably better to use a redirect here.
                return HttpResponseRedirect('/restaurante/') #preguntar para anadir bar_name_slug a la ruta
				#return bar(request, bar_name_slug)
        else:
            print form.errors
    else:
        form = TapaForm()

    context_dict = {'form':form, 'bar': bar}

    return render(request, 'restaurante/add_tapa.html', context_dict)


def reclama_datos (request):
	
	top_bares = Bar.objects.order_by('-numerovisitas')[:3]
	
	#datos = {"Bares":  [    {"Nombre":top_bares[0].nombre,"Visitas":top_bares[0].numerovisitas},    {"Nombre":top_bares[1].nombre,"Visitas":top_bares[1].numerovisitas},    {"Nombre":top_bares[2].nombre,"Visitas":top_bares[2].numerovisitas}   ]  }
	datos={'lista_bares':[top_bares[0].nombre,top_bares[1].nombre,top_bares[2].nombre], 'V':[top_bares[0].numerovisitas,top_bares[1].numerovisitas,top_bares[2].numerovisitas]} 
	return JsonResponse(datos, safe=False)




#datos={'lista_bARES':['BAR',], 'V':[]}


#def register2(request):

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    #registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    #if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        #user_form = UserForm(data=request.POST)
        #profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        #if user_form.is_valid() and profile_form.is_valid():
        #if user_form.is_valid():
            # Save the user's form data to the database.
            #user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            #user.set_password(user.password)
            #user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            #profile = profile_form.save(commit=False)
            #profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            #if 'picture' in request.FILES:
                #profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            #profile.save()

            # Update our variable to tell the template registration was successful.
            #registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        #else:
            #print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    #else:
        #user_form = UserForm()
        #profile_form = UserProfileForm()

    # Render the template depending on the context.
    #return render(request,
            #'restaurante/register.html',
            #{'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )
    #return render(request,
            #'restaurante/register.html',
            #{'user_form': user_form, 'registered': registered} )
