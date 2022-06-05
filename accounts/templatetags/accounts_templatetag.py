from django import template


register = template.Library()


@register.simple_tag
def quiz_problem_text(quiz_problems, index):

    try:
        result = quiz_problems[int(index)]
        return result

    except:
        return ""