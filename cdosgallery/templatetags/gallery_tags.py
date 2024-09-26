from django import template

register = template.Library()

@register.inclusion_tag("cdosgallery/subtemplates/character_block.html")
def character_block(character):
    return {"character": character}

@register.inclusion_tag("cdosgallery/subtemplates/exhibit_block.html")
def exhibit_block(exhibit):
    return {"exhibit": exhibit}

@register.inclusion_tag("cdosgallery/subtemplates/censored_exhibit_block.html")
def censored_exhibit_block(exhibit):
    return {"exhibit": exhibit}

@register.inclusion_tag("cdosgallery/subtemplates/paginator_block.html")
def paginator_block(page_obj):
    return {"page_obj": page_obj}
