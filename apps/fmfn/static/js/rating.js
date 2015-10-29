var __slice = [].slice;

(function ($, window) {
    var Starrr;

    Starrr = (function () {
        Starrr.prototype.defaults = {
            rating: void 0,
            numStars: 5,
            change: function (e, value) {
            }
        };

        function Starrr($el, options) {
            var i, _, _ref,
                _this = this;

            this.options = $.extend({}, this.defaults, options);
            this.$el = $el;
            _ref = this.defaults;
            for (i in _ref) {
                _ = _ref[i];
                if (this.$el.data(i) != null) {
                    this.options[i] = this.$el.data(i);
                }
            }
            this.createStars();
            this.syncRating();
            this.$el.on('mouseover.starrr', 'i', function (e) {
                return _this.syncRating(_this.$el.find('i').index(e.currentTarget) + 1);
            });
            this.$el.on('mouseout.starrr', function () {
                return _this.syncRating();
            });
            this.$el.on('click.starrr', 'i', function (e) {
                return _this.setRating(_this.$el.find('i').index(e.currentTarget) + 1);
            });
            this.$el.on('starrr:change', this.options.change);
        }

        Starrr.prototype.createStars = function () {
            var _i, _ref, _results;

            _results = [];
            for (_i = 1, _ref = this.options.numStars; 1 <= _ref ? _i <= _ref : _i >= _ref; 1 <= _ref ? _i++ : _i--) {
                _results.push(this.$el.append("<i class='fa fa-star-o'></i>"));
            }
            return _results;
        };

        Starrr.prototype.setRating = function (rating) {
            if (this.options.rating === rating) {
                rating = void 0;
            }
            this.options.rating = rating;
            this.syncRating();
            return this.$el.trigger('starrr:change', rating);
        };

        Starrr.prototype.syncRating = function (rating) {
            var i, _i, _j, _ref;

            rating || (rating = this.options.rating);
            if (rating) {
                for (i = _i = 0, _ref = rating - 1; 0 <= _ref ? _i <= _ref : _i >= _ref; i = 0 <= _ref ? ++_i : --_i) {
                    this.$el.find('i').eq(i).removeClass('fa-star-o').addClass('fa-star filled');
                }
            }
            if (rating && rating < 5) {
                for (i = _j = rating; rating <= 4 ? _j <= 4 : _j >= 4; i = rating <= 4 ? ++_j : --_j) {
                    this.$el.find('i').eq(i).removeClass('fa-star filled').addClass('fa-star-o');
                }
            }
            if (!rating) {
                return this.$el.find('i').removeClass('fa-star filled').addClass('fa-star-o');
            }
        };

        return Starrr;

    })();
    return $.fn.extend({
        starrr: function () {
            var args, option;

            option = arguments[0], args = 2 <= arguments.length ? __slice.call(arguments, 1) : [];
            return this.each(function () {
                var data;

                data = $(this).data('star-rating');
                if (!data) {
                    $(this).data('star-rating', (data = new Starrr($(this), option)));
                }
                if (typeof option === 'string') {
                    return data[option].apply(data, args);
                }
            });
        }
    });
})(window.jQuery, window);

$(function () {
    return $(".starrr").starrr();
});

$(document).ready(function () {

    $('#stars').on('starrr:change', function (e, value) {
        $('#count').val(value);
    });

    $('#send-comment').click(function () {
        console.log('hi');
        var csfrToken = $("input[name=csrfmiddlewaretoken]").val();
        var url = $("input[name=url-material]").val();
        var userId = $("input[name=id-user]").val();
        var contentId = $("input[name=id-content]").val();
        var rating = $("#count").val();
        var content = $('#comment-content').val();
        var contentTest = content.replace(/\s+/g, '');
        if (content.length == 0 || contentTest == 0) {
            $('#comment-error').show();
        } else {
            $('#comment-error').hide();
            $.ajax({
                url: url,
                type: "POST",
                data: {
                    csrfmiddlewaretoken: csfrToken,
                    rating_value: rating,
                    content: content
                },
                success: function (response) {
                    $('#comment-form').hide();
                    $('.no-comments').hide();
                    console.log(response);
                    var comment = response.data;
                    var missingRating = 5 - comment.rating;
                    var user = '<div class="author display-in-line">By:' + comment.user + '</div>';
                    var content = '<p class="content">' + comment.content + '</p>';
                    var rating = '<div class="rating display-in-line">';
                    console.log(comment.rating);
                    for (var i = 0; i < comment.rating; i++) {
                        rating += '<i class="fa fa-star filled"></i>';
                    }

                    for (var j = 0; j < missingRating; j++) {
                        rating += '<i class="fa fa-star-o"></i>';
                    }

                    rating += '</div>';
                    var inner = user + rating + content;
                    var html = '<div class="ind-comment">' + inner + '</div>';
                    console.log(html);
                    $('#material-comments').append(html);
                },
                error: function (xhr, textStatus, thrownError) {
                    console.log(xhr.statusText);
                    if (xhr.statusText) {
                        alert('Error: al publicar tu comentario, intentalo de nuevo');
                    }
                }
            });
        }
    });

    $('#leave-comment').click(function () {
        $(this).hide();
        $('#comment-form').show('slow');
    });
});