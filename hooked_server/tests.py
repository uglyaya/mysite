from django.test import TestCase
from hooked_server.models import Person
# Create your tests here.

# Person.objects.create(name='aya',age='23');

p = Person.objects.get(id=1)
p.name ='aya2'
p.save()
print str(Person.objects.all().query)
print str(Person.objects.filter(id=1).query)