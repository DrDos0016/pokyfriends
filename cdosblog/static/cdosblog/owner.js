$(document).ready(function (){
    $("#id_icon").change(refresh_icon);
    $("img[name=icon-image]").click(set_icon);
    $(".tag-shortcut").click(add_tag);

    $("select[name=privacy]").change(function (){
        if ($(this).val() == 3)
            show_field("#id_password");
        else
            hide_field("#id_password");
    });
    $("select[name=schema]").change(function (){
        if ($(this).val() == 2) // Markdown
            hide_field("#id_css");
        else
            show_field("#id_css");
        if ($(this).val() == 3) // Django
            show_field("#id_django_add_ons");
        else
            hide_field("#id_django_add_ons");
    });

    $("select[name=privacy]").change();
    $("select[name=schema]").change();
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

function hide_field(selector)
{
    // Selector = Selector of the <input>
    $(selector).parent().hide();
}

function show_field(selector)
{
    $(selector).parent().show();
}
