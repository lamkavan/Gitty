// IBM Summer Project 2019
// Kavan Lam and Nimrah Gill
// July 4, 2019

// Below is the code responsible for communicating with backend Python scripts
// to build and train the models

async function make_models(){
  await display_message("Creating and training the models please wait ...")
  response = await fetch("http://127.0.0.1:5000/make_models")
  if (response.status === 200){
  	accuracy = await response.json()
    await display_message("Models have been created and train successfully")
    await display_message("The prediction accuracy for teams is " + (accuracy["team_accuracy"] * 100).toFixed(2) + "%")
    await display_message("The prediction accuracy for assignees is " + (accuracy["assignee_accuracy"] * 100).toFixed(2) + "%")
    await display_message("")
  }else {
    await display_message("The creating and training of the model has failed. If models currently exist please delete them and try again. Alternatively, you can try restarting the flask server")
    await display_message("")
  }
}
