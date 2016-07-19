var count = 1;

$(document).ready(function () {

    var config = $("#configArea").val();
    if (config != undefined) {
        myJSON = JSON.parse(config);
        output(syntaxHighlight(JSON.stringify(myJSON, undefined, 4)));
    }

    var atId = $("#id_layerName");
    atId.change( function () {
        var selectValue = $(this).find('option:selected').attr("name");
        myJSON['layers'][0]['id'] = selectValue;
        var str = JSON.stringify(myJSON, undefined, 4);
        output(syntaxHighlight(str));
    });

    var charsetRadio = $('input[name="charset"]');
    charsetRadio.change(function () {
        var value = this.value;
        myJSON['layers'][0]['charset'] = value;
        var str = JSON.stringify(myJSON, undefined, 4);
        output(syntaxHighlight(str));
    })

    var atId = $("#attributesId");
    atId.bind("change keypress", function () {
        var tempId = $(this).val();
        myJSON['layers'][0]['attributes']['id'] = tempId;
        var str = JSON.stringify(myJSON, undefined, 4);
        output(syntaxHighlight(str));
    });

    var atCode = $("#attributesCode");
    atCode.bind("change keypress", function () {
        var tempCode = $(this).val();
        myJSON['layers'][0]['attributes']['code'] = tempCode;
        var str = JSON.stringify(myJSON, undefined, 4);
        output(syntaxHighlight(str));
    });

    var atName = $("#attributesName");
    atName.bind("change keypress", function () {
        var tempName = $(this).val();
        myJSON['layers'][0]['attributes']['name'] = tempName;
        var str = JSON.stringify(myJSON, undefined, 4);
        output(syntaxHighlight(str));
    });

    var nextAtt = $("#nextAttribute");
    nextAtt.click(function () {
        var div = document.createElement('div');
        div.className = 'form-group';
        div.innerHTML = '<div class="col-sm-4">\
                             <input type="text" class="form-control attributesLabel marginBottom5" name="attributesLabel' + count + '" id="attributesLabel' + count + '" placeholder="">\
                         </div>\
                         <div class="col-sm-8">\
                             <input type="text" class="form-control attributesValue marginBottom5" name="attributesValue' + count + '" id="attributesValue' + count + '" placeholder="" disabled="true">\
                         </div>';

        $("#attributesPanel").append(div);
        count++;
    });

    var nextFil = $("#nextFilter");
    nextFil.click(function () {
        var div = document.createElement('div');
        div.className = 'form-group';
        div.innerHTML = '<div class="col-sm-4">\
                             <input type="text" class="form-control filterLabel marginBottom5" name="filterLabel' + count + '" id="filterLabel' + count + '" placeholder="">\
                         </div>\
                         <div class="col-sm-8">\
                             <input type="text" class="form-control filterValue marginBottom5" name="filterValue' + count + '" id="filterValue' + count + '" placeholder="" disabled="true">\
                         </div>';

        $("#filterPanel").append(div);
        count++;
    });


    $("#shapefileForm").submit(function () {
        myJSON['layers'][0]['src'] = "";
        var str = JSON.stringify(myJSON, undefined, 4);
        $("#configArea").val(str);
        return true;
    })
    
});

var labelMap = new Map();
var filterMap = new Map();

$(document).bind('DOMSubtreeModified', function () {  

    $('.attributesLabel').change(function () {
        if (labelMap.get(this.id) == null) {
            myJSON['layers'][0]['attributes'][this.value] = "";
            var str = JSON.stringify(myJSON, undefined, 4);
            output(syntaxHighlight(str));
            labelMap.set(this.id, this.value);
            $(getIdValueForLable(this.id)).prop('disabled', false);
        } else {
            var tempValue = getValueForLabel(this.id);
            var tempLabel = labelMap.get(this.id);
            delete myJSON['layers'][0]['attributes'][tempLabel];
            myJSON['layers'][0]['attributes'][this.value] = tempValue;
            var str = JSON.stringify(myJSON, undefined, 4);
            output(syntaxHighlight(str));
            labelMap.set(this.id, this.value);
        }
    });

    $('.attributesValue').change(function () {
        var id = this.id.replace(/[^\d.]/g, '');
        var key = labelMap.get('attributesLabel' + id);
        myJSON['layers'][0]['attributes'][key] = this.value;
        var str = JSON.stringify(myJSON, undefined, 4);
        output(syntaxHighlight(str));
    });

    $("#createFilter").click(function () {
        $("#filterArea").removeClass('hidden'); 
        myJSON['layers'][0]['filter'] = {};
        var str = JSON.stringify(myJSON, undefined, 4);
        output(syntaxHighlight(str));
    });

    $('.filterLabel').change(function () {
        if (filterMap.get(this.id) == null) {
            myJSON['layers'][0]['filter'][this.value] = "";
            var str = JSON.stringify(myJSON, undefined, 4);
            output(syntaxHighlight(str));
            filterMap.set(this.id, this.value);
            $(getIdValueForFilter(this.id)).prop('disabled', false);
        } else {
            var tempValue = getValueForFilter(this.id);
            var tempLabel = filterMap.get(this.id);
            delete myJSON['layers'][0]['filter'][tempLabel];
            myJSON['layers'][0]['filter'][this.value] = tempValue;
            var str = JSON.stringify(myJSON, undefined, 4);
            output(syntaxHighlight(str));
            filterMap.set(this.id, this.value);
        }
    });

    $('.filterValue').change(function () {
        var id = this.id.replace(/[^\d.]/g, '');
        var key = filterMap.get('filterLabel' + id);
        myJSON['layers'][0]['filter'][key] = this.value;
        var str = JSON.stringify(myJSON, undefined, 4);
        output(syntaxHighlight(str));
    });
});

function getIdValueForLable(label) {
    var id = label.replace(/[^\d.]/g, '');
    var idValue = "#attributesValue" + id;
    return idValue;
}

function getValueForLabel(label) {
    var idValue = getIdValueForLable(label);
    var value = $(idValue).val();
    return value;
}

function getIdValueForFilter(filter) {
    var id = filter.replace(/[^\d.]/g, '');
    var idValue = "#filterValue" + id;
    return idValue;
}

function getValueForFilter(filter) {
    var idValue = getIdValueForFilter(filter);
    var value = $(idValue).val();
    return value;
}

function output(inp) {
    $("#configView").html(inp);
}

function syntaxHighlight(json) {
    json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
        var cls = 'number';
        if (/^"/.test(match)) {
            if (/:$/.test(match)) {
                cls = 'key';
            } else {
                cls = 'string';
            }
        } else if (/true|false/.test(match)) {
            cls = 'boolean';
        } else if (/null/.test(match)) {
            cls = 'null';
        }
        return '<span class="' + cls + '">' + match + '</span>';
    });
}


