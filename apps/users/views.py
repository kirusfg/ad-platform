from django.template.response import TemplateResponse
from django.views.decorators.http import require_http_methods


def test_page(request):
    return TemplateResponse(request, "test.html", {"count": 0})


@require_http_methods(["POST"])
def increment(request):
    count = int(request.POST.get("count", 0)) + 1
    return TemplateResponse(request, "test.html#counter-partial", {"count": count})
