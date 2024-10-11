$(document).ready(function (){
    $(".likes-widget").click(like_post);
});

function like_post()
{
    let pk = $("article").data("pk");
    console.log("Liking " + pk);

    let url = "/blog/action/post-like/?pk=" + pk;

    fetch(url).then(response => response.json()).then(data => update_likes(data));
}

function update_likes(data)
{
    if (! data.success)
    {
        $(".likes-widget .likes-count").html("?");
    }
    else
    {
        $(".likes-widget .likes-count").html(data.total_likes);
        $(".likes-widget").addClass("liked");
    }
}
