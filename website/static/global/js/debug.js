"use strict";
// Debug functions for development only included when ?debug=1 or Django's DEBUG setting is true
$("document").ready(function (){
    var pairs = [];
    var preview_image_url = "";
    $("meta").each(function (){
        var key = $(this).attr("name");
        if (! key)
            key = $(this).attr("property");
        else if (key.indexOf("twitter") == 0)
            key = "t:" + key.split(":")[1];

        var val = $(this).attr("content");

        pairs.push([key, val]);
    });

    let output = "";
    for (let idx = 0; idx < pairs.length; idx++)
    {
        output += `<tr><th>${pairs[idx][0]}</th><td class="l">${pairs[idx][1]}</td></tr>\n`;
        if (pairs[idx][0] == "og:image")
            preview_image_url = pairs[idx][1];
    }
    $("#meta-preview-image").attr("src", preview_image_url);
    $("#meta-tags").html($("#meta-tags").html() + output);
});
