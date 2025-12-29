
class Uploader {
    constructor(selector)
    {
        this.selector = upload_area_selector;
        this.upload_area = $(upload_area_selector);
        $(this.selector).click(this.basic_upload)
    }

    function basic_upload()
    {
        console.log("Click for basic upload");
    }
}

/*
// Drag and Drop Uploading
    $(".upload-area").click(function (){
        var target = $(this).data("file-widget");
        $("#" + target).click();
    });

    $(".upload-area").on("dragover", function(e) {
        e.preventDefault();
        e.stopPropagation();
        $(this).addClass("dragging");
    });

    $(".upload-area").on("dragleave", function(e) {
        e.preventDefault();
        e.stopPropagation();
        $(this).removeClass("dragging");
    });

    $(".upload-area").on("drop", function(e) {
        e.preventDefault();
        e.stopPropagation();
        $(this).removeClass("dragging");

        const dt = e.originalEvent.dataTransfer;
        const file = dt.files[0];
        var ext = file.name.toLowerCase().slice(-4);
        var target = $(this).data("file-widget");
        $("#" + target)[0].files = dt.files;

        if (ext == ".zip")
            parse_zip_file(file);
        else if (ext == ".zzt")
            set_uploaded_zzt_file(file);
        else if (ext == ".png" || ext == ".jpg")
            set_uploaded_image(file);
        else
            console.log("Unhandled file extension: " + ext);
    });

    $(".drag-and-drop-file-widget").change(function (e){
        const image_extensions = [".png", ".jpg", ".gif"]
        const file = $(this)[0].files[0];
        var ext = file.name.toLowerCase().slice(-4);
        if (ext == ".zip")
            parse_zip_file(file);
        else if (ext == ".zzt")
            set_uploaded_zzt_file(file);
        else if (image_extensions.indexOf(ext) != -1)
            set_uploaded_image(file);
        else
            console.log("Unhandled file extension: " + ext);
    });
*/
