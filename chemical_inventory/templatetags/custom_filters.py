import datetime

from django import template
from django.utils.html import escape, mark_safe

from ..models import Container, expired_containers, Location
from django.contrib.auth.models import User

register = template.Library()


@register.filter
def subtract(value, arg):
	return value - arg


@register.filter(name='formula_markup')
def formula_markup(formula):
	def insert_subscript(string, index):
		return string[:index] + '<sub>' + string[index:index+2] + '</sub>' + string[index+2:]
	def insert_superscript(string, index):
		return string[:index] + '<sup>' + string[index:index+2] + '</sup>' + string[index+2:]
	def insert_bullet(string, index):
		return string[:index] + '&bull;' + string[index+1:]

	formula = escape(formula)
	x = 0
	while x in range (0, len(formula)):
		if formula[x] in ('_'):
			formula = insert_subscript(formula, x)
			x += 5
		if formula[x] in ('^'):
			formula = insert_superscript(formula, x)
			x += 5
		if formula[x] in ('|'):
			formula = insert_bullet(formula, x)
			x += 6
		x += 1
	formula = formula.replace("_","").replace("^", "")
	return mark_safe(formula)
