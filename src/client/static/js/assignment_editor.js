import { Helper } from "./JSModules/helper.js"

import { Assignment, AssignmentQuestion } from "./assignment_models.js"
import { AssignmentRenderer } from "./assignment_renderer.js"

const g_Helper = new Helper()
const g_Renderer = new AssignmentRenderer()

var g_Assignment = null

function render()
{
	g_Renderer.render(document.querySelector("#assignment_render_target"), true)
}

g_Helper.hookEvent(window, "load", false, () =>
{
	// Setup controls
	g_Helper.hookElementEvent(document.querySelector("#btn_prev_question"), "click", true, () =>
	{
		g_Renderer.setQuestionNumber(g_Renderer.getQuestionNumber() - 1)
		render()
	})

	g_Helper.hookElementEvent(document.querySelector("#btn_next_question"), "click", true, () =>
	{
		g_Renderer.setQuestionNumber(g_Renderer.getQuestionNumber() + 1)
		render()
	})

	g_Helper.hookElementEvent(document.querySelector("#btn_new_question"), "click", true, () =>
	{
		const type = document.querySelector("#question_type")
		if (!type) return

		g_Assignment.getQuestions().push(new AssignmentQuestion(
			{
				"text": "New Question",
				"points": 1,
				"type": type.value
			}
		))

		g_Renderer.setQuestionNumber(g_Assignment.getQuestions().length)
		render()
	})

	g_Assignment = new Assignment(ASSIGNMENT_ID)

	g_Assignment.fetchQuestions(() =>
	{
		g_Renderer.setAssignment(g_Assignment)
		render()
	})
})