// IBM Summer Project 2019
// Kavan Lam and Nimrah Gill
// July 4, 2019

// --- Defining Constants and global variables --- //
const log = console.log
const base_url = "https://api.github.com"
const base_dir_output = "../output/"
const project_name = "OpenLiberty"
const username = "IBM-Gitty"
const password = "IBM-Gitty1234"
const date_partition = [" created:2016-01-01..2016-04-01", " created:2016-04-02..2016-08-01", " created:2016-08-02..2017-01-01",
						" created:2017-01-02..2017-04-01", " created:2017-04-02..2017-08-01", " created:2017-08-02..2018-01-01",
						" created:2018-01-02..2018-04-01", " created:2018-04-02..2018-08-01", " created:2018-08-02..2019-01-01",
						" created:2019-01-02..2019-04-01", " created:2019-04-02..2019-08-01", " created:2019-08-02..2020-01-01"]
const output_ext = ".txt"
const output_header = "Issue Title,Teams Assigned,Assignees\n"
let api_usage_count = 0
let all_teams = []
let all_assignees = []


// --- Defining Event Handlers --- //
async function query_only_open_liberty(){
	// First we need to retrieve the names of all the repos in OpenLiberty project (trival step)
	let name_of_all_repos = ["open-liberty"]
	// Now we need to go through all the repos and collect the issue data
	await collect_issue_data(name_of_all_repos)
	// Here we output to a txt file the list of all teams and assignees (no dups)
	await collect_team_and_assignee_data()
	// Let the user know the application has finished
	await display_message("Collecting issue data from open-liberty repository has completed.")
}


async function query_all_repos(){
	// First we need to retrieve the names of all the repos in OpenLiberty project
	let name_of_all_repos = await get_all_repo_names()
	// Now we need to go through all the repos and collect the issue data
	await collect_issue_data(name_of_all_repos)
	// Here we output to a txt file the list of all teams and assignees (no dups)
	await collect_team_and_assignee_data()
	// Let the user know the application has finished
	await display_message("Collecting issue data from all OpenLiberty repos has completed.")
}


// --- Helper Funtions --- //
async function display_message(message){
	const div_space = document.getElementById("content_box")
	await div_space.appendChild(document.createTextNode(message))
	await div_space.appendChild(document.createElement("br"))
}


async function write_to_file(file_name, text){
	let data = {
    	file_name: "../output/" + file_name,
    	text: text
  	}
    const request = new Request("/writeToFile", {
    	method: "post",
    	body: JSON.stringify(data),
    	headers: {
    		"Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json"
        }
    })
	response = await fetch(request)
}

async function collect_team_and_assignee_data(){
	all_teams_str = all_teams.join() + "\n"
	all_assignees_str = all_assignees.join() + "\n"
	await write_to_file("list_of_team" + output_ext, all_teams_str)
	await write_to_file("list_of_assignees" + output_ext, all_assignees_str)
}


function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}


async function consider_api_limit(){
	if (api_usage_count > 27){
		await sleep(60000)  // sleep for 1 min = 60000 milliseconds
		api_usage_count = 0
	}
	api_usage_count = api_usage_count + 1
}


async function get_next_page_url(link_string){
	if (link_string === null){
		return ""
	}

	let links = link_string.split(",")
	let next_url = ""
	let temp

	for (let link of links){
		if (link.includes('rel="next"')){
			temp = (link.split('rel="next"'))[0]
			if (link[0] === " "){
				next_url = (temp).substring(2, temp.indexOf(">;"))
				break
			}
			next_url = (temp).substring(1, temp.indexOf(">;"))
			break
		}
	}

	// Next page does not exist
	return next_url
}


