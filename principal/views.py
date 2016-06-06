from principal.models import Noticia, Comentario
from principal.forms import NoticiaForm, ComentarioForm, ContactoForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.mail import EmailMessage
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required


def sobre(request):
	html = "<html><body><center><p><p><p><h1>Sitio De Noticias En Tu Comunidad</h1><p><h2>Autor Del Proyecto:</h2><p>Lozano Zavala Ramon<p><p><p><p><h2>Programadores: </h2><p>Arriaga Jaramillo Juan Efren<p>Galindo Rico Benjamin<p>Guevara Salcedo Maria J.<p>Hernandez Escareno Hugo<p>Villicana Rodriguez Omar</body></html>"
	return HttpResponse(html)

def inicio(request):
    noticias = Noticia.objects.all()
    return render_to_response('inicio.html',{'noticias':noticias}, context_instance=RequestContext(request))

def usuarios(request):
    usuarios = User.objects.all()
    noticias = Noticia.objects.all()
    return render_to_response('usuarios.html',{'usuarios':usuarios,'noticias':noticias}, context_instance=RequestContext(request))

def lista_noticias(request):
    noticias = Noticia.objects.all()
    return render_to_response('noticias.html',{'datos':noticias}, context_instance=RequestContext(request))

def detalle_noticia(request, id_noticia):
    dato = get_object_or_404(Noticia, pk=id_noticia)
    comentarios = Comentario.objects.filter(noticia=dato)
    return render_to_response('noticia.html',{'noticia':dato,'comentarios':comentarios}, context_instance=RequestContext(request))

def contacto(request):
    if request.method=='POST':
        formulario = ContactoForm(request.POST)
        if formulario.is_valid():
            titulo = 'Mensaje desde el recetario de Maestros del Web'
            contenido = formulario.cleaned_data['mensaje'] + "\n"
            contenido += 'Comunicarse a: ' + formulario.cleaned_data['correo']
            correo = EmailMessage(titulo, contenido, to=['destinatario@email.com'])
            correo.send()
            return HttpResponseRedirect('/')
    else:
        formulario = ContactoForm()
    return render_to_response('contactoform.html',{'formulario':formulario}, context_instance=RequestContext(request))

def nueva_noticia(request):
    if request.method=='POST':
        formulario = NoticiaForm(request.POST, request.FILES)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/noticias')
    else:
        formulario = NoticiaForm()
    return render_to_response('noticiaform.html',{'formulario':formulario}, context_instance=RequestContext(request))


def nuevo_comentario(request):
    if request.method=='POST':
        formulario = ComentarioForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/noticias')
    else:
        formulario = ComentarioForm()
    return render_to_response('comentarioform.html',{'formulario':formulario}, context_instance=RequestContext(request))

