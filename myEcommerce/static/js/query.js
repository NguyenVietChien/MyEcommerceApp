
$(document).ready(function () {
    // Button Click
    $("#filter").click(function (e) {
        e.preventDefault();
        var fromPrice = $("#fromPrice").val()
        var toPrice = $("#toPrice").val()

        $.ajax({
            type: 'POST',
            url: "/api/filter/",
            data: {
                'fromPrice': fromPrice,
                'toPrice': toPrice,
            },
            success: function (response) {

                var html = "";
                for (let i = 0; i < response.length; i++)
                    html += `<tr>
                        <td>${response[i].fields["product_link"] || ""}</td>
                        <td>${response[i].fields["product_price"] || ""}</td>
                        <td>${response[i].fields["total_comments"] || "0"}</td>
                        <td>${response[i].fields["rating_point"] || "0"}</td>
                        <td>${response[i].fields["rating_5_star"] || "0"}</td>
                        <td>${response[i].fields["platform"] || ""}</td>
                        </tr>`;

                $('#product_table').html(html)
                $('#dataTable').DataTable();
            },
            error: function (response) {
                // alert the error if any error occured
                alert(response["responseJSON"]["error"]);
            }
        })
    });
});
