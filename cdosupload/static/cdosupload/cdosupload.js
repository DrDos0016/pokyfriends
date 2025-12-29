export class Uploader {
    constructor(selector, input_id)
    {
        console.log("Construct", selector, input_id);
        this.selector = selector;
        this.upload_area = $(selector);
        this.input_id = input_id;
        this.dragging_css_class = "dragging";
        $(this.selector).click((f) => this.upload_from_widget() );
        $(selector).on("dragover", (e) => this.universal(e, this.dragging_css_class) );
        $(selector).on("dragleave", (e) => this.universal(e, this.dragging_css_class) );
        $(selector).on("drop", (e) => this.upload_from_drop(e));
    }

    universal(e, css_class)
    {
        // Stop event propagation, add/remove CSS class to indicate state
        console.log("Universal", css_class, e);
        e.preventDefault();
        e.stopPropagation();
        if (e.type == "dragover")
            this.upload_area.addClass(css_class);
        else
            this.upload_area.removeClass(css_class);
    }

    upload_from_widget()
    {
        console.log("Click for basic upload", this.selector, this.input_id);
        $(this.input_id).click();
    }

    upload_from_drop(e)
    {
        this.universal(e, this.dragging_css_class);
        const dt = e.originalEvent.dataTransfer;
        const file = dt.files[0];
        $(this.input_id)[0].files = dt.files;
        this.process_file(file)
    }

    process_file(file)
    {
        console.log("Default process_file function! Please override me!");
    }
}

export function filesize_format(bytes)
{
    if (bytes == 0)
        return "0 B";
    var i = Math.floor(Math.log(bytes) / Math.log(1024));
    return (bytes / Math.pow(1024, i)).toFixed(1) * 1 + ' ' + ['B', 'KB', 'MB', 'GB', 'TB'][i];
}
