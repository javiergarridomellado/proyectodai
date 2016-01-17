from django import forms
from django.contrib.auth.models import User
#from restaurante.models import Bar, Tapa, UserProfile
from restaurante.models import Bar, Tapa



class UserForm(forms.ModelForm):
	username = forms.SlugField (max_length=8, label='Usuario:')
	email    = forms.EmailField (label='Email:')
	password = forms.SlugField (max_length=8, 
	                   help_text="(numeros y letras hasta 8)", 
	                   widget=forms.PasswordInput(),  
	                   label='Contrasena:')
	class Meta:
		model  = User
		fields = ('username', 'email', 'password')


class login_form(forms.ModelForm):
	username = forms.SlugField (max_length=8, 
	                             label='Usuario: ')
	password = forms.SlugField (max_length=8, 
	                        widget=forms.PasswordInput(),  
	                        label='Contrasena:',
	                        help_text='Hasta 8 letras')
	class Meta:
		model  = User
		fields = ('username',  'password')


class BarForm(forms.ModelForm):
    nombre = forms.CharField(max_length=128, help_text="Introduzca el nombre del Bar")
    direccion = forms.CharField(max_length=128, help_text="Introduzca la direccion(ej.Spain,Granada,Calle Recogidas).")
    numerovisitas = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Bar
        fields = ('nombre','direccion')

#si se anadiese un campo url a bar para que adapte la url
    #def clean(self):
        #cleaned_data = self.cleaned_data
        #url = cleaned_data.get('url')

        # If url is not empty and doesn't start with 'http://', prepend 'http://'.
        #if url and not url.startswith('http://'):
            #url = 'http://' + url
            #cleaned_data['url'] = url

        #return cleaned_data




class TapaForm(forms.ModelForm):
    nombre = forms.CharField(max_length=128, help_text="Porfavor, introduzca el nombre de la Tapa.")
    #url = forms.URLField(max_length=200, help_text="Please enter the URL of the page.")
    votos = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Tapa

        # What fields do we want to include in our form?
        # This way we don't need every field in the model present.
        # Some fields may allow NULL values, so we may not want to include them...
        # Here, we are hiding the foreign key.
        # we can either exclude the category field from the form,
        exclude = ('bar',)
        #or specify the fields to include (i.e. not include the category field)
        #fields = ('title', 'url', 'views')




#class UserForm(forms.ModelForm):
    #password = forms.CharField(widget=forms.PasswordInput())

    #class Meta:
        #model = User
        #fields = ('username', 'email', 'password')

#class UserProfileForm(forms.ModelForm):
    #class Meta:
        #model = UserProfile
        #fields = ('website')
		#fields = ('website', 'picture')

#class register_form(forms.ModelForm):
	#username = forms.SlugField (max_length=8, label='Usuario:')
	#email    = forms.EmailField (label='Email:')
	#password = forms.SlugField (max_length=8, 
	                   #help_text="(numeros y letras hasta 8)", 
	                   #widget=forms.PasswordInput(),  
	                   #label='Contrasena:')
	#class Meta:
		#model  = User
		#fields = ('username', 'email', 'password')
