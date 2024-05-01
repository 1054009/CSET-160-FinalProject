import { Helper } from "./JSModules/helper.js"
import { DOMBuilder } from "./JSModules/dom_builder.js"

import { Assignment } from "./assignment_models.js"
import { AssignmentRenderer } from "./assignment_renderer.js"

const g_Helper = new Helper()
const g_Builder = new DOMBuilder()
const g_Renderer = new AssignmentRenderer()

g_Helper.hookEvent(window, "load", false, () =>
{
	const assignment_list = document.querySelector("#assignment_list")

	const overviewContainer = g_Builder.start(assignment_list)
	{
		for (const block of ASSIGNMENT_LIST)
		{
			const parsed = JSON.parse(block)
			const assignment = new Assignment(parsed.id)

			assignment.fetchQuestions(() =>
			{
				g_Renderer.setAssignment(assignment)
				g_Renderer.renderOverview(overviewContainer)
			})
		}
	}
	g_Builder.end()
})
