import { Helper } from "./JSModules/helper.js"

import { Assignment, AssignmentQuestion } from "./assignment_models.js"
import { AssignmentRenderer } from "./assignment_renderer.js"

const g_Helper = new Helper()
const g_Renderer = new AssignmentRenderer()

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

	const assignment = new Assignment(ASSIGNMENT_ID)

	assignment.fetchQuestions(() =>
	{
		g_Renderer.setAssignment(assignment)
		render()
	})
})
