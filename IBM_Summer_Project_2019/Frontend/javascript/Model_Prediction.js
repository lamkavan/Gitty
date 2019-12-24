// IBM Summer Project 2019
// Kavan Lam and Nimrah Gill
// July 4, 2019

// Below is the code responsible for communicating with backend Python scripts
// to process an issue text and predict the best team(s) and assignee(s)

async function make_prediction(e){
  issue_text = e.data.issue_text.val()
  await display_message("Making a prediction for --->" + issue_text)
  const body = JSON.stringify({
		"git_issue_text": issue_text
	})
  response = await fetch("http://127.0.0.1:5000/make_prediction", {method: "POST", body:body})
  if (response.status === 200){
    predictions = await response.json()
    await display_message("The top three team are ---> " + predictions.best_teams)
    await display_message("The top three assignees are ---> " + predictions.best_assignees)
    await display_message("")
  }else {
    await display_message("Something went wrong during prediction check to ensure you have models created. Maybe try remaking the models")
    await display_message("")
  }
}
