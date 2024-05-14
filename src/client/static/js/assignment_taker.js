import { Helper } from "./JSModules/helper.js"
import { DOMBuilder } from "./JSModules/dom_builder.js"

import { Assignment, AssignmentQuestionOption } from "./assignment_models.js"
import { AssignmentRenderer } from "./assignment_renderer.js"

const g_Helper = new Helper()
const g_Builder = new DOMBuilder()
const g_Renderer = new AssignmentRenderer()

var g_Assignment = null
var g_Submissions = {}

function render(questionNumber)
{
	g_Renderer.setQuestionNumber(g_Helper.getNumber(questionNumber, false, 1))
	g_Renderer.render(document.querySelector("#assignment_render_target"), false, onQuestion, onSubmit)
}

function onQuestion(question, data)
{
	// Ugly
	if (!data)
		g_Submissions[question.getID()] = 0
	else
		if (g_Helper.isString(data))
			g_Submissions[question.getID()] = data
		else if (data instanceof AssignmentQuestionOption)
			g_Submissions[question.getID()] = data.getID()
		else
			g_Submissions[question.getID()] = 0
}

function onSubmit()
{
	const existing = document.querySelector("input[name=assignment_data]")
	if (g_Helper.isValidElement(existing))
		existing.remove()

	g_Submissions["assignment_id"] = g_Assignment.getID()

	g_Builder.start(document.querySelector("#assignment_render_target"))
	{
		g_Builder.startElement("input")
		{
			g_Builder.setAttribute("type", "hidden")
			g_Builder.setAttribute("name", "assignment_data")

			g_Builder.setProperty("value", JSON.stringify(g_Submissions))
		}
		g_Builder.endElement()
	}
	g_Builder.end()
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
