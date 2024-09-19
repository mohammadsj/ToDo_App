{% extends "mail_templated/base.tpl" %}

{% block subject %}
Hello
{% endblock %}

{% block body %}
This is for reset password
{% endblock %}

{% block html %}
http://127.0.0.1:7000/accounts/api/v1/password-reset-confirm/{{token}}
{% endblock %}