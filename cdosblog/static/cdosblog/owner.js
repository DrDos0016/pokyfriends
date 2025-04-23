$(document).ready(function (){
    $("img[name=icon-image]").attr("src", "/static/cdosblog/icons/default.png");
    $("#id_icon").change(refresh_icon);
    console.log(ICON_DATA);
});

function refresh_icon()
{
    let pk = $(this).val();
    let url = "???";
    console.log("New icon idx", pk);
    for (let idx in ICON_DATA)
    {
        if (ICON_DATA[idx].pk == pk )
        {
            url = ICON_DATA[idx].url;
            break;
        }
    }
    $("img[name=icon-image]").attr("src", url);
}
