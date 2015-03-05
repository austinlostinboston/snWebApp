// Handles small events within post and user pages
function getPostLength() {
	var post = document.getElementById("post").value.toString();
	var postLength = post.length;

	return postLength
}

// Handles auto-refreshing of new posts
window.setInterval(function () {
    // counts number of posts on page
    var num_posts = $(".panel-heading").length;
    var csrftok = $("input[name=csrfmiddlewaretoken]").val();
    var logged_in_user = $('#' + (num_posts - 1) + 'logged_in_user').val();
    //var comment = $("#" + )

    console.log(logged_in_user)

    // sends number of posts to server
    $.ajax({
        url: "/get-posts-json",
        data: {num_posts:num_posts},
        dataType : "json",
        success: function( items ) {

            // Adds each new post to the frontpage
            $(items).each(function() {

                console.log(items);

                // Create csrf token hidden field
                var csrftoken = "<input type=\"hidden\" value=\"" + csrftok + "\" name=csrfmiddlewaretoken></input>";

                var imagePath = "";
                if (this.fields.user_profile_image.length > 0) {
                    imagePath = "<img src=" + this.fields.user_profile_image + " width=\"50px\" height=\"50px\">";
                }

                // F'ing annoying. Is there a better way to do this? xml maybe?
                // Or use createElements like we learned in like week 2, I'm stupid.
                $("#post-list").append(
                    "<div class=\"panel panel-default\">" +
                        "<div class=\"panel-heading\">" +
                            "<h4 class=\"text-only\">" +
                                imagePath +
                                "<a href=\"account/" + this.fields.user + "\"> " + this.fields.user + "</a>" +
                                " squeaked " + this.fields.content+ " at " + this.fields.dateTime +
                            "</h4>" + 
                        "</div>" +
                        "<div class=\"panel-body\">" +
                            "<div id=\"" + this.pk + "\" class=\"commentDiv\">" +
                              "<input type=\"hidden\" id=\"" + this.pk + "logged_in_user\" value=" + logged_in_user + ">" +
                              "<input type=\"hidden\" id=\"" + this.pk + "post_id\" value=" + this.pk + ">" +
                              "<div class=\"input-group\">" +
                                "<input class=\"form-control\" type=\"text\" id=\"" + this.pk + "comment-input\" placeholder=\"comment\" maxlength=\"160\">" +
                                csrftoken +
                                "<span class=\"input-group-btn\">" +
                                  "<button name=\"comment-button\" type=\"submit\" class=\"btn btn-default\">" +
                                    "<span class=\"glyphicon glyphicon-comment\" aria-hidden=\"true\"></span> Comment" +
                                  "</button>" +
                                "</span>" +
                              "</div>" +
                            "</div>" +
                        "</div>" +
                    "</div>"
                );
            });
        }
    });
}, 5000);

// Handles adding comment html without a refresh
console.log("startup...");
$(document).ready(function() {
    $('button[name=comment-button]').click(function() {
        // finds the div that were appending comments to
        var $div = $(this).parent('span').parent('div').parent('div');
        var post_id = $div.attr('id');

        // sets variables to be sent in json
        var logged_in_user = $('#' + post_id + 'logged_in_user').val();
        var comment = $('#' + post_id + 'comment-input').val();
        var dateTime = $.now();
        var csrftoken = $("input[name=csrfmiddlewaretoken]").val();

        var url = "/comment/" + post_id;

        // sanity check
        console.log(comment);

        // ajax call
        $.ajax({
            type: "POST",
            url: url,
            data: {user:logged_in_user, dateTime:dateTime, comment:comment, csrfmiddlewaretoken:csrftoken},
            dataType: "json",
            success: function(data) {
                // Adds each new post to the frontpage
                $(data).each(function() {
                    // sets the submitted comment input box value to nothin
                    $("#"+post_id+"comment-input").val("");

                    // sanity check
                    console.log(this.user_profile_image);

                    // checks for user image
                    var imagePath = "";
                    if (this.user_profile_image.length > 0) {
                        imagePath = "<img src=" + this.user_profile_image + " width=\"30px\" height=\"30px\">";
                    }

                    // outputs comment
                    $("div[name=comment-object" + post_id + "]").append(
                        "<h5 class=\"comment\" name=\"comment" + post_id + "\">" + 
                        imagePath +
                        "<a href=\"account/" + this.user + "\"> " + this.user + "</a>" +
                        " commented " + this.comment+ " at " + this.dateTime +
                        "</h5>"
                    );
                });
            }
        });
    });
});
