$(function () {
    function render_time() {
        return $(this).data('timestamp')
    }
    $('[data-toggle="tooltip"]').tooltip(
        {title: render_time}
    );
});