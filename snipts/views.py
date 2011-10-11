from annoying.decorators import render_to
from snipts.api import PublicTagResource

@render_to('home.html')
def home(request):
    tr = PublicTagResource()
    tags_queryset = tr.cached_obj_get_list()[:20]
    tags_bundles = (tr.build_bundle(request=request, obj=tag) for tag in tags_queryset)
    tags = [tr.full_dehydrate(bundle) for bundle in tags_bundles]

    return {
        'tags': tags
    }
