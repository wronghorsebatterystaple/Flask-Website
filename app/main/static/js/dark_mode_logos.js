onDarkModeChange = addToFunction(onDarkModeChange, function(enabled) {
    const jQFooterIconGitHub = $("#footer__icon--github");
    if (!jQFooterIconGitHub) {
        return;
    }

    if (enabled) {
        jQFooterIconGitHub.attr("src", URL_ICON_GITHUB_DARK);
    } else {
        jQFooterIconGitHub.attr("src", URL_ICON_GITHUB_LIGHT);
    }
});