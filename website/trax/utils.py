from django.contrib.admin.views.decorators import staff_member_required
from django.forms import modelform_factory
from fuzzywuzzy import fuzz, process

def get_object_by_string(s, klass, attribute, score_cutoff=60):
    choices = klass.objects.all().values_list(attribute, flat=True)
    result = process.extractOne(s, choices, score_cutoff=score_cutoff)
    if result:
        return klass.objects.get(**{attribute:result[0]})


def is_staff_required(*a, **k):
    return staff_member_required(login_url='/accounts/login/', *a, **k)


class ModelFormWidgetMixin(object):
    def get_form_class(self):
        return modelform_factory(self.model, fields=self.fields,
                                 widgets=self.widgets)
