from django.shortcuts import render,redirect
from django.http import HttpResponseNotFound, HttpResponse
from my_app.models import Categories, Course, Author, Level, Video, User_Course, Contactus, Comment
# Create your views here.4
from django.contrib.auth.models import User

from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Sum
from my_app.models import CustomModelName
from django.contrib import messages
import razorpay
from my_app.forms import CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required



Private_API_Key = 'Your_API_KEY'
Private_Auth_Token = 'Your_Private_Auth_Token'


def discount(price, discount):
    discount_price = (price * discount)/100
    final_price = price - discount_price
    return final_price

def Base(request):
    return render(request, 'base.html')



def home(request):
    categories = Categories.objects.all()

    courses = Course.objects.filter(status="PUBLISH").order_by('id')
    print(courses[0])
    time_duration = []
    for k in courses :
         i = Video.objects.filter(course=k)
         sum = 0
         for j in i:
              sum += int(j.time_duration)
         time_duration.append(sum)
    print(time_duration)
    time_duration_in_hr = ['Not']
    time_duration_in_min = ['Not']
    for x in time_duration:
          z1 = x // 60
          z2 = x % 60

          time_duration_in_hr.append(z1)
          time_duration_in_min.append(z2)

    print(time_duration_in_min, time_duration_in_hr)
    context = {
        'category' : categories,
        'course' : courses,
        'time_duration_in_hr' :time_duration_in_hr,
        'time_duration_in_min':time_duration_in_min
    }
    return render(request, 'main/home.html', context)


@login_required(login_url="/login")
def available_courses(request):
    categories = Categories.get_all_category(Categories)
    courses = Course.objects.filter(status="PUBLISH").order_by('-id')
    author = Author.objects.all()
    levels = Level.objects.all()
    free_course_count = Course.objects.filter(price=0).count()
    paid_course_count = Course.objects.filter(price__gte=1).count()
    page_number = request.GET.get('page')
    p = Paginator(courses, 2)
    time_duration = []
    for k in courses :
         i = Video.objects.filter(course=k)
         sum = 0
         for j in i:
              sum += int(j.time_duration)
         time_duration.append(sum)
    print(time_duration)
    time_duration_in_hr = ['Not']
    time_duration_in_min = ['Not']
    for x in time_duration:
          z1 = x // 60
          z2 = x % 60

          time_duration_in_hr.append(z1)
          time_duration_in_min.append(z2)

    print(time_duration_in_min, time_duration_in_hr)

    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    context = {
        'category' : categories,
        'course' : courses,
        'author' : author,
        'levels' : levels,
        'free_course_count' : free_course_count,
        'paid_course_count' : paid_course_count,
        'page_obj' : page_obj,
        'time_duration_in_min' :time_duration_in_min,
        'time_duration_in_hr' :time_duration_in_hr

    }
    return render(request, 'main/courses.html', context)



def ContactUs(request):
    if request.method == "POST":
         name = request.POST['name']
         email = request.POST['email']
         message = request.POST['message']
         try :
                a = Contactus(name = name, Email = email, Message=message)
                a.save()
                messages.success(request, 'We will Contact You Shortly Please check you email regularly')
                return redirect('Home')
         except Exception as e:
              messages.error(request, 'Sorry to say that we are facing techanical glitch please try again after sometime')
              return redirect('Home')
    return render(request, 'main/contact_us.html')



def AboutUs(request):
    return render(request, 'main/about_us.html')

@login_required(login_url="/login")
def filter_data(request):
    categories = request.GET.getlist('category[]')
    level = request.GET.getlist('level[]')
    price = request.GET.getlist('price[]')
    print('categories',categories)
    print('level',level)
    print('price', price)

    

    if categories:
        course = Course.objects.filter(category__id__in=categories).order_by('-id')

    elif level:
        course = Course.objects.filter(level__id__in=level).order_by('-id')
        
    elif price == ['pricefree']:
        course = Course.objects.filter(price=0)

    elif price == ['pricepaid']:
        course = Course.objects.filter(price__gte=1)

    elif price == ['priceall']:
        course = Course.objects.all()
    
    else: 
        course = Course.objects.all().order_by('-id')
    
    t = render_to_string('ajax/course.html', {'course': course})

    return JsonResponse({'data': t})


