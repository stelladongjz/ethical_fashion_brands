$(document).ready(function() {
    

    $("form").on("submit", function (e) {
        let input = $("#search-input");
        input.val(input.val().trim());  

        if (input.val() === " ") {
            e.preventDefault();  
            input.val('');  
            input.focus();  
        }
    });



    $("#add-form").on("submit", function(e) {
        e.preventDefault(); // Prevent default form submission

        $.ajax({
            url: "/add",
            method: "POST",
            data: $(this).serialize(),
            success: function(response) {
                if (response.success) {
                    // Show success message with a link to the new item
                    $("#message").html(
                        `New item successfully created. <a href="${response.redirect_url}">See it here</a>.`
                    ).show();

                    // Clear the form
                    $("#add-form")[0].reset();

                    // Focus on the first input field
                    $("#title").focus();
                } else {
                    // Display validation errors
                    $(".error-message").text(""); // Clear previous errors
                    for (const field in response.errors) {
                        $(`#${field}-error`).text(response.errors[field]);
                    }
                }
            },
            error: function(xhr, status, error) {
                alert("Error: " + error);
            }
        });
    });

    document.addEventListener('DOMContentLoaded', function () {
        const searchForm = document.getElementById('search-form');
        const searchInput = document.getElementById('search-input');
    
        searchForm.addEventListener('submit', function (event) {
            let query = searchInput.value.trim(); // Trim whitespace
    
            if (query === '') {
                event.preventDefault(); // Prevent form submission
                searchInput.value = ''; // Clear out whitespace
                searchInput.focus(); // Keep focus on input
            }
        });
    });
    

    // Function to display validation errors
    function showErrors(errors) {
        // Reset all error messages
        $('.error-message').text('');
        
        // Display error messages
        for (const field in errors) {
            $(#${field}-error).text(errors[field]);
        }
    }

    $('#edit-form').on('submit', function(e) {
        e.preventDefault();
        const itemId = $(this).data('id');
        $.post(/edit/${itemId}, $(this).serialize(), function(response) {
            if (response.success) {
                window.location.href = response.redirect;
            } else {
                showErrors(response.errors);
            }
        });
    });

    $("#discard-btn").on("click", function() {
        const itemId = $(this).data('id');
        if (confirm("Are you sure you want to discard the changes?")) {
            window.location.href = "/view/" + itemId;
        }
    });
});
