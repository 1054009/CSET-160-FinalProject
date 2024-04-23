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

	renderOpenEnded(question, renderTarget, editable)
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

	renderMultipleChoice(question, renderTarget, editable)
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
					builder.addClass("question_option")

					builder.setAttribute("type", "radio")
					builder.setAttribute("name", "question_option")


					if (option.getCorrect())
						builder.setAttribute("checked", true)

					builder.setProperty("id", optionID)
				}
				builder.endElement()

				builder.startElement("label")
				{
					builder.addClass("question_option_label")

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

	renderAssignment(assignment, questionNumber, renderTarget, editable)
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

		const builder = this.m_Builder

		// Main question
		builder.start(renderTarget)
		{
			if (editable)
			{

			}
			else
			{
				builder.startElement("h3")
				{
					builder.setProperty("innerHTML", question.getText())
				}
				builder.endElement()
			}
		}
		builder.end()

		// The rest
		switch (question.getType())
		{
			default:
			case QUESTION_TYPE.OPEN_ENDED:
				this.renderOpenEnded(question, renderTarget, editable)
				break

			case QUESTION_TYPE.MULTIPLE_CHOICE:
				this.renderMultipleChoice(question, renderTarget, editable)
				break
		}
	}
}
