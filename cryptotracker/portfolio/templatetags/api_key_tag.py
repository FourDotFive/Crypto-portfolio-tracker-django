from django import template
import environ

register = template.Library()

env = environ.Env()
environ.Env.read_env()


@register.simple_tag
def get_cryptocompare_api_key():
    return env('cryptocompare_api_key')
