
from django.template.loader import render_to_string


class BasicForm(object):

    def as_basic(self):
        return render_to_string('xhrforms/basic_form.html', {'basic_form': self})
