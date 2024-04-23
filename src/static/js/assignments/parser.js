import { Assignment } from "./assignment.js"
import { Question } from "./question.js"
import { QuestionOption } from "./question_option.js"

export function sql_to_js(data)
{
	const questions = data.get("questions") || []
	const questionOptions = data.get("question_options") || {}

	const assignment = new Assignment(data)
	assignment.m_Questions = questions.map((rawQuestion) =>
	{
		const question = new Question(rawQuestion)

		const options = []
		const rawOptions = questionOptions[question.getID()]

		if (rawOptions)
			options = rawOptions.map(option => new QuestionOption(option))

		question.m_Options = options

		return question
	})

	return assignment
}
