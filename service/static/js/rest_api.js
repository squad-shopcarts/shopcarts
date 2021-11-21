$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#sc_customer_id").val(res.customer_id);
        $("#sc_product_id").val(res.product_id);
        $("#sc_product_name").val(res.product_name);
        $("#product_quantity").val(res.quantity);
        $("#product_price").val(res.price);

        if (res.instock == 'true') {
            $("#instock").val("true");
        } else {
            $("#instock").val("false");
        }
        if (res.wishlist == 'true') {
            $("#sc_wishlist").val("true");
        } else {
            $("#sc_wishlist").val("false");
        }
    }

    function update_form_create(res) {
        $("#sc_customer_id").val(res.customer_id);
    }

    // Clears all form fields
    function clear_form_data() {
        $("#sc_customer_id").val("");
        $("#sc_product_id").val("");
        $("#sc_product_name").val("");
        $("#product_quantity").val("");
        $("#product_price").val("");
        $("#instock").val("");
        $("#sc_wishlist").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // Clear search results for shopcarts
    const clearShopcartResults = () => {
        $("#search_results").empty(); 
        $("#search_results").append('<table class="table-striped" cellpadding="10">');
        let header = '<tr>'; 
        header += '<th style="width:15%">Product ID</th>'; 
        header += '<th style="width:15%">Product Name</th>'; 
        header += '<th style="width:15%">Quantity</th>'; 
        header += '<th style="width:15%">Price</th>'; 
        header += '<th style="width:15%">Instock Status</th>'; 
        header += '<th style="width:15%">Wishlist Status</th>'; 
        $("#search_results").append(header);
    }
    
    // List the products in a shopcart
    const listShopcarts = (res) => {
        clearShopcartResults(); 
        let itemsString = ""; 
        res.product_list.map((product) => {itemsString+=`<tr><td>${product.product_id}: <th style="width:15%">${product.product_name}:</th> : <th style="width:15%">${product.quantity}:</th>: <th style="width:10%">${product.price}:</th> : <th style="width:15%">${product.instock}:</th> : <th style="width:15%">${product.wishlist}:</th> : ;</td><td>`})
        const row = "<tr><td>"+itemsString+"</td></tr>";
        $("#search_results").append(row); 
    }

    const listWishlist = (res) => {
        $("#wishlist_results").empty();
        $("#wishlist_results").append('<table class="table-striped" cellpadding="10">');
        var header = '<tr>'
        header += '<th style="width:10%">Product_ID</th>'
        header += '<th style="width:15%">Product_Name</th>'
        header += '<th style="width:15%">Quantity</th>'
        header += '<th style="width:15%">Price</th>'
        header += '<th style="width:15%">In_Stock</th>'
        header += '<th style="width:10%">Wishlist</th></tr>'
        header +=
        $("#wishlist_results").append(header);
        var firstProduct = "";
        for(var i = 0; i < res.length; i++) {
            var product = res[i];
            var row = "<tr><td>"+product.product_id+
                "</td><td>"+product.product_name+
                "</td><td>"+product.quantity+
                "</td><td>"+product.price+
                "</td><td>"+product.instock+
                "</td><td>"+product.wishlist+"</td></tr>";

            $("#wishlist_results").append(row);
                // if (i == 0) {
                //     firstPet = pet;
                // }
        }
        $("#wishlist_results").append('</table>');
    }

    // ****************************************
    // Create a Shopcart
    // ****************************************

    $("#create-btn").click(function () {

        var product_list = []

        var data = {
            "product_list": product_list,
        };

        var ajax = $.ajax({
            type: "POST",
            url: "/shopcarts",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function (res) {
            update_form_create(res);
            // flash_message("Success");
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message)
        });
    });

    // ****************************************
    // Delete a Shopcart
    // ****************************************

    $("#delete-shopcart-btn").click(function () {

        var customer_id = $("#sc_customer_id").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: "/shopcarts/" + customer_id,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Shopcart " + customer_id + " has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Update a Shopcart
    // ****************************************

    $("#update-btn").click(function () {
        var customer_id = $("#sc_customer_id").val();
        var product_id = $("#sc_product_id").val();
        var product_name = $("#sc_product_name").val();
        var quantity = $("#product_quantity").val();
        var price = $("#product_price").val();
        var instock = $("#instock").val();
        var wishlist = $("#sc_wishlist").val();
        var data = {
            "customer_id": customer_id,
            "product_id": product_id,
            "product_name": product_name,
            "quantity": quantity,
            "price": price,
            "instock": instock,
            "wishlist": wishlist
        };

        var url = "/shopcarts/" + customer_id + "/products/" + product_id;
        var ajax = $.ajax({
            type: "PUT",
            url: url,
            contentType: "application/json",
            data: JSON.stringify(data)
        })

        ajax.done(function (res) {
            update_form_data(res)
            flash_message("Success")
        });
    });

    // ****************************************
    // Retrieve a Shopcart
    // ****************************************

    $("#retrieve-btn").click(function () {

        var customer_id = $("#sc_customer_id").val();
        
        var ajax = $.ajax({
            type: "GET",
            url: "/shopcarts/" + customer_id,
            contentType: "application/json",
            data: ''
        });

        ajax.done(function (res) {
            console.log(res);
            //alert(res.toSource())
            listShopcarts(res)
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function (res) {
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a Product in a Shopcart
    // ****************************************

    $("#search-product-btn").click(function () {

        var customer_id = $("#sc_customer_id").val();
        var product_id = $("#sc_product_id").val();
        
        var ajax = $.ajax({
            type: "GET",
            url: "/shopcarts/" + customer_id + "/products/" + product_id,
            contentType: "application/json",
            data: ''
        });

        ajax.done(function (res) {
            update_form_data(res)
            flash_message("Successfully get product " + product_id + " in shopcart " + customer_id)
        });

        ajax.fail(function (res) {
            clear_form_data()
            flash_message("can not retrieve product " + product_id + " in shopcart " + customer_id)
        });

    });

    // ****************************************
    // Delete a Product in a Shopcart
    // ****************************************

    $("#delete-product-btn").click(function () {

        var customer_id = $("#sc_customer_id").val();
        var product_id = $("#sc_product_id").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: "/shopcarts/" + customer_id + "/products/" + product_id,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function (res) {
            clear_form_data()
            flash_message("Product " + product_id + " in shopcart " + customer_id + " has been Deleted!")
        });

        ajax.fail(function (res) {
            flash_message("Delete Failed!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#pet_id").val("");
        clear_form_data()
    });

    // ****************************************
    // Retrieve a Wishlisted Products in a Shpocart
    // ****************************************

    $("#retrieve-wishlist-btn").click(function () {

        var customer_id = $("#sc_customer_id").val();
        
        var ajax = $.ajax({
            type: "GET",
            url: `/shopcarts/wishlist?customer-id=${customer_id}`,
            contentType: "application/json",
            data: ''
        });

        ajax.done(function (res) {
            console.log(res);
            //alert(res.toSource())
            listWishlist(res)
            update_form_data(res)
            flash_message("Successfully Retrieved Wishlisted Items")
        });

        ajax.fail(function (res) {
            clear_form_data()
            flash_message(res.responseJSON.message)
        });
    });

    // ****************************************
    // Change the Wishlist Status of a Product
    // ****************************************

    $("#change-wishlist-btn").click(function () {

        var customer_id = $("#sc_customer_id").val();
        var product_id = $("#sc_product_id").val();

        console.group('hi')
        
        var ajax = $.ajax({
            type: "PUT",
            url: `/shopcarts/${customer_id}/products/${product_id}/reversewishlist`,
            contentType: "application/json",
            data: ''
        });

        ajax.done(function (res) {
            console.log(res);
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function (res) {
            clear_form_data()
            flash_message(res.responseJSON.message)
        });
    });

})