def search_course(request):
    query = request.GET['query']
    categories = Categories.objects.all()
    course = Course.objects.filter(title__icontains=query)
    print(course)
    context = {
              'course' : course, 
               'query': query
               }
    return render(request, 'search/search.html' , context)



@login_required(login_url="/login")
def course_detail(request, slug):

    course = Course.objects.filter(slug=slug)
    if request.method == 'POST' :
                 form = CommentForm(request.POST)
                 print(form)
                 if form.is_valid():
                      form.instance.user = request.user
                      form.instance.course = course.first()
                      form.save()
                      return redirect('my_course', course.first().slug)
    course = Course.objects.filter(slug=slug)
    query = course.first().title
    query_list = query.split(' ')
    course_all = Course.objects.all()
    course_match = []
    
    for k in course_all:
         query3 = k.title
         query4 = query3.split(' ')
         x = 10
         for j in query4:
              for i in query_list:
                   if j == i:
                        course_match.append(k.id)
                        x = 0
                        break
              if x == 0:
                   break
                   
                        

    print(course_match)
    course_matched = Course.objects.filter(id__in = course_match)
    print(course_matched)
    # user_course = User_Course.objects.all()
    time_duration = Video.objects.filter(course__slug=slug).aggregate(sum=Sum('time_duration'))
    enroll = False
    try :
         check_enroll = User_Course.objects.filter(user=request.user)
         course1 = Course.objects.get(slug=slug)
         for k in check_enroll:
                if k.Course.id == course1.id:
                    enroll = True
                else:
                    enroll= False
              
    except User_Course.DoesNotExist:
         check_enroll = None
         enroll =False
    if course.exists():
        course = course.first()
        print(enroll)
        comment = Comment.objects.filter(course=course)
                 

        return render(request, 'course/course_detail.html', {'course':course, 'time_duration':time_duration, 
                                                             'forms' :CommentForm, 'enroll' :enroll, 'comment':comment, 
                                                             'course_matched' : course_matched
                                                             })
    else:
        return HttpResponseNotFound('Course Does Not exists')
    


@login_required(login_url="/login")
def checkout(request, slug):
    course = Course.objects.get(slug=slug)
    courses = User_Course.objects.filter(Course=course)
    if courses.exists():
         messages.success(request, 'you have already enrollled in the course')
         return redirect('my_course')
         
    if course.price == 0:
        
        usercourse = User_Course(
            user = request.user,
            Course = course)
        usercourse.save()
        messages.success(request, 'course is successfully Enrolled')
        return redirect('my_course')
    return render(request, 'checkout/checkout.html')


def my_course(request):
    
    print(request.user)
    courses = User_Course.objects.filter(user=request.user)
    return render(request, 'course/my_course.html', {'courses' : courses})

def order(request, course_id):    
        client = razorpay.Client(auth=(Private_API_Key,Private_Auth_Token))
        course_obj =  Course.objects.get(id=course_id)
        user_course = User_Course.objects.filter(user=request.user)
        

        # order_obj= User_Course.objects.create(
        #     user = request.user,
        #     course = course_obj,
        #     paid = False
        # )
        order_obj = User_Course.objects.get(user=request.user, Course=course_obj)
        order_amount = discount(course_obj.price, course_obj.discount)
        course_obj.price = order_amount
        order_currency = 'INR'
        order_receipt = 'order_rcptid_11'
        payment = client.order.create(dict(amount=order_amount*100, currency=order_currency, receipt=order_receipt))
        order_obj.razor_pay_order_id = payment['id']
        order_obj.save()
        print("********", payment)

        return render(request, 'BuyNow/buynow.html', {'course' : course_obj, 'payment':payment,  'user_course' : user_course})
