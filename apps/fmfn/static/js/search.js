$(document).ready(function () {
    $("form").submit(function (e) {
        e.preventDefault();

        prefixUrl = $(this).attr("action");
        $('input[name=prefix-url]').val(prefixUrl);
        url = $(this).attr("action") + '?page=1';
        console.log(url);
        console.log($(this).serialize());
        doSearch(url);
    });
});

function doSearch(url) {
    $.ajax(url, {
        method: 'POST',
        data: $("form").serialize(),
        success: function (data, textStatus, jqXHR) {
            $('#results-content').html('');
            console.log(JSON.stringify(data));
            var html = '';
            var results = data.results;
            var pages = data.pages;
            var overhead = pages.count % pages.total;
            console.log('elementos: ' + overhead);
            var title, description, themes, languages, types, ages, rating, materialId, url;
            var j;

            var start, end, total;
            total = pages.count;
            if (pages.current == 1) {
                if (pages.count < pages.page_size) {
                    start = 1;
                    end = pages.count;
                } else {
                    start = 1;
                    end = pages.page_size * pages.current;
                }
            } else if (pages.current == pages.total) {
                start = pages.page_size * pages.current - pages.page_size;
                end = start + overhead;
            } else {
                end = pages.page_size * pages.current;
                start = end - pages.page_size;
            }

            var itemCount = '<div class="items-count">' + 'Mostrando ' + start + ' al ' + end + ' de ' + pages.count + ' resultados' + '</div>';

            $('#results-content').append(itemCount);

            for (var i = 0; i < data.results.length; i++) {
                title = results[i].title;

                description = results[i].description.substring(0, 240);
                if (description.length > 240) {
                    description += '...';
                }

                themes = results[i].tags.themes;
                languages = results[i].tags.languages;
                types = results[i].tags.types;
                ages = results[i].tags.ages;
                console.log(ages);
                rating = results[i].rating;
                materialId = results[i].id;
                url = '/content/' + materialId + '/';

                var stars = '<div class="stars">';
                stars += '<i class="fa fa-star filled"></i>'.repeat(rating);
                stars += '<i class="fa fa-star-o"></i>'.repeat(5 - rating);
                stars += '</div>';

                var containerTags = '<div class="tags-container">';
                for (j = 0; j < themes.length; j++) {
                    containerTags += '<div class="material-tags">' + themes[j] + '</div>';
                }

                for (j = 0; j < types.length; j++) {
                    containerTags += '<div class="material-tags">' + types[j] + '</div>';
                }

                for (j = 0; j < languages.length; j++) {
                    containerTags += '<div class="material-tags">' + languages[j] + '</div>';
                }

                for (j = 0; j < ages.length; j++) {
                    containerTags += '<div class="material-tags">' + ages[j] + '</div>';
                }
                containerTags += '</div>';

                var materialCard = '<div class="material-card">';
                materialCard += '<a class="title" href="' + url + '" target="_blank">' + title + '</a>';
                materialCard += stars;
                materialCard += '<div class="description">' + description + '</div>';
                materialCard += containerTags;

                $('#results-content').append(materialCard);
            }

            var navigation = '<div class="navigation-pages">';
            if (pages.prev != null) {
                navigation += '<a href="#" id="' + $('input[name=prefix-url]').val() + '?page=' + pages.prev + '" class="navigate search-ajax-back"> <i class="fa fa-chevron-left"></i> Anterior </a>';
            }
            navigation += '<span class="current"> pagina ' + pages.current + ' de ' + pages.total + '</span>';
            if (pages.next != null) {
                navigation += '<a href="#" id="' + $('input[name=prefix-url]').val() + '?page=' + pages.next + '" class="navigate search-ajax-next"> Siguiente <i class="fa fa-chevron-right"></i> </a>';
            }

            $('#results-content').append(navigation);
            $('#results').show();
            $('#make-search').hide();
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log(errorThrown);
        }
    });
}

$(document).on('click', '.search-ajax-next', function () {
    var url = this.id;
    doSearch(url);
});

$(document).on('click', '.search-ajax-back', function () {
    var url = this.id;
    doSearch(url);
});