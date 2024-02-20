const express = require("express");
const path = require("path");
const fs = require("fs");
const bodyParser = require("body-parser");
const { exec } = require("child_process")

const app = express();
const port = 3000;

// Get the current date and time
const date = new Date();
const dateString = `${date.getFullYear()}-${date.getMonth()+1}-${date.getDate()}_${date.getHours()}-${date.getMinutes()}-${date.getSeconds()}`;
const filename = `coordinates_${dateString}`;

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Serve static files from "public"
app.use(express.static(path.join(__dirname, "public")));

app.get("/", function(req, res) {
  res.sendFile(path.join(__dirname, "public", "index.html"));

});

app.get("/client.js", function(req, res) {
  res.sendFile(path.join(__dirname, "public", "client_side.js"));

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
  const data = coordinates.map(coordinate => `${setNumber}, ${coordinate.x}, ${coordinate.y}, ${coordinate.i}\n`).join("");

  // Use the date and time as the filename
  const txt_filepath = path.join(__dirname, "data", "txt", `${filename}.txt`);

  // Write the data to a file
  fs.appendFile(txt_filepath, data, (err) => {
    if (err) {
      console.log(err);
      res.sendStatus(500);

    } else {
      console.log(`Saved coordinates for set number ${setNumber}`);
      res.sendStatus(200);

    }

  });

});

app.get("/generate_marker_plot", (req, res) => {

  // execute generate_marker_plot()
  exec(`python ./python_scripts/data_analysis.py generate_marker_plot ${filename}`, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error executing Python script: ${error.message}`);
      return res.status(500).send("Internal Server Error");

    }

    // send plot as response download
    res.download(`./data/images/${filename}.png`);
    console.log("Plot downloaded");

  });

});

app.get("/generate_ma_plot", (req, res) => {

  // execute generate_ma_plot()
  exec(`python ./python_scripts/data_analysis.py generate_ma_plot ${filename}`, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error executing Python script: ${error.message}`);
      return res.status(500).send("Internal Server Error");

    }

    // send plot as response download
    res.download(`./data/images/${filename}-ma.png`);
    console.log("Plot downloaded");

  });

});

app.get("/generate_kmeans_plot", (req, res) => {

  // execute generate_kmeans_plot()
  exec(`python ./python_scripts/data_analysis.py generate_kmeans_plot ${filename}`, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error executing Python script: ${error.message}`);
      return res.status(500).send("Internal Server Error");

    }

    // send plot as response download
    res.download(`./data/images/${filename}-kmeans.png`);
    console.log("Plot downloaded");

  });

});

app.listen(port, () => {
  console.log(`Website is running at http://localhost:${port}`);

});
