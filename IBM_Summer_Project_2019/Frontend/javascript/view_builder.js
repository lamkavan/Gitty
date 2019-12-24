// IBM Summer Project 2019
// Kavan Lam and Nimrah Gill
// July 4, 2019

// This just builds the top portion of view which is constant
function build_basic_view(){
	// Clear the view
	const body = $("body")

	// Setup the header
	const header = $('<header>')
	const row1 = $('<div id="master_container">')

	// Add the website title to the header
	const website_title = $('<h1> Gitty </h1>')
	row1.append(website_title)

	// Add the navigation buttons
	const data_search_button = $('<button id="nav_button" type="button" class="btn btn-outline-primary">Data Search</button>')
	const model_creation_button = $('<button id="nav_button" type="button" class="btn btn-outline-warning">Model Creation</button>')
	const predict_button = $('<button id="nav_button" type="button" class="btn btn-outline-success">Predict</button>')
  data_search_button.on("click", build_data_search_view)
  model_creation_button.on("click", build_model_creation_view)
  predict_button.on("click", build_predict_view)
	row1.append(data_search_button)
	row1.append(model_creation_button)
	row1.append(predict_button)

	// Add the Gitty info content which is hidden until user presses button
	const gitty_info = $(`
  <div class="collapse" id="navbarToggleExternalContent">
    <div class="bg-dark p-4">
      <h5 class="text-white h4">Information</h5>
      <span class="text-muted">IBM Summer Project 2019 <a class="header_links" href="https://github.ibm.com/kavan-lam/Gitty" target="_blank">View the git repository</a> <br> Developers:
			Kavan Lam and Nimrah Gill <br> Mentor/Guidance: Don Bourne <br>
			Gitty automates git issue routing using artificial intelligence to
			determine the best team and/or person to assign to</span>
    </div>
  </div>`)
  header.append(gitty_info)

	// Add the hidden info button
	const hidden_info_button = $(`<nav class="navbar navbar-dark">
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarToggleExternalContent" aria-controls="navbarToggleExternalContent" aria-expanded="false" aria-label="Toggle navigation">
      <div class="navbar-toggler-icon"></div>
    </button>
  </nav>`)
	row1.append(hidden_info_button)

	// Finish by adding the master container (this holds everything) to the body
	header.append(row1) // Ensure row1 get append after gitty_info
	body.append(header)
}


function build_data_search_view(){
  // Grab the body and main portions of view
  const body = $("body")
  const main = $("main")
  main.empty()

  // Add the page title
  const page_title = $('<h2>Data Search</h2>')
  main.append(page_title)

  // Add the buttons
  const query_ol_btn = $('<button id="page_buttons" type="button" class="btn btn-primary btn-lg btn-block">Query only open-liberty</button>')
  const query_all_btn = $('<button id="page_buttons" type="button" class="btn btn-primary btn-lg btn-block">Query all repository in OpenLiberty project</button>')
  //Ensure to uncomment below before release...
  //query_ol_btn.on("click", query_only_open_liberty)
  //query_all_btn.on("click", query_all_repos)
  main.append(query_ol_btn)
  main.append(query_all_btn)

  // Add content_box
  const content_box = $('<div id="content_box">')
  main.append(content_box)

  // Add all changes to main to the body so changes are visible
  body.append(main)
}


function build_model_creation_view(){
  // Grab the body and main portions of view
  const body = $("body")
  const main = $("main")
  main.empty()

  // Add the page title
  const page_title = $('<h3>Model Creation</h2>')
  main.append(page_title)

  // Add the buttons
  const create_model_btn = $('<button id="page_buttons" type="button" class="btn btn-warning btn-lg btn-block">Build and train models</button>')
  create_model_btn.on("click", make_models)
  main.append(create_model_btn)

  // Add content_box
  const content_box = $('<div id="content_box">')
  main.append(content_box)

  // Add all changes to main to the body so changes are visible
  body.append(main)
}


function build_predict_view(){
  // Grab the body and main portions of view
  const body = $("body")
  const main = $("main")
  main.empty()

  // Add the page title
  const page_title = $('<h4>Predict</h2>')
  main.append(page_title)

  // Add the text box
  const issue_text_box = $('<input type="text" class="form-control" id="issue_text_box" placeholder="Enter git issue text">')
  main.append(issue_text_box)

  // Add the buttons
  const predict_btn = $('<button id="page_buttons" type="button" class="btn btn-success btn-lg btn-block">Make prediction</button>')
  predict_btn.on("click", {issue_text: issue_text_box}, make_prediction)
  main.append(predict_btn)

  // Add content_box
  const content_box = $('<div id="content_box">')
  main.append(content_box)

  // Add all changes to main to the body so changes are visible
  body.append(main)
}
