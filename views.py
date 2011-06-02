from annoying.decorators import render_to

@render_to('home.html')
def home(request):
    return {}
