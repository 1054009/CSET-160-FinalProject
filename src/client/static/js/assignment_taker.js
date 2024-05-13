import { Helper } from "./JSModules/helper.js"

import { Assignment, AssignmentQuestionOption } from "./assignment_models.js"
import { AssignmentRenderer } from "./assignment_renderer.js"

const g_Helper = new Helper()
const g_Renderer = new AssignmentRenderer()

var g_Assignment = null
var g_Submissions = {}

function render(questionNumber)
{
	g_Renderer.setQuestionNumber(g_Helper.getNumber(questionNumber, false, 1))
	g_Renderer.render(document.querySelector("#assignment_render_target"), false, onSubmit)
}

function onSubmit(question, data)
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

	// Go to the next question
	if (g_Renderer.getQuestionNumber() == g_Renderer.getQuestionCount())
	{
		// TODO: Submit it actually
		top.location = "/home/"
	}
	else
		render(g_Renderer.getQuestionNumber() + 1)
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
