import { Helper } from "./JSModules/helper.js"

import { Assignment, AssignmentQuestion } from "./assignment_models.js"
import { AssignmentRenderer } from "./assignment_renderer.js"

const g_Helper = new Helper()
const g_Renderer = new AssignmentRenderer()

g_Helper.hookEvent(window, "load", false, () =>
{
	const test = new Assignment(ASSIGNMENT_ID)

	test.fetchQuestions(() =>
	{
		g_Renderer.setAssignment(test)
		g_Renderer.render(document.querySelector("#assignment_render_target"), true)
	})
})
