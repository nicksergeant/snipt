from django import template
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name

register = template.Library()


@register.filter
def pygmentize(text):
    return highlight(
        text,
        get_lexer_by_name("diff", encoding="UTF-8"),
        HtmlFormatter(
            linenos="table", anchorlinenos=True, lineanchors="L", linespans="L"
        ),
    )
