import { Helper } from "./JSModules/helper.js"

import { Assignment, AssignmentQuestion } from "./assignment_models.js"
import { AssignmentRenderer } from "./assignment_renderer.js"

const g_Helper = new Helper()
const g_Renderer = new AssignmentRenderer()

g_Helper.hookEvent(window, "load", false, () =>
{
	const assignment = new Assignment(ASSIGNMENT_ID)

	assignment.fetchQuestions(() =>
	{
		g_Renderer.setAssignment(assignment)
		g_Renderer.render(document.querySelector("#assignment_render_target"), true)
	})
})
