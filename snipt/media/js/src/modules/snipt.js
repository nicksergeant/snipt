
(function(Snipt) {

    Snipt.SniptModel = Backbone.Model.extend({
    });
    Snipt.SniptView = Backbone.View.extend({

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
            'click a.embed':    'embedFromClick',
            'click a.expand':   'expand',
            'click .container': 'selectFromClick',
            'copyRaw':          'copy',
            'copyClose':        'copyClose',
            'detail':           'detail',
            'deselect':         'deselect',
            'edit':             'edit',
            'embed':            'embed',
            'embedClose':       'embedClose',
            'expand':           'expand',
            'next':             'next',
            'prev':             'prev',
            'selectSnipt':      'select'
        },

        copy: function() {
            if (!window.ui_halted) {
                window.ui_halted = true;

                this.$copyModalBody.append('<textarea class="raw"></textarea>');
                $textarea = $('textarea.raw', this.$copyModalBody).val(this.model.get('code'));

                this.$copyModal.modal('show');
                $textarea.select();
            }
        },
        copyClose: function() {
            $('textarea', this.$copyModal).remove();
        },
        copyFromClick: function() {
            this.copy();
            return false;
        },
        deselect: function() {
            this.$el.removeClass('selected');
            window.$selected = false;
        },
        detail: function() {
            window.location = this.model.get('get_absolute_url');
        },
        edit: function() {
            if (!window.ui_halted) {
                this.select();
                var editPane = this.editTemplate({
                    snipt: this.model.toJSON()
                });
                window.site.$main.hide();
                window.site.$body.addClass('detail editing');
                window.site.$main_edit.html(editPane).show();

                $('div#editor', window.site.$main_edit).css('height', ($(window).height() - 187));
                window.editor = ace.edit('editor');
                window.editor.setTheme('ace/theme/tomorrow');
                window.editor.renderer.setShowGutter(false);
                var JavaScriptMode = require('ace/mode/javascript').Mode;
                window.editor.getSession().setMode(new JavaScriptMode());
                
                window.editor.$textarea = $('textarea', window.editor.container);
                window.editor.focus();
                window.editor.$textarea.bind('keydown', 'esc', function(e) {
                    $(this).blur();
                    return false;
                });

                window.scrollTo(0, 0);

                window.editing = true;
                window.ui_halted = true;
            }
            return false;
        },
        embed: function() {
            if (!window.ui_halted) {
                window.ui_halted = true;

                this.$embedModalBody.append('<textarea class="raw"></textarea>');
                $textarea = $('textarea.raw', this.$embedModalBody).val('<script type="text/javascript">' + this.model.get('embed_url') + '</script>');

                this.$embedModal.modal('show');
                $textarea.select();
            }
        },
        embedClose: function() {
            $('textarea', this.$embedModal).remove();
        },
        embedFromClick: function() {
            this.embed();
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

            this.$embedModal = $('div.embed-modal', this.$el);
            this.$embedModalBody = $('div.modal-body', this.$embedModal);

            this.$h1 = $('header h1 a', this.$el);
            this.$tags = $('section.tags ul', this.$aside);

            this.$copyModal.on('hidden', function(e) {
                $(this).parent().trigger('copyClose');
                window.ui_halted = false;
                window.from_modal = true;
            });
            this.$embedModal.on('hidden', function(e) {
                $(this).parent().trigger('embedClose');
                window.ui_halted = false;
                window.from_modal = true;
            });
        },
        next: function() {
            if (!window.ui_halted) {
                nextSnipt = this.$el.next('article.snipt');
                if (nextSnipt.length) {
                    return nextSnipt.trigger('selectSnipt');
                }
            }
        },
        prev: function() {
            if (!window.ui_halted) {
                prevSnipt = this.$el.prev('article.snipt');
                if (prevSnipt.length) {
                    return prevSnipt.trigger('selectSnipt');
                }
            }
        },
        remove: function() {
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
            window.site.$body.append('<script id="disqus" type="text/javascript">' + $('script#disqus-template').text() + '</script>');

            return this;
        },
        select: function(fromClick) {

            $('article.selected', window.site.snipt_list.$el).removeClass('selected');
            this.$el.addClass('selected');

            if (fromClick !== true) {
                if (window.site.$snipts.index(this.$el) === 0) {
                    window.scrollTo(0, 0);
                } else {
                    window.site.$html_body.animate({
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
    Snipt.SniptListView = Backbone.View.extend({
        el: 'section#snipts',

        initialize: function(opts) {

            opts.snipts.each(this.addExistingSnipt);
            this.$el = $(this.el);

            this.keyboardShortcuts();

            var cmd;
            if (navigator.platform == 'MacPPC' ||
                navigator.platform == 'MacIntel') {
                cmd = 'Cmd';
            }
            else {
                cmd = 'Ctrl';
            }
            $('span.cmd-ctrl').text(cmd);
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
                code: $('div.raw', $el).html(),
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

            var view = new Snipt.SniptView({
                el: this,
                model: new Snipt.SniptModel(data)
            });
        },
        keyboardShortcuts: function() {

            $selected = window.selected;
            $document = $(document);

            $document.bind('keydown', 'j', function() {
                if (!window.ui_halted) {
                    if (!$selected) {
                        window.site.$snipts.eq(0).trigger('selectSnipt');
                    } else {
                        $selected.trigger('next');
                    }
                }
            });
            $document.bind('keydown', 'k', function() {
                if (!window.ui_halted) {
                    if (!$selected) {
                        window.site.$snipts.eq(0).trigger('selectSnipt');
                    } else {
                        $selected.trigger('prev');
                    }
                }
            });
            $document.bind('keydown', 'c', function(e) {
                if (!window.ui_halted) {
                    if ($selected) {
                        e.preventDefault();
                        $selected.trigger('copyRaw');
                    }
                }
            });
            $document.bind('keydown', 'Ctrl+e', function() {
                if (!window.ui_halted) {
                    if ($selected) {
                        if ($selected.hasClass('editable')) {
                            $selected.trigger('edit');
                        }
                    }
                }
            });
            $document.bind('keydown', 'esc', function() {
                if (window.editing) {
                    if (!window.site.$html.hasClass('detail')) {
                        window.site.$body.removeClass('detail');
                    }
                    window.site.$main_edit.hide();
                    window.site.$body.removeClass('editing');
                    window.site.$main.show();

                    window.editing = true;
                    window.ui_halted = false;

                    if (window.site.$snipts.index(window.$selected) === 0) {
                        window.scrollTo(0, 0);
                    } else {
                        window.site.$html_body.animate({
                            scrollTop: window.$selected.offset().top - 50
                        }, 0);
                    }
                } else {
                    if (!window.ui_halted) {
                        if ($selected) {
                            $selected.trigger('deselect');
                        }
                    }
                }
            });
            $document.bind('keydown', 'g', function() {
                if (!window.ui_halted) {
                    if (window.$selected) {
                        window.$selected.trigger('deselect');
                    }
                    window.scrollTo(0, 0);
                }
            });
            $document.bind('keydown', 'Shift+g', function() {
                if (!window.ui_halted) {
                    if (window.$selected) {
                        window.$selected.trigger('deselect');
                    }
                    window.scrollTo(0, document.body.scrollHeight);
                }
            });
            $document.bind('keydown', 'n', function() {
                if (!window.ui_halted) {
                    var $anc = $('li.next a');
                    if ($anc.length) {
                        if ($anc.attr('href') !== '#') {
                            window.location = $anc.attr('href');
                        }
                    }
                }
            });
            $document.bind('keydown', 'e', function() {
                if (!window.ui_halted) {
                    if ($selected) {
                        if ($selected.hasClass('expandable')) {
                            $selected.trigger('expand');
                        }
                    }
                }
            });
            $document.bind('keydown', 'p', function() {
                if (!window.ui_halted) {
                    var $anc = $('li.prev a');
                    if ($anc.length) {
                        if ($anc.attr('href') !== '#') {
                            window.location = $anc.attr('href');
                        }
                    }
                }
            });
            $document.bind('keydown', 'v', function(e) {
                if (!window.ui_halted) {
                    if ($selected) {
                        e.preventDefault();
                        $selected.trigger('embed');
                    }
                }
            });
            $document.bind('keydown', 'o', function() {
                if (!window.ui_halted) {
                    if ($selected) {
                        $selected.trigger('detail');
                    }
                }
            });
            $document.bind('keydown', 'return', function() {
                if (!window.ui_halted) {
                    if ($selected) {
                        $selected.trigger('detail');
                    }
                }
            });
        }
    });

})(snipt.module('snipt'));
