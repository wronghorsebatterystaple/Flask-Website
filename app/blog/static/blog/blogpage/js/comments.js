var DIGITS_RE = /\d+/;

// Reveal fields for comment on clicking a reply button
$(document).on("submit", ".comment-reply-btn", function(e) {
    e.preventDefault();

    var id = $(this).attr("id").match(DIGITS_RE)[0];
    var commentReplyForm_elem = $(`#comment-reply-form-${id}`);
    commentReplyForm_elem.removeAttr("hidden");
    commentReplyForm_elem.find("#parent").val(id); // insert under right parent
    commentReplyForm_elem.find("#author-input").focus();
    e.target.setAttribute("hidden", "");

    asteriskRequiredFields();
});

// Populate comment id hidden fields for comment deletion
function loadDeleteButtonIDs() {
    $(".comment-delete-btn").each(function() {
        var id = $(this).attr("id").match(DIGITS_RE)[0];
        $(this).find("#id").val(id);
    });
}
$(document).ready(loadDeleteButtonIDs)

function onCommentReload() {
    flask_moment_render_all();
    loadDeleteButtonIDs();
}

$(document).on("submit", ".comment-ajax", function(e) {
    e.preventDefault();

    var formData = new FormData($(e.target).get(0), $(e.originalEvent.submitter).get(0));
    $.ajax({
        type: "POST",
        url: window.location.pathname + window.location.search,
        data: formData,
        processData: false,
        contentType: false,
        dataType: "json"
    })
    .done(function(response) {
        if (response.redirect_uri) {
            var newURI = response.redirect_uri;
            if (response.flash_message) {
                newURI += `?flash=${encodeURIComponent(response.flash_message)}`;
            }
            window.location.href = newURI;
        } else {
            if (response.flash_message) {
                customFlash(response.flash_message);
            }

            if (response.submission_errors) {
                errors = response.submission_errors;
                Object.keys(errors).forEach((field_name) => {
                    var field_elem = $(e.target).find(`#${field_name}-field`)
                    field_elem.find(`#${field_name}-input`).addClass("is-invalid");
                    field_elem.find(".invalid-feedback").text(errors[field_name][0]);
                    });
            }

            if (response.success) {
                $(e.target).find("*").filter(function() {
                    return this.id.match(/.*-input/);
                }).val("");
                $("#commentlist").load(window.location.href + " #commentlist > *", onCommentReload);
            }
        }
    });
});
