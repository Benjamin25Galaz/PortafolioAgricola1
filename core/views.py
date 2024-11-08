from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from transbank.webpay.webpay_plus.transaction import Transaction
from django.contrib.auth.forms import AuthenticationForm
from transbank.webpay.webpay_plus.transaction import Transaction
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout as django_logout, authenticate
from .forms import TemaForm, SolicitudForm, RegisterForm, DonacionForm, CommentForm, ProductoForm, PagoForm
from .models import Tema, Solicitud, Register, Donacion, Producto,Pago,Compra, CompraProducto
from .carrito import Carrito
from django.utils import timezone


# Create your views here.
def home(request):
    return render(request, 'core/home.html')

def donacion(request):
    return render(request, 'core/donacion.html')

def donacion(request):
    if request.method == 'POST':
        form = DonacionForm(request.POST)
        if form.is_valid():
            donacion_guardada = form.save()
            return redirect('resumen_donacion', donacion_id=donacion_guardada.id)
    else:
        form = DonacionForm()
    return render(request, 'core/donacion.html', {'form': form})

def resumen_donacion(request, donacion_id):
    donacion = Donacion.objects.get(id=donacion_id)
    return render(request, 'core/resumen_donacion.html', {'donacion': donacion})


def migrar_usuarios():
    # Obtener todos los registros de la tabla Register
    registros = Register.objects.all()

    for registro in registros:
        # Verifica si ya existe un usuario con ese correo electrónico
        if not User.objects.filter(username=registro.correo_electronico).exists():
            # Crea un usuario en la tabla User
            user = User.objects.create_user(
                username=registro.correo_electronico,  # Utiliza el correo como nombre de usuario
                email=registro.correo_electronico,
                password=registro.contrasena,  # Asegúrate de que la contraseña esté almacenada de forma segura
                first_name=registro.nombre,
                last_name=registro.apellido
            )
            user.save()

@login_required(login_url='acceder')
def tema_detail(request, tema_id):
    tema = get_object_or_404(Tema, id=tema_id)
    comments = tema.comments.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.tema = tema
            comment.author = request.user
            comment.save()
            return redirect('tema_detail', tema_id=tema.id)
    else:
        form = CommentForm()

    return render(request, 'core/tema_detail.html', {
        'tema': tema,
        'comments': comments,
        'form': form,
    })


def register(request):
    return render(request, 'core/register.html')



def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Obtener los datos del formulario
            nombre = form.cleaned_data['nombre']
            apellido = form.cleaned_data['apellido']
            correo = form.cleaned_data['correo_electronico']
            contrasena = form.cleaned_data['contrasena']

            # Verificar si el usuario ya existe
            if User.objects.filter(username=correo).exists():
                # Agregar un mensaje de error al formulario
                form.add_error('correo_electronico', 'Este usuario ya está registrado.')
            else:
                # Crear el usuario en la tabla User
                user = User.objects.create_user(
                    username=correo,  # Utiliza el correo como nombre de usuario
                    email=correo,
                    password=contrasena,
                    first_name=nombre,
                    last_name=apellido
                )
                user.save()

                # Autenticar y loguear al usuario después de registrarse
                backend = 'core.authentication_backends.EmailBackend'
                login(request, user, backend=backend)  # Especifica el backend al iniciar sesión

                return redirect('home')  # Redirige a la página principal después del registro
    else:
        form = RegisterForm()
    return render(request, 'core/register.html', {'form': form})


def bienvenido(request):
    return render(request, 'core/bienvenido.html')


def solicitudes(request):
    return render(request, 'core/solicitudes.html')

def superurser(request):
    return render(request, 'core/superuser.html')


def solicitudes(request):
    if request.method == 'POST':
        form = SolicitudForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda la solicitud en la base de datos
            return redirect('solicitudes')
    else:
        form = SolicitudForm()

    return render(request, 'core/solicitudes.html', {'form': form})


