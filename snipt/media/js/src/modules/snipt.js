
(function(Snipt) {

    SniptModel = Backbone.Model.extend({
    });
    SniptView = Backbone.View.extend({

        tagName: 'article',

        initialize: function() {
            this.model.view = this;
            this.model.bind('change', this.render, this);
            this.model.bind('destroy', this.remove, this);

            this.template     = _.template($('#snipt').html());
            this.editTemplate = _.template($('#edit').html());

            this.initLocalVars();
        },
        events: {
            'click a.copy':     'copyFromClick',
            'click a.edit':     'edit',
            'click a.embed':    'embed',
            'click a.expand':   'expand',
            'click .container': 'selectFromClick',
            'copyRaw':          'copy',
            'copyClose':        'copyClose',
            'detail':           'detail',
            'deselect':         'deselect',
            'edit':             'edit',
            'embed':            'embed',
            'expand':           'expand',
            'next':             'next',
            'prev':             'prev',
            'selectSnipt':      'select'
        },

        copy: function() {
            if (!this.$copyModal.is(':visible')) {
                var cmd;
                if (navigator.platform == 'MacPPC' ||
                    navigator.platform == 'MacIntel') {
                    cmd = 'Cmd';
                }
                else {
                    cmd = 'Ctrl';
                }

                this.$copyModalBody.append('<textarea class="raw"></textarea>');
                $textarea = $('textarea.raw', this.$copyModalBody).val(this.$raw.text());

                this.$copyModalType.text(cmd);
                this.$copyModal.modal('show');
                $textarea.select();
            }
        },
        copyClose: function() {
            console.log('copyClose called');
            $('textarea', this.$copyModal).remove();
        },
        copyFromClick: function() {
            this.copy();
            return false;
        },
        deselect: function() {
            if (!this.$copyModal.is(':visible')) {
                this.$el.removeClass('selected');
                window.$selected = false;
            }
        },
        detail: function() {
            window.location = this.model.get('get_absolute_url');
        },
        edit: function() {
            if (!$('section.main-edit:visible').length) {
                this.select();
                var editPane = this.editTemplate(this.model.toJSON());
                $('section#main').hide();
                $('section#main-edit').html(editPane).show();
            }
            return false;
        },
        embed: function() {
            alert('TODO');
            return false;
        },
        expand: function() {
            this.$container.toggleClass('expanded', 100);
            this.$tags.toggleClass('expanded');
            this.select();
            return false;
        },
        initLocalVars: function() {
            this.$el = $(this.el);
            this.$aside = $('aside', this.$el);
            this.$container = $('div.container', this.$el);
            this.$copyModal = $('div.copy-modal', this.$el);
            this.$copyModalBody = $('div.modal-body', this.$copyModal);
            this.$copyModalClose = $('a.close', this.$copyModal);
            this.$copyModalType = $('h4 span', this.$copyModal);
            this.$h1 = $('header h1 a', this.$el);
            this.$raw = $('div.raw', this.$el);
            this.$tags = $('section.tags ul', this.$aside);

            this.$copyModal.on('hidden', function(e) {
                $(this).parent().trigger('copyClose');
            });
        },
        next: function() {
            window.site.$copyModals.modal('hide');
            nextSnipt = this.$el.next('article.snipt');
            if (nextSnipt.length) {
                return nextSnipt.trigger('selectSnipt');
            }
        },
        prev: function() {
            window.site.$copyModals.modal('hide');
            prevSnipt = this.$el.prev('article.snipt');
            if (prevSnipt.length) {
                return prevSnipt.trigger('selectSnipt');
            }
        },
        remove: function() {
            console.log('SniptView.remove() called');
        },
        render: function() {

            this.$el.html(this.template({
                snipt: this.model.toJSON()
            }));
            this.initLocalVars();

            if (this.model.get('pub') === true) {
                this.$el.removeClass('private-snipt');
            } else {
                this.$el.addClass('private-snipt');
            }

            if (this.model.get('user').username === window.user) {
                this.$el.addClass('editable');
            } else {
                this.$el.removeClass('editable');
            }

            if (this.model.get('line_count') > 8 && !window.detail) {
                this.$el.addClass('expandable');
            } else {
                this.$el.removeClass('expandable');
            }

            $('script#disqus').remove();
            $('body').append('<script id="disqus" type="text/javascript">' + $('script#disqus-template').text() + '</script>');

            return this;
        },
        select: function(fromClick) {

            $('article.selected', SniptList.$el).removeClass('selected');
            this.$el.addClass('selected');

            if (fromClick !== true) {
                if (SniptList.$snipts.index(this.$el) === 0) {
                    window.scrollTo(0, 0);
                } else {
                    $('html, body').animate({
                        scrollTop: this.$el.offset().top - 50
                    }, 0);
                }
            }

            window.$selected = this.$el;
        },
        selectFromClick: function(e) {
            this.select(true);
            e.stopPropagation();
        }
    });
    SniptListView = Backbone.View.extend({
        el: 'section#snipts',

        initialize: function(opts) {

            this.$snipts = opts.snipts;
            this.$snipts.each(this.addExistingSnipt);
            this.$el = $(this.el);

            this.keyboardShortcuts();
        },

        addExistingSnipt: function() {

            var $el = $(this);
            var $created = $('li.created', $el);
            var $h1 = $('header h1 a', $el);
            var $pub = $('div.public', $el);
            var $user = $('li.author a', $el);
            var is_public = $pub.text() === 'True' ? true : false;
            var tag_lis = $('section.tags li', $el);
            var tags = [];

            for (var i=0; i < tag_lis.length; i++) {
                var $tag = $('a', tag_lis.eq(i));
                tags[i] = {
                    name: $tag.text(),
                    absolute_url: $tag.attr('href')
                };
            }

            var data = {
                code: $('div.raw', $el).text(),
                created: $created.attr('title'),
                created_formatted: $created.text(),
                embed_url: $('div.embed-url', $el).text(),
                get_absolute_url: $h1.attr('href'),
                pk: parseInt($el.attr('id').replace('snipt-', ''), 0),
                key: $('div.key', $el).text(),
                lexer: $('div.lexer', $el).text(),
                lexer_name: $('div.lexer-name', $el).text(),
                line_count: parseInt($('div.line-count', $el).text(), 0),
                modified: $('div.modified', $el).text(),
                pub: is_public,
                resource_uri: $('div.resource-uri', $el).text(),
                slug: $('div.slug', $el).text(),
                stylized: $('div.stylized', $el).text(),
                tags: tags,
                tags_list: $('div.tags-list', $el).text(),
                title: $h1.text(),
                user: {
                    get_absolute_url: $user.attr('href'),
                    username: $user.text()
                }
            };

            var view = new SniptView({
                el: this,
                model: new SniptModel(data)
            });
        },
        keyboardShortcuts: function() {

            $selected = window.selected;
            $document = $(document);

            $document.bind('keydown', 'j', function() {
                if (!$selected) {
                    SniptList.$snipts.eq(0).trigger('selectSnipt');
                } else {
                    $selected.trigger('next');
                }
            });
            $document.bind('keydown', 'k', function() {
                if (!$selected) {
                    SniptList.$snipts.eq(0).trigger('selectSnipt');
                } else {
                    $selected.trigger('prev');
                }
            });
            $document.bind('keydown', 'c', function(e) {
                if ($selected) {
                    e.preventDefault();
                    $selected.trigger('copyRaw');
                }
            });
            $document.bind('keydown', 'Ctrl+e', function() {
                if ($selected) {
                    if ($selected.hasClass('editable')) {
                        $selected.trigger('edit');
                    }
                }
            });
            $document.bind('keydown', 'esc', function() {
                if ($('section#main-edit:visible').length) {
                    $('section#main-edit').hide();
                    $('section#main').show();
                    $('html, body').animate({
                        scrollTop: $selected.offset().top - 50
                    }, 0);
                } else {
                    if ($selected) {
                        $selected.trigger('deselect');
                    }
                }
            });
            $document.bind('keydown', 'g', function() {
                if (window.$selected) {
                    window.$selected.trigger('deselect');
                }
                window.scrollTo(0, 0);
            });
            $document.bind('keydown', 'Shift+g', function() {
                if (window.$selected) {
                    window.$selected.trigger('deselect');
                }
                window.scrollTo(0, document.body.scrollHeight);
            });
            $document.bind('keydown', 'n', function() {
                var $anc = $('li.next a');
                if ($anc.length) {
                    if ($anc.attr('href') !== '#') {
                        window.location = $anc.attr('href');
                    }
                }
            });
            $document.bind('keydown', 'e', function() {
                if ($selected) {
                    if ($selected.hasClass('expandable')) {
                        $selected.trigger('expand');
                    }
                }
            });
            $document.bind('keydown', 'p', function() {
                var $anc = $('li.prev a');
                if ($anc.length) {
                    if ($anc.attr('href') !== '#') {
                        window.location = $anc.attr('href');
                    }
                }
            });
            $document.bind('keydown', 'v', function() {
                if ($selected) {
                    $selected.trigger('embed');
                }
            });
            $document.bind('keydown', 'o', function() {
                if ($selected) {
                    $selected.trigger('detail');
                }
            });
            $document.bind('keydown', 'return', function() {
                if ($selected) {
                    $selected.trigger('detail');
                }
            });
        }
    });
    Snipt.Views = {
        'SniptListView': SniptListView
    };

})(snipt.module('snipt'));
