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
		const builder = this.m_Builder

		builder.start(renderTarget)
		{
			builder.startElement("textarea")
			{

			}
			builder.endElement()
		}
		builder.end()
	}

	renderMultipleChoice(question, renderTarget)
	{
		const builder = this.m_Builder

		builder.start(renderTarget)
		{
			const options = question.getOptions()
			for (const option of options)
			{
				const optionText = option.getText()
				const optionID = optionText + options.indexOf(option)

				builder.startElement("input")
				{
					builder.setAttribute("type", "radio")
					builder.setAttribute("name", "question_option")

					if (option.getCorrect())
						builder.setAttribute("checked", true)

					builder.setProperty("id", optionID)
				}
				builder.endElement()

				builder.startElement("label")
				{
					builder.setAttribute("for", optionID)

					builder.setProperty("innerHTML", optionText)
				}
				builder.endElement()

				builder.startElement("br")
				builder.endElement()
			}
		}
		builder.end()
	}

	renderAssignment(assignment, questionNumber, renderTarget)
	{
		const helper = this.getHelper()

		if (!helper.isValidElement(renderTarget))
			return

		renderTarget.innerHTML = ""

		const question = assignment.getQuestion(questionNumber)
		if (!question)
		{
			console.error("Invalid question (?)")
			return
		}

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
