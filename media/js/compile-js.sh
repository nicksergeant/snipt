#!/bin/bash

cat media/js/src/application.js|jsmin > media/js/src/application.min.js
cat media/js/src/modules/site.js|jsmin > media/js/src/modules/site.min.js
cat media/js/src/modules/snipt.js|jsmin > media/js/src/modules/snipt.min.js

cat media/js/src/pro.js|jsmin > media/js/src/pro.min.js

cat media/js/libs/underscore.js \
    media/js/libs/json2.js \
    media/js/libs/backbone.js \
    media/js/libs/bootstrap.js \
    media/js/plugins/jquery.hotkeys.js \
    media/js/plugins/jquery.infieldlabel.js \
    media/js/plugins/jquery.chosen.js \
    media/js/src/application.min.js \
    media/js/src/modules/site.min.js \
    media/js/src/modules/snipt.min.js \
    media/js/libs/codemirror.js \
    > media/js/snipt.js

cat media/js/src/pro.js \
    > media/js/pro.js