async function fetch_repos_from_project(){
	// Ex of link <https://api.github.com/search/repositories?q=org%3AOpenLiberty&page=2>; rel="next", <https://api.github.com/search/repositories?q=org%3AOpenLiberty&page=3>; rel="last"
	const header = {
		"Authorization": `Basic ${btoa(`${username}:${password}`)}`
	}
	let url = ""
	let result = []
	let next_page_url = ""
	let link_string = ""
	let response

	while (true){
		url = next_page_url
		if (next_page_url === ""){
			url = base_url + "/search/repositories?q=org:" + project_name
		}
		// Make the API call
		await consider_api_limit()
		response = await fetch(url, {"method": "GET", "headers": header})
		link_string = await response.headers.get("link")
		next_page_url = await get_next_page_url(link_string)
		response = (await response.json()).items
		// Store the names of the repos from current page
		for (let repo of response){
			if (!(repo.private)){
				result.push(repo.name)
			}
		}
		// Exit the loop when there are no more pages
		if (next_page_url === ""){
			break
		}
	}
	return result
}


async function get_all_repo_names(){
	await display_message("Collecting the names of all the repos within the OpenLiberty project from Github...")
	// Make a request to the Github REST API to query for all the repos
	const result = await fetch_repos_from_project()
	await display_message("Finished collecting the names of repos from OpenLiberty")
	return result
}


async function repo_reach_issue_limit(repo_name){
	const header = {
		"Authorization": `Basic ${btoa(`${username}:${password}`)}`
	}
	let url = base_url + "/search/issues?q=repo:" + project_name + "/" + repo_name + " type:issue"
	await consider_api_limit()
	let response = await fetch(url, {"method": "GET", "headers": header})
	response = (await response.json())
	if (response.total_count > 999){
		return true
	}
	return false
}


async function get_assigness(assignees_raw_list){
	let assignees_list = []
	for (let assignee of assignees_raw_list){
		await assignees_list.push(assignee.login)
		if (!(all_assignees.includes(assignee.login))){
			all_assignees.push(assignee.login)
		}
	}
	return assignees_list
}


async function get_teams(team_raw_list){
	let team_list = []
	for (let team of team_raw_list){
		if ((team.name).substring(0, 5) === "team:"){
			await team_list.push((team.name).substring(5, (team.name).length))
			if (!(all_teams.includes((team.name).substring(5, (team.name).length)))){
				all_teams.push((team.name).substring(5, (team.name).length))
			}
		}
	}
	return team_list
}


async function collect_issues_in_repo(repo_name){
	const header = {
		"Authorization": `Basic ${btoa(`${username}:${password}`)}`
	}
	let url = ""
	let next_page_url = ""
	let link_string = ""
	let response
	let dates

	// First we need to check if the repo has more than 1000 issues
	if (await repo_reach_issue_limit(repo_name)){
		dates = date_partition
	}else{
		dates = [""]
	}

	// Now we prepare a txt file to write issue data to
	await write_to_file(repo_name + output_ext, output_header)

	// Get the issue data and write to file
	for (let date of dates){
		while (true){
			url = next_page_url
			if (next_page_url === ""){
				url = base_url + "/search/issues?q=repo:" + project_name + "/" + repo_name + " type:issue" + date + " &per_page=100"
			}
			// Make the API call
			await consider_api_limit()
			response = await fetch(url, {"method": "GET", "headers": header})
			link_string = await response.headers.get("link")
			next_page_url = await get_next_page_url(link_string)
			response = (await response.json()).items
			// Export the issue data to a txt file
			for (let issue of response){
				let assignees = await get_assigness(issue.assignees)
				let teams_assigned = await get_teams(issue.labels)
				let issue_text = "\"" + issue.title + "\"," + "\"" + teams_assigned.toString() + "\"," + "\"" + assignees.toString() + "\"" + "\n"
				await write_to_file(repo_name + output_ext, issue_text)
			}
			// Exit the loop when there are no more pages
			if (next_page_url === ""){
				break
			}
		}
	}
}


async function collect_issue_data(name_of_all_repos){
	await display_message("Starting to collect issue data from repo(s)")
	for (let repo of name_of_all_repos){
		await display_message("Collecting issue data from " + repo + "...")
		await collect_issues_in_repo(repo)
		await display_message("Finished collecting issue data from " + repo)
	}
	await display_message("Finished collecting data from repo(s)")
}


// Call this to build the view (this is what the user see as soon as they enter Gitty)
build_basic_view()
build_data_search_view()
