// get all arrow elements
const arrows = document.querySelectorAll(".arrow");

// new var for x and y
let offsetX, offsetY;

arrows.forEach(arrow => {

    // Event listener for when dragging starts
    arrow.addEventListener("dragstart", function(event) {
        offsetX = event.clientX - arrow.getBoundingClientRect().left;
        offsetY = event.clientY - arrow.getBoundingClientRect().top;

        event.dataTransfer.setData("text/plain", arrow.id);

    });

    // Event listener for when dragging ends
    arrow.addEventListener('dragend', function() {
        // reset
        offsetX = offsetY = 0;

    });
});

// prevents default behavior during dragover
document.addEventListener("dragover", function(event) {
    event.preventDefault();

});

// get id and move arrow to new coordinates
document.addEventListener("drop", function(event) {
    event.preventDefault();

    const id = event.dataTransfer.getData("text/plain");
    const arrow = document.getElementById(id);

    const newX = event.clientX - offsetX;
    const newY = event.clientY - offsetY;

    const imageContainer = document.getElementById("clickArea");
    const containerX = imageContainer.getBoundingClientRect().left;
    const containerY = imageContainer.getBoundingClientRect().top;

    arrow.style.left = newX - containerX + "px";
    arrow.style.top = newY - containerY + "px";

});

$(document).ready(function () {
    var setNumber = 1; // set number
    var allCoordinates = []; // store coordinates

    // Event listener for click on the image area
    $("#clickArea").click(function(event){
        var imgPos = $(this).offset();
        var x = event.pageX - imgPos.left; // x of click
        var y = event.pageY - imgPos.top; // y of click

        // Create a new div at the click location
        var clickMarker = $("<div class='clickMarker currentSet marker'></div>"); // we want clickMarker, currentSet, and marker for general, clearing, and showing all purposes respectively

        clickMarker.css({
            left: x,
            top: y

        });

        $(this).parent().append(clickMarker);
        console.log("Set Number: " + setNumber);

        $.ajax({
            url: "/click",
            type: "POST",
            data: {
                x: x,
                y: y

            },

            success: function () {
                console.log("Click event sent to server");

            }

        });

        allCoordinates.push({x: x, y: y}); // Store coordinates

    });

    // Add click event listener to the Clear Markers button
    $("#clearMarkers").click(function () {
        $(".currentSet").remove();

        // clear coordinates array
        allCoordinates = [];

    });

    // Add click event listener to the End Set button
    $("#endSet").click(function () {
        if ($(".currentSet").length > 0) {

            // change the class of the markers from "currentSet" to "previousSets"
            $(".currentSet").removeClass("currentSet").addClass("previousSets").hide();

            // send coordinates to server to save them
            $.ajax({
                url: "/saveCoordinates",
                type: "POST",
                data: {
                    coordinates: allCoordinates,
                    setNumber: setNumber,

                },

                success: function () {
                    console.log("Coordinates sent to server");

                }

            });

            // clear coordinates array
            allCoordinates = [];

            // increment set number
                setNumber++;

        }

    });

    // show all button shows all markers (with marker div)
    $("#showAll").click(function () {
        $(".marker").show();

    });

    // hide all button hides all markers (with marker div)
    $("#hideAll").click(function () {
        $(".marker").hide();

    });

    // downloads plot on client side
    $("#downloadPlot").click(function () {

        // call server to download plot
        window.open("/generate_marker_plot", "_blank");

    });

    // downloads plot on client side
    $("#downloadMA").click(function () {

        // call server to download plot
        window.open("/generate_ma_plot", "_blank");

    });

});
