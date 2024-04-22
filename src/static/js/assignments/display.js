assignment_display = {}
assignment_display.data = new Map()

assignment_display.create_question_body = () =>
{
	const question_body = document.createElement("div")
	question_body.classList.add("question_body")

	return question_body
}

assignment_display.import = (id, data, questions) =>
{
	assignment_display.data.set("id", id)
	assignment_display.data.set("data", data)
	assignment_display.data.set("questions", questions)
}

assignment_display.render_to = (display_element) =>
{
	display_element.innerHTML = ""

	const question_body = assignment_display.create_question_body()

}
