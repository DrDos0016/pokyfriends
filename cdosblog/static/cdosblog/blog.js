var overlay_return_pos = {"x": 0, "y": 0}

$(document).ready(function (){
    $(".likes-widget").click(like_post);
    $(".thumb-link").click(overlay_image);
    $("body").on("click", "#overlay-close-button", overlay_close);
    $("body").on("click", "#image-overlay", overlay_close);
});

function like_post()
{
    let pk = $("article").data("pk");

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



function overlay_close(e)
{
    if (! e) // Fired when opening a thumb link
    {
        $("#image-overlay").remove();
        $("body").removeClass("image-overlay-open");
    }
    else if (e.target.classList.contains("wrapper") || e.target.id == "overlay-close-button")
    {
        $("#image-overlay").remove();
        $("body").removeClass("image-overlay-open");
        window.scroll(overlay_return_pos.x, overlay_return_pos.y);
    }
}


function overlay_image(e)
{
    e.preventDefault();
    overlay_close();

    let image = $(this).find("img");
    let w = image[0].naturalWidth;
    let h = image[0].naturalHeight;
    let image_src = image.attr("src");
    let image_alt = image.attr("alt");
    let image_title = image.attr("title");

    overlay_return_pos.x = document.querySelector("html").scrollLeft;
    overlay_return_pos.y = document.querySelector("html").scrollTop;

    let overlay = `
    <figure id="image-overlay">
        <div class="wrapper"><img src="${image_src}" alt="${image_alt}" style="aspect-ratio:${w}/${h}"></div>
        <figcaption>${image_title}</figcaption>
        <footer>
            <div><a href="${image_src}" target="_blank">Media Link</a></div>
            <div><button type="button" id="overlay-close-button">Close</button></div>
        </footer>
    </figure>
    `;
    $(".post-content").append(overlay);
    window.scroll(0, 0);
    $("body").addClass("image-overlay-open");
}
