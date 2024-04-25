

$(document).ready(function () {
    console.log("scripts.js working");
    $(".owl-carousel").owlCarousel({
        loop: false,
        margin: 15,
        nav: false,
        autoplay: true,
        autoplayTimeout: 3000, // Set autoplay speed in milliseconds (e.g., 3000ms = 3 seconds)
        dots: false,
        responsive: {
            0: {
                items: 1, // Display 1 item on screens smaller than 600px
            },
            576: {
                items: 2, // Display 2 items on screens between 576px and 767px
            },
            768: {
                items: 3, // Display 3 items on screens between 768px and 991px
            },
            992: {
                items: 4, // Display 4 items on screens between 992px and 1199px
            },
            1200: {
                items: 6, // Display 6 items on screens larger than or equal to 1200px
            },
        },
    });
    // Attach click event handler to logout link
    $('.logout').click(function (event) {
        // Prevent the default action of the link
        event.preventDefault();

        // Show an alert to confirm logout
        if (confirm('Are you sure you want to logout?')) {
            // If the user confirms, redirect to the logout URL
            window.location.href = $(this).attr('href');
        } else {
            // If the user cancels, do nothing
            return false;
        }
    });




    // Timer for alerts
    setTimeout(function () {
        $(".alert").alert("close");
    }, 5000);

    // add to cart
    $(".add-to-cart-btn").click(function (e) {

        let addButton = $(this);
        console.log("add-to-cart-btn clicked");

        let id = addButton.attr('data-index');
        console.log("add-to-cart-btn : id :", id);

        let quantity = $("#no_of_quantity_" + id).val()
        console.log("quantity :", quantity);

        $.ajax({
            dataType: 'json',
            type: 'GET',
            url: '/add-to-cart',

            data: {
                "id": id,
                "quantity": quantity,

            },

            beforeSend: function () {
                console.log('trying to send data');
            },

            success: function (res) {
                console.log('data send');
                addButton.html("Added To Cart");
                console.log(res);
                no_of_items = res.no_of_cart_items;
                $(".cart-count").text(no_of_items);
            },

            error: function (response) {
                console.log(response)
            }
        });

    });


    // // delete from Cart
    // function handleDeleteProduct() {
    //     console.log('delete-product clicked');
    //     let delButton = $(this);
    //     let id = delButton.attr('data-id');
    //     console.log(id);

    //     $.ajax({
    //         dataType: 'json',
    //         type: 'GET',
    //         url: '/del-product-from-cart',
    //         data: {
    //             'id': id
    //         },
    //         beforeSend: function () {
    //             console.log('trying to delete from cart');
    //         },
    //         success: function (res) {
    //             console.log('deleted from cart');
    //             console.log(res);
    //             $("#cart_async").html(res.context);

    //             // Reattach the event handler after content update
    //             $('.delete-product').off('click').on('click', handleDeleteProduct);
    //         },
    //         error: function (err) {
    //             console.log('error in delete from cart');
    //             console.log(err);
    //         }
    //     });
    // }
    // // Attach initial event handler for delete product
    // $('.delete-product').click(handleDeleteProduct);
    // // end delete from Cart


    // // update from Cart
    // function handleUpdateProduct() {
    //     console.log('update-product clicked');
    //     let updateButton = $(this);
    //     let id = updateButton.attr('data-id');
    //     console.log('id:', id);
    //     // console.log(typeof (id));

    //     let quantity = $("#no_of_quantity_" + id).val();
    //     console.log('qty: ', quantity);

    //     if (quantity <= 0) {
    //         alert('Quantity must be equal to or greater than one!')
    //     } else {
    //         $.ajax({
    //             dataType: 'json',
    //             type: 'GET',
    //             url: '/update-from-cart',
    //             data: {
    //                 'id': id,
    //                 'quantity': quantity
    //             },
    //             beforeSend: function () {
    //                 console.log('trying to update from cart');
    //             },
    //             success: function (res) {
    //                 console.log('updated from cart');
    //                 console.log(res);
    //                 $("#cart_async").html(res.context);

    //                 // Reattach the event handler after content update
    //                 $('.update-product').off('click').on('click', handleUpdateProduct);
    //             },
    //             error: function (err) {
    //                 console.log('error in update from cart');
    //                 console.log(err);
    //             }
    //         });
    //     }


    // }
    // // Attach initial event handler for delete product
    // $('.update-product').click(handleUpdateProduct);
    // // end delete from Cart



    // ##################################################################
    // ##################################################################
    // ##################################################################
    // delete from Cart
    function handleDeleteProduct() {
        console.log('delete-product clicked');
        let delButton = $(this);
        let id = delButton.attr('data-id');
        console.log(id);

        $.ajax({
            dataType: 'json',
            type: 'GET',
            url: '/del-product-from-cart',
            data: {
                'id': id
            },
            beforeSend: function () {
                console.log('trying to delete from cart');
            },
            success: function (res) {
                console.log('deleted from cart');
                console.log(res);
                $("#cart_async").html(res.context);
            },
            error: function (err) {
                console.log('error in delete from cart');
                console.log(err);
            }
        });
    }

    // Attach event handler for delete product using event delegation
    $(document).on('click', '.delete-product', handleDeleteProduct);

    // update from Cart
    function handleUpdateProduct() {
        console.log('update-product clicked');
        let updateButton = $(this);
        let id = updateButton.attr('data-id');
        console.log('id:', id);
        // console.log(typeof (id));

        let quantity = parseInt($("#no_of_quantity_" + id).val()); // Parse input value to integer
        console.log('qty: ', quantity);

        if (quantity <= 0) {
            alert('Quantity must be equal to or greater than one!');
            // Reset value to default
            let defaultQuantity = parseInt($("#no_of_quantity_" + id).attr('value'));
            $("#no_of_quantity_" + id).val(defaultQuantity);
        } else {
            $.ajax({
                dataType: 'json',
                type: 'GET',
                url: '/update-from-cart',
                data: {
                    'id': id,
                    'quantity': quantity
                },
                beforeSend: function () {
                    console.log('trying to update from cart');
                },
                success: function (res) {
                    console.log('updated from cart');
                    console.log(res);
                    $("#cart_async").html(res.context);
                },
                error: function (err) {
                    console.log('error in update from cart');
                    console.log(err);
                }
            });
        }
    }

    // Attach event handler for update product using event delegation
    $(document).on('click', '.update-product', handleUpdateProduct);





});

