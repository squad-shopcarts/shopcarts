$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#customer_id").val(res.customer_id);
        $("#product_id").val(res.product_id);
        $("#product_name").val(res.product_name);
        $("#product_quantity").val(res.quantity);
        $("#product_price").val(res.price);

        if (res.instock == true) {
            $("#instock").val("true");
        } else {
            $("#instock").val("false");
        }
        if (res.wishlist == true) {
            $("#wishlist").val("true");
        } else {
            $("#wishlist").val("false");
        }
    }

    function update_form_create(res) {
        $("#customer_id").val(res.customer_id);
    }

    // Clears all form fields
    function clear_form_data() {
        $("#customer_id").val("");
        $("#product_id").val("");
        $("#product_name").val("");
        $("#product_quantity").val("");
        $("#product_price").val("");
        $("#instock").val("");
        $("#wishlist").val("");
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

    // ****************************************
    // Create a Pet
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
            flash_message(res);
            // flash_message("Success");
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a Shopcart
    // ****************************************

    $("#update-btn").click(function () {

        var pet_id = $("#pet_id").val();
        var name = $("#pet_name").val();
        var category = $("#pet_category").val();
        var available = $("#pet_available").val() == "true";

        var data = {
            "name": name,
            "category": category,
            "available": available
        };

        var ajax = $.ajax({
            type: "PUT",
            url: "/pets/" + pet_id,
            contentType: "application/json",
            data: JSON.stringify(data)
        })

        ajax.done(function (res) {
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message)
        });
    });

    // ****************************************
    // Retrieve a Shopcart
    // ****************************************

    $("#retrieve-btn").click(function () {

        var customer_id = $("#customer_id").val();
        
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
            update_form_create(res)
            flash_message("Success")
        });

        ajax.fail(function (res) {
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    

    // ****************************************
    // Delete a Pet
    // ****************************************

    $("#delete-btn").click(function () {

        var pet_id = $("#pet_id").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: "/shopcarts/" + pet_id,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function (res) {
            clear_form_data()
            flash_message("Pet has been Deleted!")
        });

        ajax.fail(function (res) {
            flash_message("Server error!")
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
    // Search for a Pet
    // ****************************************

    $("#search-btn").click(function () {

        var name = $("#pet_name").val();
        var category = $("#pet_category").val();
        var available = $("#pet_available").val() == "true";

        var queryString = ""

        if (name) {
            queryString += 'name=' + name
        }
        if (category) {
            if (queryString.length > 0) {
                queryString += '&category=' + category
            } else {
                queryString += 'category=' + category
            }
        }
        if (available) {
            if (queryString.length > 0) {
                queryString += '&available=' + available
            } else {
                queryString += 'available=' + available
            }
        }

        var ajax = $.ajax({
            type: "GET",
            url: "/shopcarts?" + queryString,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function (res) {
            //alert(res.toSource())
            $("#search_results").empty();
            $("#search_results").append('<table class="table-striped" cellpadding="10">');
            var header = '<tr>'
            header += '<th style="width:10%">ID</th>'
            header += '<th style="width:40%">Name</th>'
            header += '<th style="width:40%">Category</th>'
            header += '<th style="width:10%">Available</th></tr>'
            $("#search_results").append(header);
            var firstPet = "";
            for (var i = 0; i < res.length; i++) {
                var pet = res[i];
                var row = "<tr><td>" + pet._id + "</td><td>" + pet.name + "</td><td>" + pet.category + "</td><td>" + pet.available + "</td></tr>";
                $("#search_results").append(row);
                if (i == 0) {
                    firstPet = pet;
                }
            }

            $("#search_results").append('</table>');

            // copy the first result to the form
            if (firstPet != "") {
                update_form_data(firstPet)
            }

            flash_message("Success")
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message)
        });

    });

})
