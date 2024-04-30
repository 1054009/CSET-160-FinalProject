import { Helper } from "./JSModules/helper.js"

import { Assignment, AssignmentQuestion } from "./assignment_models.js"
import { AssignmentRenderer } from "./assignment_renderer.js"

const g_Helper = new Helper()

g_Helper.hookEvent(window, "load", false, () =>
{
	const test = new Assignment(ASSIGNMENT_ID)

	test.fetchQuestions(() =>
	{
		console.log(test)

		console.log(test.getQuestions())
	})
})
