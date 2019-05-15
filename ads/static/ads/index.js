$(document).ready(function () {
    $('#facebookForm').submit(submitFacebookForm);
    $('#vkForm').submit(submitVkForm);

    function submitVkForm(event) {
        event.preventDefault();
        return sendData(this);
    }

    function submitFacebookForm(event) {
        event.preventDefault();
        var isLoaded = $(this).attr('configurationLoaded');
        if (isLoaded)
            return sendData(this);
        else
            return getConfiguration(this)
    }
    
    function getConfiguration(form) {
        $.get(form.action, function (data) {
                $(form).attr('configurationLoaded', 'True');
                $(form).find('.configuration').show();
                var select = $(form).find('#page');
                $.each(data.pages, function (i, item) {
                    select.append(new Option(item.name, item.id, false, false))
                });
            }).fail(function (data) {
                console.log(data)
            })
    }

    function sendData(form) {
        var btn = $(form).find('button');
        btn.addClass('no-active');
        btn.prop('disabled', true);
        $.ajax({
            url: form.action,
            method: 'POST',
            data: new FormData(form),
            contentType: false,
            processData: false,
            success: function (data) {
                document.location.reload()
            },
            error: function (response) {
                $(form).find('.errors').html(response.responseText)
            }
        })
    }
});