@login_required(login_url="/login")
def sucess(request):
      try :
            order_id = request.GET.get('order_id')
            payment_id = request.GET.get('payment_id')
            signature = request.GET.get('signature')
            print(order_id)
            order = User_Course.objects.get(razor_pay_order_id=order_id)
            order.razor_pay_payment_id  = payment_id
            order.razor_pay_payment_signature =signature
            order.paid =True
            order.save()
            order_amount = discount(order.Course.price, order.Course.discount)

            return render(request, 'BuyNow/sucess.html', {'order':order, 'order_amount':order_amount})
      except Exception as e:
            return render(request, 'BuyNow/fail.html', {'error':e})

@login_required(login_url="/login")
def contactform(request, course_id):
    course_obj =  Course.objects.get(id=course_id)
    user_course = User_Course.objects.filter(user=request.user)
    if request.method == "POST":
            print('Yellow')
            course_obj =  Course.objects.get(id=course_id)
            print(course_obj.id)
            profession = request.POST['billing_company']
            country = request.POST['billing_state']
            postcode = request.POST['billing_postcode']
            billing_phone = request.POST['billing_phone']
            order_obj= User_Course.objects.create(
            user = request.user,
            Course = course_obj,
            paid = False,
            profession=profession,
            country=country, 
            postcode=postcode, 
            Phone=billing_phone
            )
            print("""""""""""""""""""""""""""""",order_obj)
            order_obj.save()
            return redirect('order', course_id=course_obj.id)
    
    print(len(user_course))
    if len(user_course) >= 1 :
        for k in user_course:
                    print(k.user, request.user)
                    print(k.Course,  course_obj)
                    if k.Course == course_obj :
                        print('yaha par koun hai')
                        messages.success(request, 'you have already enrollled in the course')
                        return redirect('my_course')
        for k in user_course:         
                if k.user == request.user:
                        messages.success(request, 'you have already fill the contact form in the course')
                        order_obj= User_Course.objects.create(
                        user = request.user,
                        Course = course_obj,
                        paid = False,
                        profession=k.profession,
                        country=k.country, 
                        postcode=k.postcode, 
                        Phone=k.Phone
                        )
                        order_obj.save()
                        return redirect('order', course_id=course_obj.id)

                    
    entries = User.objects.get(email=request.user.email)
    course_obj =  Course.objects.get(id=course_id)
    context = {
        'user' : entries,
        'course' : course_obj
    }
    return render(request, 'BuyNow/contactform.html', context)

@login_required(login_url="/login")
def Watch_Course(request, slug):
            course = Course.objects.filter(slug=slug)
            if request.method == 'POST' :
                 form = CommentForm(request.POST)
                 print(form)
                 if form.is_valid():
                      form.instance.user = request.user
                      form.instance.course = course.first()
                      form.save()
                      return redirect('watch_course', course.first().slug)

                 
            course = Course.objects.filter(slug=slug)
            lecture = request.GET.get('lecture')
            print('lecture', lecture)
            
            video = Video.objects.filter(serial_number=lecture, course=course.first()).first()
            print(video)
            if video is not None :
                    current = video.serial_number
            else:
                 current = 1
            if current <= 1 :
                 next = current + 1
                 prev = 1

            else:    
                next = current + 1
                prev = current - 1
            
            if course.exists():
                course = course.first()
            else:
                return HttpResponse('404')
            author = Author.objects.get(course= course)
            print(course)
            next_lec = Video.objects.filter(serial_number=next, course=course).first()
            
            prev_lec = Video.objects.filter(serial_number=prev, course=course).first()
            comment = Comment.objects.filter(course=course)
            context = {'course' : course,
                        'author' :author, 'video': video, 'next':next, 'prev':prev, 'next_lec':next_lec, 'prev_lec':prev_lec, 
                        'forms':CommentForm, 'comment' :comment}
            return render(request, 'course/watch_course.html', context)




