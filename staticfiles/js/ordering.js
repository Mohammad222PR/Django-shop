$(document).ready(function () {
    let current_url_params = new URLSearchParams(window.location.search)
    $("#page-size-filter").val(current_url_params.get("page_size") || "")
    $("#order-by-filter").val(current_url_params.get("order_by") || "")
    $("#search-query-filter").val(current_url_params.get("q") || "")
    $("#min-price-filter").val(current_url_params.get("min_price") || "")
    $("#max-price-filter").val(current_url_params.get("max_price") || "")
    $("#category-id-filter").val(current_url_params.get("category_id") || "")

});

$('#page-size-filter').change(function () {
    let current_url_params = new URLSearchParams(window.location.search)
    var selectedOption = $(this).val();
    current_url_params.set("page_size", selectedOption)
    let new_url = window.location.pathname + "?" + current_url_params.toString()
    window.location.href = new_url
});
$('#order-by-filter').change(function () {
    let current_url_params = new URLSearchParams(window.location.search)
    var selectedOption = $(this).val();
    current_url_params.set("order_by", selectedOption)
    let new_url = window.location.pathname + "?" + current_url_params.toString()
    window.location.href = new_url
});