def lista_solicitudes(request):
    solicitudes = Solicitud.objects.all()  # Obtenemos todas las solicitudes
    return render(request, 'core/lista_solicitudes.html', {'solicitudes': solicitudes})

def lista_donaciones(request):
    donaciones = Donacion.objects.all()  # Obtén todas las donaciones

    context = {
        'donaciones': donaciones,
    }
    return render(request, 'core/lista_donaciones.html', context)

def logout(request):
    logout(request)
    return HttpResponseRedirect('core/logout.html')

def catalogo(request):
    return render(request, 'core/catalogo.html')


def pago(request):
    return render(request, 'core/pago.html')

def pago(request):
    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
            pago = Pago(usuario=request.user, cantidad=form.cleaned_data['cantidad'])
            pago.save()
            messages.success(request, 'El pago ha sido procesado con éxito.')
            return redirect('pago_exitoso')
    else:
        form = PagoForm()

    return render(request, 'core/pago.html', {'form': form})

def pago_exitoso(request):
    return render(request, 'core/pago_exitoso.html')

def pago_fallido(request):
    return render(request, 'core/pago_exitoso.html')


def foro(request):
    return render(request, 'core/foro.html')

def foro(request):
    temas = Tema.objects.all()  # Obtiene todos los temas
    return render(request, 'core/foro.html', {'temas': temas})

# Vista del tema del foro
def crear_tema(request):
    return render(request, 'core/crear_tema.html')


@login_required(login_url='acceder')
def crear_tema(request):
    if request.method == 'POST':
        form = TemaForm(request.POST)
        if form.is_valid():
            tema = form.save(commit=False)  # No guarda todavía
            tema.author = request.user  # Asigna el autor
            tema.save()  # Guarda el tema en la base de datos
            return redirect('foro')  # Redirige a donde quieras
    else:
        form = TemaForm()
    return render(request, 'core/crear_tema.html', {'form': form})

def acceder(request):
    if request.method == "POST":
        correo_electronico = request.POST.get('correo_electronico')
        contrasena = request.POST.get('contrasena')

        # Autenticar al usuario usando el correo como nombre de usuario
        usuario = authenticate(request, username=correo_electronico, password=contrasena)

        # Verificar si la autenticación fue exitosa
        if usuario is not None:
            login(request, usuario)
            # Almacena el nombre en la sesión
            request.session['nombre_usuario'] = usuario.first_name  # Cambia según el campo que desees mostrar
            return redirect('bienvenido')
        else:
            error_message = "Credenciales inválidas."
            return render(request, 'core/acceder.html', {'error': error_message})

    return render(request, 'core/acceder.html')


def listar_productos(request):
    productos = Producto.objects.all()
    carrito = Carrito(request)
    total = carrito.obtener_total()
    return render(request, "core/listar_productos.html", {
        'productos': productos,
        'carrito': carrito,
        'total': total
    })

def agregar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = get_object_or_404(Producto, id=producto_id)

    if producto.stock > 0:
        carrito.agregar_carrito(producto)
        producto.stock -= 1
        producto.save()
        producto.verificar_y_reponer_stock()  # Llama al método para verificar el stock
        messages.success(request, f'{producto.nombre} ha sido añadido al carrito.')
    else:
        messages.error(request, 'Este producto está agotado.')

    return redirect('morstrar_carrito')


def eliminar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = get_object_or_404(Producto, id=producto_id)

    # Obtener la cantidad de este producto en el carrito antes de eliminarlo
    cantidad_en_carrito = carrito.obtener_cantidad(producto)

    # Eliminar el producto del carrito
    carrito.eliminar(producto)

    # Devolver el stock a la tienda
    producto.stock += cantidad_en_carrito
    producto.save()

    messages.success(request, f'{producto.nombre} ha sido eliminado del carrito y el stock ha sido actualizado.')
    return redirect("morstrar_carrito")  # Cambiar por el nombre que corresponda

