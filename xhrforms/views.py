
import json

from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.views.generic.edit import FormView

class XhrFormView(FormView):
    """
    Implements the ability to use the generic xhr submission of a
    core.forms.BasicForm form.

    adds methods:
    xhr_form_valid
    xhr_form_invalid

    validate_inline
        short circuits the normal submit flow so return validity of fields
        without submitting the form.
    """

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        if request.method == 'POST' and request.is_ajax():
            try:
                data = json.loads(request.raw_post_data)
            except ValueError:
                pass
            else:
                if 'inline_submit' in data:
                    return self.validate_inline(request, data)

        return super(XhrFormView, self).dispatch(request, *args, **kwargs)

    def form_invalid(self, form, *args, **kwargs):
        if not self.request.is_ajax():
            return super(XhrFormView, self).form_invalid(form, *args, **kwargs)
        else:
            return self.xhr_form_invalid(form)

    def form_valid(self, form, *args, **kwargs):
        if not self.request.is_ajax():
            return super(XhrFormView, self).form_valid(form, *args, **kwargs)
        else:
            return self.xhr_form_valid(form)

    def xhr_form_invalid(self, form):
        errors = dict([(k, form.error_class.as_text(v)) for k, v in form.errors.items()])
        return HttpResponse(json.dumps(errors), status=400, content_type='application/json')

    def xhr_form_valid(self, form):
        return HttpResponse('{}', content_type='application/json')

    def validate_inline(self, request, data):
        response_body = {'errors': {}}
        status = 200
        fields = data['fields']
        form = self.get_form(self.form_class)
        for field_name, value in fields.items():
            if not field_name in form.fields:
                response_body['errors'][field_name] = '%s is not a valid field' % field_name
                status = 400
                continue
            field = form.fields[field_name]
            # value_from_datadict() gets the data from the data dictionaries.
            # Each widget type knows how to retrieve its own data, because some
            # widgets split data over several HTML fields.
            value = field.widget.value_from_datadict(fields, {}, form.add_prefix(field_name))
            try:
                value = field.clean(value)
                form.cleaned_data = {field_name: value}
                if hasattr(form, 'clean_%s' % field_name):
                    getattr(form, 'clean_%s' % field_name)()
            except ValidationError as e:
                response_body['errors'][field_name] = e.messages
                status = 400

        return HttpResponse(json.dumps(response_body), status=status,
                            content_type='application/json')
