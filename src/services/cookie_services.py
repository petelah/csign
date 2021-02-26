def create_cookie(res, form):
	res.set_cookie('csign', 'signed_in', secure=True, max_age=60 * 60 * 24 * 365 * 1)
	res.set_cookie('csign-email', form.email.data, secure=True, max_age=60 * 60 * 24 * 365 * 1)
	res.set_cookie('csign-fname', form.first_name.data, secure=True, max_age=60 * 60 * 24 * 365 * 1)
	res.set_cookie('csign-lname', form.last_name.data, secure=True, max_age=60 * 60 * 24 * 365 * 1)
	res.set_cookie('csign-phone', form.phone_number.data, secure=True, max_age=60 * 60 * 24 * 365 * 1)


def grab_cookie(form, request):
	form.email.data = request.cookies.get('csign-email')
	form.first_name.data = request.cookies.get('csign-fname')
	form.last_name.data = request.cookies.get('csign-lname')
	form.phone_number.data = request.cookies.get('csign-phone')