$(document).ready(function () {
    //create config
    var container = document.getElementById("jsoneditor");

    if (container != undefined) {
        var options = {
            mode: 'tree',
            modes: ['form', 'text', 'tree', 'view'], // allowed modes
            onError: function (err) {
                alert(err.toString());
            },
            onModeChange: function (newMode, oldMode) {
                console.log('Mode switched from', oldMode, 'to', newMode);
            }
        };
        var editor = new JSONEditor(container, options);
    }

    // get json on submit
    $('#configForm').submit(function () {
        var json = editor.get();
        $('#myConfig').val(JSON.stringify(json, null, 2));
    });

    //view config
    var container2 = document.getElementById("jsonviewer");
    if (container2 != undefined) {
        var options2 = {
            mode: 'text',
            onError: function (err) {
                alert(err.toString());
            },
        };
        editor2 = new JSONEditor(container2, options2);      
    }

    $('.configRow').click(function () {
        var id = $(this).data('id');
        var json = JSON.parse($('#' + id).val());
        editor2.set(json);
    });

    $('#shpConfig').change(function () {
        config = $(this).find(':selected').attr('data-config');
        json = JSON.parse(config);
        editor2.set(json);
    });

    var container3 = document.getElementById("jsonedit");
    if (container3 != undefined) {
        var options3 = {
            mode: 'text',
            modes: ['form', 'text', 'tree', 'view'], // allowed modes
            onError: function (err) {
                alert(err.toString());
            },
        };
        editor3 = new JSONEditor(container3, options3);

        var json = JSON.parse($('#myConfig').val());
        editor3.set(json);
    }

    $('#configFormEdit').submit(function () {
        var json = editor3.get();
        $('#myConfig').val(JSON.stringify(json, null, 2));
    });
});
