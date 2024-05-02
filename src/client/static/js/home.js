import { Helper } from "./JSModules/helper.js"
import { DOMBuilder } from "./JSModules/dom_builder.js"

import { Assignment } from "./assignment_models.js"
import { AssignmentRenderer } from "./assignment_renderer.js"

const g_Helper = new Helper()
const g_Builder = new DOMBuilder()
const g_Renderer = new AssignmentRenderer()

g_Helper.hookEvent(window, "load", false, () =>
{
	// TODO: Figure out why this says "Invalid Assignment"
	// TODO: Figure out why this causes a server error sometimes (???)

	const assignment_list = document.querySelector("#assignment_list")

	const overviewContainer = g_Builder.start(assignment_list)
	{
		for (const block of ASSIGNMENT_LIST)
		{
			const parsed = JSON.parse(block)
			const assignment = new Assignment(parsed.id)

			assignment.fetchQuestions(() =>
			{
				g_Builder.startPush(overviewContainer)
				{
					g_Builder.startElement("div")
					{
						g_Renderer.setAssignment(assignment)
						g_Renderer.renderOverview(g_Builder.getTop())
					}
					g_Builder.endElement()
				}
				g_Builder.endPop()
			})
		}
	}
	g_Builder.end()
})
