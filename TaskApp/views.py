from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from .models import BlogCategory, BlogPost, BookAppointment, CustomUser
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from datetime import datetime, timedelta

# Create your views here.


def login_page(request):
    if request.method == 'POST':
        user_name = request.POST['txtUsername']
        user_password = request.POST['txtPassword']
        u1 = authenticate(username=user_name, password=user_password)
        if u1 is not None:
            if u1.is_superuser:
                login(request, u1)
                doctor_details = {
                    'first_name': u1.first_name,
                    'last_name': u1.last_name,
                    'username': u1.username,
                    'email': u1.email,
                    'address': u1.user_address,
                    'lane': u1.user_lane,
                    'city': u1.user_city,
                    'state': u1.user_state,
                    'pincode': u1.user_pincode,
                    'profile_picture': u1.profile_picture,
                }
                return render(request, 'doctor_home.html', {'DoctorDetails': doctor_details})
            else:
                login(request, u1)
                user_details = {
                    'first_name': u1.first_name,
                    'last_name': u1.last_name,
                    'username': u1.username,
                    'email': u1.email,
                    'address': u1.user_address,
                    'lane': u1.user_lane,
                    'city': u1.user_city,
                    'state': u1.user_state,
                    'pincode': u1.user_pincode,
                    'profile_picture': u1.profile_picture,
                }
                return render(request, 'patient_home.html', {'UserDetails': user_details})
        else:
            return render(request, 'login.html', {'Msg': 'Username and Password Not Matching'}) 
    else:       
        return render(request, 'login.html')
    
def patient_signup_page(request):
    if request.method == 'POST':
        first_name = request.POST['txtFirstName']
        last_name = request.POST['txtLastName']
        profile_picture = request.FILES.get('txtProfilePicture')
        user_name = request.POST['txtUsername']
        email_id = request.POST['txtEmailId']
        password = request.POST['txtPassword']
        confirm_password = request.POST['txtConfirmPassword']
        address = request.POST['txtAddress']
        lane = request.POST['txtLine1']
        city = request.POST['txtCity']
        state = request.POST['txtState']
        pincode = int(request.POST['txtPinCode'])
        if password == confirm_password:
            if CustomUser.objects.filter(username = user_name).exists():
                return render(request, 'patient_signup.html', {'Msg': 'Username already in use please use different'})
            elif CustomUser.objects.filter(email=email_id).exists():
                return render(request, 'patient_signup.html', {'Msg': 'Email already exist use different'})
            else:
                u1 = CustomUser.objects.create_user(
                    first_name = first_name, 
                    last_name = last_name, 
                    username = user_name, 
                    email = email_id, 
                    password = password,
                    user_address = address,
                    user_lane = lane,
                    user_city = city,
                    user_state = state,
                    user_pincode = pincode,
                    profile_picture = profile_picture
                    )
                u1.save()
                return render(request, 'patient_signup.html', {'Success1': 'Account Created Successfully'})
        else:
            return render(request, 'patient_signup.html', {'Msg1': 'Password & Confirm Password not matching'})
    else:            
        return render(request, 'patient_signup.html')    

def doctor_signup_page(request):
    if request.method == 'POST':
        first_name = request.POST['txtFirstName1']
        last_name = request.POST['txtLastName1']
        profile_picture = request.FILES.get('txtProfilePicture1')
        user_name = request.POST['txtUsername1']
        email_id = request.POST['txtEmailId1']
        password = request.POST['txtPassword1']
        confirm_password = request.POST['txtConfirmPassword1']
        address = request.POST['txtAddress1']
        lane = request.POST['txtLine1']
        city = request.POST['txtCity1']
        state = request.POST['txtState1']
        pincode = int(request.POST['txtPinCode1'])
        if password == confirm_password:
            if CustomUser.objects.filter(username=user_name).exists():
                return render(request, 'doctor_signup.html', {'Msg': 'Username already in use please use different'})
            elif CustomUser.objects.filter(email=email_id).exists():
                return render(request, 'doctor_signup.html', {'Msg': 'Email already exist use different'})
            else:
                u1 = CustomUser.objects.create_superuser(
                    first_name=first_name, 
                    last_name=last_name, 
                    username=user_name, 
                    email=email_id, 
                    password=password,
                    user_address = address,
                    user_lane = lane,
                    user_city = city,
                    user_state = state,
                    user_pincode = pincode,
                    profile_picture = profile_picture
                    )
                u1.save()
                return render(request, 'doctor_signup.html', {'Success1': 'Account Created Successfully'})
        else:
            return render(request, 'doctor_signup.html', {'Msg1': 'Password & Confirm Password not matching'})
    else:            
        return render(request, 'doctor_signup.html')


def doctor_home_page(request):
    return render(request, 'doctor_home.html')

def patient_home_page(request):
    return render(request, 'patient_home.html')

def blog_post_page(request):
    if request.method == 'POST':
        b1 = BlogPost()
        b1.title = request.POST['txtTitle']
        b1.image = request.FILES.get('txtImage')
        b1.category = BlogCategory.objects.get(category_name=request.POST['txtCategory'])
        b1.summary = request.POST['txtSummary']
        b1.content = request.POST['txtContent']
        b1.draft = request.POST.get('chkDraft') == 'on' # if check box is selected
        
        b1.save()
        return render(request, 'upload_blog.html', {'Msg': 'Data Added Successfully'})
    else:
        categories = BlogCategory.objects.all()
        return render(request, 'upload_blog.html', {'categories': categories})

def display_blog_page(request):
    post_data = BlogPost.objects.all()
    return render(request, 'view_blog.html', {'PostData': post_data})

def blog_list_page(request):
    category = BlogCategory.objects.all()    
    posts = BlogPost.objects.filter(draft=False)
    return render(request, 'blog_list.html', {'Posts': posts, 'Category': category})

def doctors_list(request):
    doctors = CustomUser.objects.filter(is_superuser=True)
    return render(request, 'doctor_list.html', {'Doctors': doctors})


def book_appointment(request, id):
    a1 = CustomUser.objects.get(id=id)
    if request.method == 'POST':
        a1.first_name = request.POST['txtFirstName']
        a1.last_name = request.POST['txtLastName']
        a1.save()
        a2 = BookAppointment()
        a2.speciality = request.POST['txtSpeciality']
        a2.appointment_date = request.POST['txtAppointmentDate']
        a2.appointment_time = request.POST['txtStartTime']
         # Calculate end time (start time + 45 minutes)
        start_time = datetime.strptime(a2.appointment_time, '%H:%M')
        end_time = start_time + timedelta(minutes=45)
        a2.end_time = end_time.strftime('%H:%M')
        a2.save()
        appointments = BookAppointment.objects.all()
        return render(request, 'appointment_details.html', {'appointment': a2, 'first_name': a1.first_name, 'last_name': a1.last_name})
    return render(request, 'book_appointment.html', {'CustomUser': a1})

def display_appointments(request):
    appointments = BookAppointment.objects.all()
    return render(request, 'display_aappointments.html', {'appointment': appointments})

def logout_fun(request):
    logout(request)
    return redirect('login')