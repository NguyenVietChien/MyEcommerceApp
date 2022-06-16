
$(document).ready(function () {
    // Button Click
    $("#crawl").click(function (e) {
        e.preventDefault();

        var keyword = $("#search-product").val()

        var tikiUrl = "https://tiki.vn/search?q=" + keyword.replace(/\s/g, '+')
        var shopeeUrl = "https://shopee.vn/search?keyword=" + keyword.replace(/\s/g, '%20')
        var lazadaUrl = "https://www.lazada.vn/catalog/?q=" + keyword.replace(/\s/g, '+') + "&_keyori=ss&from=input&spm=a2o4n.home.search.go.27f86afeOMumZF"

        $.ajax({
            type: 'POST',
            url: "/api/crawl/",
            data: {
                'tikiUrl': tikiUrl,
                'shopeeUrl': shopeeUrl,
                'lazadaUrl': lazadaUrl
            },
            success: function (response) {
                // Something
            },
            error: function (response) {
                // alert the error if any error occured
                alert(response["responseJSON"]["error"]);
            }
        })
    });
});
