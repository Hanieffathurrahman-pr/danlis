from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth import login as auth_login, get_user_model
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
import re
import pandas as pd
from django.http import Http404
import json


def base(request):
    """
    Render the dashboard page.
    """
    context = {
        'title': 'Dashboard',
    }
    return render(request, 'base.html', context)
def index(request):
    """
    Render the index page.
    """
    context = {
        'title': 'Home',
    }
    return render(request, 'index.html', context)   

def about(request):
    """
    Render the about page.
    """
    context = {
        'title': 'About',
    }
    return render(request, 'about.html', context)
def contact(request):
    """
    Render the contact page.
    """ 
    context = {
        'title': 'Contact',
    }
    return render(request, 'contact.html', context)

#login --------------------> fix
userModel = get_user_model()
def Login(request):
    """
    Render the login page.
    """
    context = {
        'title': 'Login',
    }
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        identifier = request.POST.get('identifier')
        password = request.POST.get('password')

        try:
            if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', identifier):
                user = userModel.objects.get(email=identifier)
            else:
                user = userModel.objects.get(username=identifier)
            if user.check_password(password):
                auth_login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Password salah.")
                return redirect('login')
        except user.DoesNotExist:
            messages.error(request, "User tidak ditemukan.")
            return redirect('login')
    return render(request, 'login.html', context)

# Register --------------------> fix
def register(request):
    """
    Render the register page.
    """
    context = {
        'title': 'Register',
    }
   
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Pendaftaran berhasil. Silakan login.")  
            return redirect('login')
        else:
            messages.error(request, "Ada kesalahan dalam pendaftaran. Silakan periksa kembali.")
            return redirect('register')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form, 'title': 'Register'})

        


# Dashboard view
@login_required(login_url='login')
def dashboard(request):
    """
    Render the dashboard page for logged-in users.
    """
    context = {
        'title': 'Dashboard',
        'user': request.user,
    }
    return render(request, 'backend/dashboard.html', context)

@login_required(login_url='login')
def analisis(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        try:
            df = pd.read_excel(file) if file.name.endswith('.xlsx') else pd.read_csv(file)
            
        except Exception as e:
            return render(request, 'backend/analisis.html', {
                'error': f"Error membaca file: {str(e)}"
            })
        for col in df.columns:
            if col.lower() in ['tanggal', 'waktu', 'date']:
                try:
                    df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime('%Y-%m-%d')
                except Exception:
                    pass
        from django.contrib.auth import get_user_model
        User = get_user_model()

        user = User.objects.get(pk=request.user.id)
        Dataset.objects.create(
            namaFile=file.name,
            data=json.loads(df.astype(str).to_json(orient='records')),
            user=user # Ini penting untuk RLS
        )

        data = json.loads(df.to_json(orient='records'))  # Data berisi baris-baris
        columns = df.columns.tolist()                    # Nama-nama kolom
        # Ambil nama kolom dari DataFrame

        
        return render(request,'backend/analisis.html',{
            'sukses': 'File berhasil diupload.',
            'data':data,
            'columns': columns,   
        })
    
  
    return render(request, 'backend/analisis.html')

#lihat dataset yang udah diupload
@login_required(login_url='login')
def daftar_upload(request):
    """
    Render the page to list uploaded datasets.
    """
    datasets = Dataset.objects.all().order_by('-tanggalUpload')
    return render(request, 'backend/analisis.html', {'datasets': datasets, 'title': 'Daftar Upload'})
        
#detail dataset yang udah diupload
@login_required(login_url='login')  
def detail_upload(request, dataset_id):
    """
    Render the detail page for a specific uploaded dataset.
    """
    dataset = get_object_or_404(Dataset, id=dataset_id)
    df = pd.DataFrame(dataset.data_json)
    data = df.to_dict(orient='records')
    columns = df.columns
    return render(request, 'backend/detil.html', {
        'upload': dataset,
        'data': data,
        'columns': columns
    })
#hapus dataset yang udah diupload
@login_required(login_url='login')
def hapus_upload(request, dataset_id):
    """
    Handle the deletion of an uploaded dataset.
    """
    dataset = get_object_or_404(Dataset, id=dataset_id)
    if request.method == 'POST':
        dataset.delete()
        messages.success(request, "Dataset berhasil dihapus.")
        return redirect('daftarUpload')
    return render(request, 'backend/lihatData.html', {'dataset': dataset})

#profile
@login_required(login_url='login')
def profile(request):
    """
    Render the user profile page.
    """
    context = {
        'title': 'Profile',
        'user': request.user,
    }
    return render(request, 'backend/profile.html', context)

#upload file

    
    

def logout(request):
    """
    Handle user logout.
    """
    from django.contrib.auth import logout as auth_logout
    auth_logout(request)
    return render(request,'backend/logout.html', {'title': 'Logout'})