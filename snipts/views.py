from annoying.decorators import render_to
from snipts.api import PublicSniptResource, PublicTagResource

@render_to('home.html')
def home(request):

    tr = PublicTagResource()
    #tags_queryset = tr.cached_obj_get_list()[:20]
    tags_queryset = tr.obj_get_list()[:20]
    tags_bundles = (tr.build_bundle(request=request, obj=tag) for tag in tags_queryset)
    tags = [tr.full_dehydrate(bundle) for bundle in tags_bundles]

    sr = PublicSniptResource()
    #snipts_queryset = sr.cached_obj_get_list()[:20]
    snipts_queryset = sr.obj_get_list()[:20]
    snipts_bundles = (sr.build_bundle(request=request, obj=snipt) for snipt in snipts_queryset)
    snipts = [sr.full_dehydrate(bundle) for bundle in snipts_bundles]

    return {
        'snipts': snipts,
        'tags': tags,
    }
