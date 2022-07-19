(function($){
    $.fn.extend({
        text_to_stars: function() {

            return this.each(function() {
                var rating_score = $(this).text().split("/")[0];
                var total_score = $(this).text().split("/")[1];

                $(this).text('');

                for (var i=0; i<total_score; i++) {
                    var rating_span = $("<span></span>");
                    if (i <= rating_score-1)
                        rating_span.addClass("star_on");
                    $(this).append(rating_span);
                }
            });

        }
    });
})(jQuery);