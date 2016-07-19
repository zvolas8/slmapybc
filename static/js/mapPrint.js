
$(document).ready(function () {
    mapPath = $("#mapPath").html();
    
    var map = kartograph.map('#map');
    map.loadMap(mapPath, function () {
        $("#border").click(function () {
            map.addLayer('border');
            map.getLayer('border').style('stroke-width', '1.5');
        });

        $("#river").click(function () {
                map.addLayer('river');
                map.getLayer('river').style('stroke-width', '3');
                map.getLayer('river').style('stroke', 'blue');

                map.getLayer('river').on('mouseover', function (data, path, event) {
                    path.attr('stroke-width', '12');
                    $("#mapInfo").html(data.name);
                });

                map.getLayer('river').on('mouseout', function (data, path, event) {
                    path.attr('stroke-width', '3');
                    $("#mapInfo").html("");
                });
        });

        $("#mountains").click(function () {
            map.addLayer('mountains');
            map.getLayer('mountains').style('stroke-width', '3');
            map.getLayer('mountains').style('stroke', 'brown');

            map.getLayer('mountains').on('mouseover', function (data, path, event) {
                path.attr('stroke-width', '12');
                $("#mapInfo").html(data.name);
            });

            map.getLayer('mountains').on('mouseout', function (data, path, event) {
                path.attr('stroke-width', '3');
                $("#mapInfo").html("");
            });
        });

        $("#city").click(function () {
            map.addLayer('city');
            map.getLayer('city').style('stroke-width', '3');
            map.getLayer('city').style('stroke', 'brown');

            map.getLayer('city').on('mouseover', function (data, path, event) {
                path.attr('stroke-width', '12');
                $("#mapInfo").html(data.name);
            });

            map.getLayer('city').on('mouseout', function (data, path, event) {
                path.attr('stroke-width', '3');
                $("#mapInfo").html("");
            });
        });

        $("#delete").click(function () {
            map.clear()
            $(".svgLayersButton").removeClass('active');
        });    
    });
});
