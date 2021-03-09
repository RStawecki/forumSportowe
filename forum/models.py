from django.db.models import *
from accounts.models import User
from datetime import datetime, timezone

class Question(Model):
    title = CharField(max_length=250)
    desc = TextField()
    image = ImageField(blank=True, upload_to='images/')
    createDate = DateTimeField(auto_now_add=True)
    user = ForeignKey(User, on_delete=CASCADE)

    categories = [
        ("", 'Choose category'),
        ('ft', 'Football'),
        ('bs', 'Basketball'),
        ('sj', 'Ski Jumping'),
        ('hb', 'Handball'),
        ('bx', 'Boxing'),
        ('vb', 'Volleyball')
    ]

    category = CharField(max_length=2, choices=categories, default='')
    likes = ManyToManyField(User, related_name='likes', blank=True)

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    def display_date(self):
        tz = timezone.utc
        actualDate = datetime.now(tz)
        diffDate = (actualDate - self.createDate).total_seconds()
        if(diffDate >= 86400):
            return str(round(diffDate/60/60/24)) + " d. ago"
        elif(diffDate > 3600 and diffDate < 86400):
            return str(round(diffDate/60/60)) + " h. ago"
        else:
            return str(round(diffDate/60)) + " min. ago"


class Answer(Model):
    desc = TextField()
    createDate = DateTimeField(auto_now_add=True)
    user = ForeignKey(User, on_delete=CASCADE)
    question = ForeignKey(Question, on_delete=CASCADE, related_name='answers')
    image = ImageField(blank=True, upload_to='images/')

    def __str__(self):
        return self.desc[:15]

    

