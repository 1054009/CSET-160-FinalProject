import { Helper } from "./JSModules/helper.js"
import { DOMBuilder } from "./JSModules/dom_builder.js"

export class AssignmentRenderer
{
	constructor()
	{
		Helper.assignToObject(this)
		this.m_Builder = new DOMBuilder()
	}

	setAssignment(assignment)
	{
		this.m_Assignment = assignment

		this.setQuestionNumber(1)
	}

	getAssignment()
	{
		return this.m_Assignment
	}

	setQuestionNumber(number)
	{
		const helper = this.getHelper()

		const minQuestion = 1
		const maxQuestion = this.getAssignment().getQuestions().length

		this.m_iQuestionNumber = helper.clamp(helper.getNumber(number, false, 1), minQuestion, maxQuestion)
	}

	getQuestionNumber()
	{
		return this.m_iQuestionNumber
	}

	multipleChoice(builder, question, editable)
	{
		builder.startElement("div")
		{
			builder.addClass("flexbox")
			builder.addClass("flex_column")
			builder.addClass("flex_gap")

			for (const option of question.getOptions())
			{
				builder.startElement("div")
				{
					builder.addClass("flexbox")
					builder.addClass("flex_gap")
					builder.addClass("flex_vcenter")

					builder.startElement("input") // TODO: Make the inputs do something
					{
						builder.setAttribute("type", "radio")
						builder.setAttribute("name", "question_option")

						builder.setProperty("checked", editable ? option.getCorrect() : false)
					}
					builder.endElement()

					if (editable)
					{
						builder.startElement("input") // TODO: Make the inputs do something
						{
							builder.addClass("flex_fill")

							builder.setAttribute("type", "text")
							builder.setAttribute("maxlength", "65535")
							builder.setAttribute("required", true)

							builder.setProperty("value", option.getText())
						}
						builder.endElement()
					}
					else
					{
						builder.startElement("p")
						{
							builder.setProperty("innerHTML", option.getText())
						}
						builder.endElement()
					}
				}
				builder.endElement()
			}
		}
		builder.endElement()
	}

	openEnded(builder, question, editable)
	{
		builder.startElement("textarea")
		{
			// TODO: Maybe something else?
		}
		builder.endElement()
	}

	render(target, editable)
	{
		const helper = this.getHelper()
		if (!helper.isValidElement(target))
			return

		const builder = this.m_Builder
		const assignment = this.getAssignment()

		// Base
		builder.start(target)
		{
			builder.setProperty("innerHTML", "")

			if (editable)
			{
				builder.startElement("input")
				{
					builder.setAttribute("type", "text")
					builder.setAttribute("maxlength", 255)
					builder.setAttribute("placeholder", "Assignment Title")
					builder.setAttribute("required", true)

					builder.setProperty("value", assignment.getTitle())
				}
				builder.endElement()
			}
			else
			{
				builder.startElement("h3")
				{
					builder.setProperty("innerHTML", assignment.getTitle())
				}
				builder.endElement()
			}

			const question = assignment.getQuestions()[this.getQuestionNumber() - 1]
			if (question)
			{
				if (editable)
				{
					builder.startElement("input")
					{
						builder.setAttribute("type", "text")
						builder.setAttribute("maxlength", 65535)
						builder.setAttribute("placeholder", "Question text")
						builder.setAttribute("required", true)

						builder.setProperty("value", question.getText())
					}
					builder.endElement()
				}
				else
				{
					builder.startElement("h3")
				{
					builder.setProperty("innerHTML", question.getText())
				}
				builder.endElement()
				}

				if (question.getType() == "MULTIPLE_CHOICE")
					this.multipleChoice(builder, question, editable)
				else
					this.openEnded(builder, question, editable)
			}
		}
		builder.end()
	}
}
