import factory
import factory.fuzzy
from django.contrib.auth import get_user_model

from model.user.models import User
from model.routine.models import Routine
from model.routine.models import RoutineDay
from model.routine.models import RoutineResult
from model.routine.choices import CATEGORY_CHOICES
from model.routine.choices import RESULT_CHOICES
from model.routine.choices import WEEKDAY_CHOICES

UserModel = get_user_model()


class RoutineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Routine
    
    account = factory.Iterator(User.objects.all())
    title = factory.fuzzy.FuzzyText(length=20)
    category = factory.fuzzy.FuzzyChoice(
        CATEGORY_CHOICES,
        getter=lambda c: c[0]
    )
    goal = factory.Faker("sentence")
    is_alarm = True


class RoutineDayFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RoutineDay
        django_get_or_create = ('day', 'routine')
    
    day = factory.fuzzy.FuzzyChoice(
        WEEKDAY_CHOICES,
        getter=lambda c: c[0]
    )
    routine = factory.Iterator(Routine.objects.all())


class RoutineResultFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RoutineResult
    
    result = factory.fuzzy.FuzzyChoice(
        RESULT_CHOICES,
        getter=lambda c: c[0]
    )
    routine = factory.Iterator(Routine.objects.all())
