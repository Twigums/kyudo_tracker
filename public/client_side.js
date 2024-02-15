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

function reset_pos() {
    let arrows = ["arrow1", "arrow2", "arrow3", "arrow4"];

    for (let i = 0; i < arrows.length; i++) {
        document.getElementById(arrows[i]).style.top = "50px";
        document.getElementById(arrows[i]).style.left = 50 * (i + 1) + "px";

    }

}

$(document).ready(function () {
    let setNumber = 1;

    // Add click event listener to the Clear Markers button
    $("#clearMarkers").click(function () {
        $(".currentSet").remove();
        reset_pos();

    });

    // Add click event listener to the End Set button
    $("#endSet").click(function () {
        let coords = [];

        ["arrow1", "arrow2", "arrow3", "arrow4"].forEach(i => {
            const arrow = document.getElementById(i);
            const arrow_rect = arrow.getBoundingClientRect();
            const x = arrow_rect.left + arrow_rect.width / 2;
            const y = arrow_rect.top + arrow_rect.height / 2;

            coords.push({x, y, i});

        });

        $.ajax({
            url: "/saveCoordinates",
            type: "POST",
            data: {
                coordinates: coords,
                setNumber: setNumber,

            },

            success: function () {
                console.log("Coordinates sent to server.");

            }

        });

        reset_pos();

        setNumber++;

    });

    // show all button shows all markers (with marker div)
    $("#showAll").click(function () {
        $(".arrow").show();

    });

    // hide all button hides all markers (with marker div)
    $("#hideAll").click(function () {
        $(".arrow").hide();

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
