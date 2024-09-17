function applyPostAndCommentStyles(baseSelector) {
    const jQueryBase = $(baseSelector);
    if (jQueryBase.length <= 0) {
        return;
    }
    const jQueryPostContent = jQueryBase.find("#post__content");
    const jQueryCommentContent = jQueryBase.find(".comment__content");
    const jQueryPostAndCommentContent = $.merge(jQueryPostContent, jQueryCommentContent);

    // make all links except same-page ones indicated by custom markdown and same-page URL fragments
    // (including footnotes and footnote backrefs) open in new tab
    jQueryPostAndCommentContent.find("a").each(function() {
        if (!$(this).is("[data-same-page]") && !$(this).attr("href").startsWith("#")) {
            $(this).attr("target", "_blank");
        }
    });

    // add CSS classes for extra styling
    jQueryPostContent.find("h1").addClass("post__h1");
    jQueryCommentContent.find("h1").addClass("comment__h1");
    jQueryPostContent.find("h2").addClass("post__h2");
    jQueryCommentContent.find("h2").addClass("comment__h2");
    jQueryPostContent.find("img").addClass("post__img");
    jQueryCommentContent.find("img").addClass("comment__img");
    jQueryPostAndCommentContent.find(".post__h1, .comment__h1").addClass("fs-4");
    jQueryPostAndCommentContent.find(".post__h2, .comment__h2").addClass("fs-7");

    // images use alt text as hover text too
    jQueryPostAndCommentContent.find(".post__img[alt], .comment__img[alt]").each(function() {
        $(this).attr("title", $(this).attr("alt"));
    });
}

const ANCHORJS_OPTIONS = {
    icon: "\uF470",
    placement: "right"
};
function addPostAnchors() {
    anchors.options = ANCHORJS_OPTIONS;
    anchors.add(".post__h1, .post__h2");
}

// for syntax guide
function addCommentHoverTooltip() {
    let text = "";
    $("[data-comment-formatting-tooltip]").first().parent().prev().each(function() {
        text = $(this).text();
        $(this).html("<a id=\"comment-formatting-tooltip\"></a>"); // need `<a>` so tooltip disappears on hover end
    });

    $("#comment-formatting-tooltip")
            .append(`${text} (hover to show formatting options)`)
            .attr("data-bs-toggle", "tooltip")
            .attr("data-bs-custom-class", "tooltip--text-align-left")
            .attr("data-bs-html", "true")
            .attr("data-bs-title", `
                <ul class='mb-0'>
                  <li>Markdown
                    <ul>
                      <li>Tables: GFM, or reStructuredText Grid with line separators</li>
                      <li>No images</li>
                      <li>Links are not rendered; use plain text & no footnotes</li>
                    </ul>
                  </li>
                  <li>LaTeX (via MathJax)
                    <ul>
                      <li>Needs escaping: \\\\\\\\(, \\\\\\\\), \\\\\\\\[, \\\\\\\\], \\\\\\\\\\\\\\\\, and anything like \\\\* that may be interpreted as Markdown</li>
                    </ul>
                  </li>
                  <li>My custom inline Markdown syntax if you can figure it out :3</li>
                </ul>
            `);

    refreshTooltips("#leave-a-comment");
}

applyPostAndCommentStyles("body");
// must add anchors after applying `post__h1` etc. classes
addPostAnchors();
addCommentHoverTooltip();
