// IBM Summer Project 2019
// Kavan Lam and Nimrah Gill
// July 4, 2019

// --- Import Dependencies --- //
const express = require("../dependencies/node_modules/express")
const bodyParser = require("../dependencies/node_modules/body-parser")
const path = require('path')
const fs = require("fs")


// --- Constants --- //
const log = console.log
const port = process.env.PORT || 3000


// --- Initialize Express Server --- //
const app = express()
app.use(bodyParser.json())
app.use(bodyParser.urlencoded({extended:true}))
app.use(express.static(__dirname))
app.use('/css', express.static(path.join(__dirname, "../css")));


// --- Express Routes --- //
app.get("/", (req, res) => {
  // load up the user interface
  res.sendFile(path.join(__dirname, "../index.html"));
})

app.post("/writeToFile", (req, res) =>{
	fs.appendFileSync(req.body.file_name, req.body.text, (err) => {
		if (err) throw err
	})
	res.status(200).send("OK, made changes to the file.")
})


// --- Begin Listening --- //
app.listen(port, () => {
	log("Listening on port " + port)
});
