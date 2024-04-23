import { Helper } from "../JSModules/helper.js"
import { DOMBuilder } from "../JSModules/dom_builder.js"

import { QUESTION_TYPE } from "./question.js"

export class AssignmentRenderer
{
	constructor()
	{
		Helper.assignToObject(this)

		this.m_Builder = new DOMBuilder()
	}

	renderOpenEnded(question, renderTarget)
	{

	}

	renderMultipleChoice(question, renderTarget)
	{

	}

	renderAssignment(assignment, questionNumber, renderTarget)
	{
		const helper = this.getHelper()

		if (!helper.isValidElement(renderTarget))
			return

		renderTarget.innerHTML = ""

		const question = assignment.getQuestion(questionNumber)

		// Main question
		this.m_Builder.start(renderTarget)
		{
			this.m_Builder.startElement("h3")
			{
				this.m_Builder.setProperty("innerHTML", question.getText())
			}
			this.m_Builder.endElement()
		}
		this.m_Builder.end()

		// The rest
		switch (question.getType())
		{
			default:
			case QUESTION_TYPE.OPEN_ENDED:
				this.renderOpenEnded(question, renderTarget)
				break

			case QUESTION_TYPE.MULTIPLE_CHOICE:
				this.renderMultipleChoice(question, renderTarget)
				break
		}
	}
}
