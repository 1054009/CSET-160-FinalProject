import { Helper } from "./JSModules/helper.js"

import { Assignment, AssignmentQuestion } from "./assignment_models.js"
import { AssignmentRenderer } from "./assignment_renderer.js"

const g_Helper = new Helper()
const g_Renderer = new AssignmentRenderer()

var g_Assignment = null

function render(questionNumber)
{
	g_Renderer.setQuestionNumber(g_Helper.getNumber(questionNumber, false, 1))
	g_Renderer.render(document.querySelector("#assignment_render_target"), true)
}

g_Helper.hookEvent(window, "load", false, () =>
{
	// Setup controls
	g_Helper.hookElementEvent(document.querySelector("#btn_prev_question"), "click", true, () =>
	{
		render(g_Renderer.getQuestionNumber() - 1)
	})

	g_Helper.hookElementEvent(document.querySelector("#btn_next_question"), "click", true, () =>
	{
		render(g_Renderer.getQuestionNumber() + 1)
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

		render(g_Renderer.getQuestionCount())
	})

	g_Helper.hookElementEvent(document.querySelector("#btn_del_question"), "click", true, () =>
	{
		g_Assignment.getQuestions().splice(0, 1)
		render(g_Renderer.getQuestionNumber())
	})

	g_Helper.hookElementEvent(document.querySelector("form"), "submit", true, () =>
	{
		const assignment_data = document.querySelector("input[name=assignment_data]")

		const assignmentData = {
			"title": g_Assignment.getTitle(),
			"due_date": g_Assignment.getDueDate(),

			"questions": []
		}

		for (const question of g_Assignment.getQuestions())
		{
			const options = []

			for (const option of question.getOptions())
				options.push({
					"text": option.getText(),
					"is_correct": option.getCorrect()
				})

			assignmentData["questions"].push({
				"text": question.getText(),
				"points": question.getPoints(),
				"type": question.getType(),

				"options": options
			})
		}

		assignment_data.value = JSON.stringify(assignmentData)
	})

	// Setup assignment data
	g_Assignment = new Assignment(ASSIGNMENT_ID)

	g_Assignment.fetchQuestions(() =>
	{
		g_Renderer.setAssignment(g_Assignment)
		render()
	})
})
