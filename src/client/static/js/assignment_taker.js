import { Helper } from "./JSModules/helper.js"

import { Assignment } from "./assignment_models.js"
import { AssignmentRenderer } from "./assignment_renderer.js"

const g_Helper = new Helper()
const g_Renderer = new AssignmentRenderer()

var g_Assignment = null

function render(questionNumber)
{
	g_Renderer.setQuestionNumber(g_Helper.getNumber(questionNumber, false, 1))
	g_Renderer.render(document.querySelector("#assignment_render_target"), false)
}

g_Helper.hookEvent(window, "load", false, () =>
{
	g_Assignment = new Assignment(ASSIGNMENT_ID)

	g_Assignment.fetchQuestions(() =>
	{
		g_Renderer.setAssignment(g_Assignment)
		render()
	})
})

// TODO: Come back