def restar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = get_object_or_404(Producto, id=producto_id)
    carrito.restar(producto)
    return redirect('morstrar_carrito')  # Cambiar por el nombre que corresponda

def mostrar_carrito(request):
    carrito = Carrito(request)
    total = carrito.obtener_total()
    return render(request, "core/carrito.html", {
        'carrito': carrito,
        'total': total
    })


def sumar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = get_object_or_404(Producto, id=producto_id)

    # Verificar y reponer stock si es necesario
    producto.verificar_y_reponer_stock()

    # Obtener la cantidad actual del producto en el carrito después de actualizar stock
    cantidad_en_carrito = carrito.obtener_cantidad(producto)

    # Verificar si la cantidad en el carrito es menor al stock
    if cantidad_en_carrito < producto.stock:
        carrito.sumar(producto)
        producto.stock -= 1
        producto.save()
        messages.success(request, f'Se ha añadido una unidad más de {producto.nombre}.')
    else:
        messages.error(request, f'No se puede añadir más de {producto.stock} unidades de {producto.nombre}.')

    return redirect("morstrar_carrito")

def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect("morstrar_carrito")  # Cambiar por el nombre que corresponda

def formulario_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')
    else:
        form = ProductoForm()
    return render(request, 'core/formulario_producto.html', {'form': form})

def listar_productos(request):
    productos = Producto.objects.all()
    return render(request, 'core/listar_productos.html', {'productos': productos})

def detalle_producto(request, pk):
    producto = Producto.objects.get(pk=pk)
    return render(request, 'core/detalle_producto.html', {'producto': producto})

@login_required(login_url='acceder')
def iniciar_pago(request):
    transaction = Transaction()
    response = transaction.create(
        buy_order='orden123',
        session_id='sesion123',
        amount=10000,
        return_url='https://ecoagricola.pythonanywhere.com/webpay/retorno'
    )
    return redirect(response['url'] + '?token_ws=' + response['token'])

def retorno_pago(request):
    token = request.GET.get('token_ws')
    transaction = Transaction()
    response = transaction.commit(token)
    if response['status'] == 'AUTHORIZED':
        # Pago exitoso
        return render(request, 'core/pago_exitoso.html', {'response': response})
    else:
        # Error en el pago
        return render(request, 'core/pago_fallido.html', {'response': response})

@login_required(login_url='acceder')
def finalizar_compra(request):
    if request.user.is_authenticated:
        carrito = Carrito(request)

        # Verificar si el carrito no está vacío
        if not carrito.carrito:
            return redirect('carrito')  # O una página que desees si el carrito está vacío

        # Crear la compra y asociarla al usuario actual
        compra = Compra.objects.create(usuario=request.user)

        # Recorrer los productos del carrito y registrar cada uno
        for producto_id, item in carrito.carrito.items():
            producto = Producto.objects.get(id=producto_id)
            cantidad = item['cantidad']
            CompraProducto.objects.create(compra=compra, producto=producto, cantidad=cantidad)

        # Limpiar el carrito después de completar la compra
        carrito.limpiar()  # Vacía el carrito
        return redirect('home')
 # Redirige al historial de compras # Redirige al historial de compras después de la compra


@login_required(login_url='acceder')
def historial_compras(request):
    compras = Compra.objects.all()

    # Crear una lista para almacenar cada compra con su total
    compras_totales = []
    for compra in compras:
        total_compra = sum(item.producto.precio * item.cantidad for item in compra.compraproducto_set.all())
        compras_totales.append({
            'compra': compra,
            'total': total_compra,
        })

    return render(request, 'core/historial_compras.html', {'compras_totales': compras_totales})



def buscar_productos(request):
    query = request.GET.get('search')
    productos = Producto.objects.filter(nombre__icontains=query) if query else None
    return render(request, 'core/buscar_productos.html', {'productos': productos, 'query': query})
