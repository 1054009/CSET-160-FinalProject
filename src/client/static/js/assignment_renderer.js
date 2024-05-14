import { Helper } from "./JSModules/helper.js"
import { DOMBuilder } from "./JSModules/dom_builder.js"

import { AssignmentQuestionOption } from "./assignment_models.js"

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

	getQuestionCount()
	{
		return this.getAssignment().getQuestions().length
	}

	multipleChoice(builder, question, editable, questionCallback, submitCallback)
	{
		const helper = this.getHelper()

		builder.startElement("div")
		{
			builder.addClass("flexbox")
			builder.addClass("flex_column")
			builder.addClass("flex_gap")

			for (const option of question.getOptions())
			{
				const optionIndex = question.getOptions().indexOf(option)

				builder.startElement("div")
				{
					builder.addClass("flexbox")
					builder.addClass("flex_gap")
					builder.addClass("flex_vcenter")

					builder.startElement("input")
					{
						builder.setAttribute("type", "radio")
						builder.setAttribute("name", "question_option")

						builder.setProperty("m_Option", option)
						builder.setProperty("checked", editable ? option.getCorrect() : false)

						if (editable)
						{
							helper.hookElementEvent(builder.getTop(), "change", true, () =>
							{
								for (const option of question.getOptions())
									option.setCorrect(false)

								option.setCorrect(true)
							})
						}
						else
						{
							// TODO: Log answer
						}
					}
					builder.endElement()

					if (editable)
					{
						builder.startElement("input")
						{
							builder.addClass("flex_fill")

							builder.setAttribute("type", "text")
							builder.setAttribute("maxlength", "65535")
							builder.setAttribute("required", true)

							builder.setProperty("value", option.getText())

							// Why are there so many :/
							const onchange = (_, self) =>
							{
								option.setText(self.value)
							}

							helper.hookElementEvent(builder.getTop(), "change", true, onchange)
							helper.hookElementEvent(builder.getTop(), "keypress", true, onchange)
							helper.hookElementEvent(builder.getTop(), "paste", true, onchange)
							helper.hookElementEvent(builder.getTop(), "input", true, onchange)
						}
						builder.endElement()

						builder.startElement("button")
						{
							builder.setProperty("innerHTML", "Delete Option")

							helper.hookElementEvent(builder.getTop(), "click", true, () =>
							{
								question.getOptions().splice(optionIndex, 1)
								this.refresh(true)
							})
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

			if (editable)
			{
				builder.startElement("button")
				{
					builder.setProperty("innerHTML", "Add Option")

					helper.hookElementEvent(builder.getTop(), "click", true, () =>
					{
						question.getOptions().push(new AssignmentQuestionOption(
							{
								"text": "New Option",
								"is_correct": false
							}
						))

						this.refresh(true)
					})
				}
				builder.endElement()
			}
			else
			{
				builder.startElement("input")
				{
					builder.setAttribute("type", "submit")

					builder.setProperty("value", "Submit Answer")

					// Can't use hookElementEvent because of stacking events
					this.m_RenderTarget.onsubmit = (event) =>
					{
						const chosen = document.querySelector("input[type=radio]:checked")

						if (helper.isFunction(questionCallback))
						{
							if (!helper.isValidElement(chosen))
								questionCallback(question, null)
							else
								questionCallback(question, chosen.m_Option || null)
						}

						if (this.getQuestionNumber() >= this.getQuestionCount())
						{
							if (helper.isFunction(submitCallback))
								submitCallback()
						}
						else
						{
							// Go to the next question
							this.setQuestionNumber(this.getQuestionNumber() + 1)
							this.refresh(false, questionCallback, submitCallback)

							event.preventDefault()

							return false
						}
					}
				}
				builder.endElement()
			}
		}
		builder.endElement()
	}

	openEnded(builder, question, editable, questionCallback, submitCallback)
	{
		const helper = this.getHelper()

		const textArea = builder.startElement("textarea")
		{
			// TODO: Maybe something else?
		}
		builder.endElement()

		builder.startElement("input")
		{
			builder.setAttribute("type", "submit")

			builder.setProperty("value", "Submit Answer")

			this.m_RenderTarget.onsubmit = (event) =>
			{
				if (helper.isFunction(questionCallback))
					questionCallback(question, textArea.value)

				if (this.getQuestionNumber() >= this.getQuestionCount())
				{
					if (helper.isFunction(submitCallback))
						submitCallback()
				}
				else
				{
					// Go to the next question
					this.setQuestionNumber(this.getQuestionNumber() + 1)
					this.refresh(false, questionCallback, submitCallback)

					event.preventDefault()

					return false
				}
			}
		}
		builder.endElement()
	}

	render(target, editable, questionCallback, submitCallback)
	{
		const helper = this.getHelper()
		if (!helper.isValidElement(target))
			return

		const builder = this.m_Builder
		const assignment = this.getAssignment()

		this.m_RenderTarget = target

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

					// TODO: Handle input
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

						// TODO: Handle input
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
					this.multipleChoice(builder, question, editable, questionCallback, submitCallback)
				else
					this.openEnded(builder, question, editable, questionCallback, submitCallback)
			}
		}
		builder.end()
	}

	refresh(editable, questionCallback, submitCallback)
	{
		this.render(this.m_RenderTarget, editable, questionCallback, submitCallback)
	}

	renderOverview(target)
	{
		const helper = this.getHelper()
		if (!helper.isValidElement(target))
			return

		const builder = this.m_Builder
		const assignment = this.getAssignment()

		this.m_RenderTarget = target

		builder.start(target)
		{
			builder.setProperty("innerHTML", "")

			builder.startElement("div")
			{
				builder.addClass("flexbox")
				builder.addClass("flex_hspace")
				builder.addClass("flex_vcenter")

				builder.startElement("div")
				{
					builder.addClass("flexbox")
					builder.addClass("flex_column")

					builder.startElement("p")
					{
						builder.setProperty("innerHTML", assignment.getTitle())
					}
					builder.endElement()

					builder.startElement("p")
					{
						builder.setProperty("innerHTML", assignment.getDueDate())
					}
					builder.endElement()
				}
				builder.endElement()

				builder.startElement("button")
				{
					builder.setProperty("innerHTML", "Take")

					helper.hookElementEvent(builder.getTop(), "click", true, () =>
					{
						top.location = `/assignments/take/${assignment.getID()}`
					})
				}
				builder.endElement()
			}
			builder.endElement()
		}
		builder.end()
	}
}
