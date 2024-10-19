$(document).ready(function (){
    $("img[name=icon-image]").attr("src", "/static/cdosblog/icons/default.png");
    $("#id_icon").change(refresh_icon);
});

function refresh_icon()
{
    let pk = $(this).val();
    let url = ICON_DATA[pk].url;
    $("img[name=icon-image]").attr("src", url);
}
