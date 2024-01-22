const express = require("express");
const path = require("path");
const fs = require("fs");
const bodyParser = require("body-parser");

const app = express();
const port = 3000;

// Get the current date and time
const date = new Date();
const dateString = `${date.getFullYear()}-${date.getMonth()+1}-${date.getDate()}_${date.getHours()}-${date.getMinutes()}-${date.getSeconds()}`;

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Serve static files from the "public" directory
app.use(express.static(path.join(__dirname, "public")));

app.get("/", function(req, res) {
  res.sendFile(path.join(__dirname, "public", "index.html"));

});

// log click events
app.post("/click", (req, res) => {
  console.log(`Click at coordinates (${req.body.x}, ${req.body.y})`);
  res.sendStatus(200);

});

// save coordinates from click events
app.post("/saveCoordinates", (req, res) => {
  const coordinates = req.body.coordinates;
  const setNumber = req.body.setNumber;

  // Convert the coordinates array to a CSV string
  // data will be saved in the format of "set number, x, y"
  const data = coordinates.map(coordinate => `${setNumber}, ${coordinate.x}, ${coordinate.y}\n`).join("");

  // Use the date and time as the filename
  const filename = `coordinates_${dateString}.txt`;

  // Write the data to a file
  fs.appendFile(filename, data, (err) => {
    if (err) {
      console.log(err);
      res.sendStatus(500);

    } else {
      console.log(`Saved coordinates for set number ${setNumber}`);
      res.sendStatus(200);

    }

  });

});
app.listen(port, () => {
  console.log(`Website is running at http://localhost:${port}`);

});
