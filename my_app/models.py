from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.contrib.auth.models import User

# Create your models here.
from django.contrib.auth.models import User
class CustomModelName(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # instead of user_id = IntegerField()
 
class Categories(models.Model):
    icon = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name
    
    def get_all_category(self):
        return Categories.objects.all().order_by('-id')[0:5]
    

class Language(models.Model):
    language = models.CharField(max_length=255)

    def __str__(self):
        return self.language
class Author(models.Model):
    author_profile = models.ImageField(upload_to='author', null=True, blank=True)
    name = models.CharField(max_length=255, null=True)
    author_designation = models.CharField(max_length=255, null=True)
    about_author = models.CharField(max_length=2555, null=True)

    def __str__(self):
        return self.name
    
class Level(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

class Course(models.Model):
    STATUS = (
        ('PUBLISH', 'PUBLISH'),
        ('DRAFT', 'DRAFT'),
    )
    featured_image = models.ImageField(upload_to='media/featured_img', null=True)
    featured_video = models.CharField(max_length=300, null=True)
    title = models.CharField(max_length=500)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Categories,on_delete=models.CASCADE, null=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, null=True)
    description = models.TextField()
    price = models.IntegerField(null=True, default=0)
    discount = models.IntegerField(null=True)
    
    slug = models.SlugField(default='', max_length=500, null=True, blank=True)
    status= models.CharField(choices=STATUS, max_length=100, null=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True)
    deadline_date = models.DateField(null=True)
    certificate = models.BooleanField(null=True, default=False)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('course_details', kwargs={'slug':self.slug})
    

    def __str__(self):
        return self.title
    

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Course.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s"(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, Course)
    

class what_you_learn(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    points = models.CharField(max_length=255)


    def __str__(self):
        return self.points
    
class Requirements(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    points = models.CharField(max_length=255)

    def __str__(self):
        return self.points
    
class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name + ' - ' + self.course.title
    

class Video(models.Model):
    serial_number = models.IntegerField(null=True)
    thumbnail = models.ImageField(upload_to='media/yt_thumbnail', null=True)
    course  = models.ForeignKey(Course, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    title = models.CharField(max_length=100) #javascript_headings
    youtube_id = models.CharField(max_length=200)#youtube_video_ids
    time_duration = models.FloatField(null=True)#array_50
    preview = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Contactus(models.Model):
    name = models.CharField(max_length=255)
    Email = models.EmailField(max_length=254)
    Message =models.TextField(null=True)

    def __str__(self):
        return self.name  + " - " + self.Email
# p = Video(Course=a, lesson=y, title=javascript_tutorial_topics[k], youtube_id=my_list[k], time_duration=array_of_50_numbers[k])
# y.save()





class User_Course(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    Course = models.ForeignKey(Course, on_delete=models.RESTRICT, null=True, blank=True)
    profession =models.CharField(max_length=500, null=True, blank=True)
    city =models.CharField(max_length=500, null=True, blank=True)
    country =models.CharField(max_length=500, null=True, blank=True)
    postcode =models.CharField(max_length=500, null=True, blank=True)
    Phone =models.CharField(max_length=500, null=True, blank=True)
    razor_pay_order_id = models.CharField(max_length=500, null=True, blank=True)
    razor_pay_payment_id = models.CharField(max_length=500, null=True, blank=True)
    razor_pay_payment_signature = models.CharField(max_length=500, null=True, blank=True)
    paid = models.BooleanField(default=False)
    date  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name + ' - ' + self.Course.title
    

class Comment(models.Model):
    RATING = (("Below Average","Below Average"), ("Partly Average","Partly Average"), ("Average","Average"), ("Very Good","Very Good"), ("Excellent","Excellent"))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    rating = models.CharField(choices=RATING, max_length=100, null=True)
    content = models.TextField()

    def __str__(self):
        return self.user.username
    
    
