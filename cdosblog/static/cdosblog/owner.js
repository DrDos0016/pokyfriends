$(document).ready(function (){
    $("#id_icon").change(refresh_icon);
    $("img[name=icon-image]").click(set_icon);
    $(".tag-shortcut").click(add_tag);
});

function refresh_icon()
{
    let pk = $(this).val();
    let idx = -1;
    for (idx in ICON_DATA)
    {
        if (ICON_DATA[idx].pk == pk )
        {
            break;
        }
    }
    $(`img[name=icon-image]`).removeClass("selected");
    $(`img[name=icon-image][data-pk=${idx}]`).addClass("selected");
}

function set_icon()
{
    let pk = $(this).data("pk");
    console.log("SET PK TO", pk);
    let value = $("#id_icon option")[pk].getAttribute("value");
    $("#id_icon").val(value);
    $(`img[name=icon-image]`).removeClass("selected");
    $(this).addClass("selected");
}

function add_tag()
{
    let tag = $(this).text();
    let current = $("input[name=tags_str]").val();
    $("input[name=tags_str]").val(current + tag + ", ");
}
