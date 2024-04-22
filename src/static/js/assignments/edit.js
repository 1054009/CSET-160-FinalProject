assignment = {}

assignment.add_question = () =>
{
	const question_type = document.querySelector("#question_type")
	if (!question_type) return

	const type = question_type.value
}

assignment.update_display = () =>
{
	const question_display = document.querySelector("#question_display")
	if (!question_display) return

	assignment_display.render_to(question_display)
}

window.addEventListener("load", () =>
{
	assignment.update_display()
})
