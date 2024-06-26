import { Helper } from "./JSModules/helper.js"

export class Assignment
{
	constructor(id)
	{
		const helper = Helper.assignToObject(this)

		this.m_iID = helper.getUnsignedNumber(id, false, 0)

		this.m_Questions = []
	}

	getID()
	{
		return this.m_iID
	}

	getTitle()
	{
		return this.m_strTitle
	}

	getDueDate()
	{
		return this.m_strDueDate
	}

	fetchQuestions(callback)
	{
		const helper = this.getHelper()

		helper.fetchJSON(`${window.location.origin}/assignments/get_data/${this.getID()}`, (data) =>
		{
			try
			{
				if (!data && this.m_Questions.length < 1)
				{
					alert("Failed to get assignment data!")
					return
				}

				this.m_strTitle = helper.getString(data.title)
				this.m_strDueDate = helper.getString(data.due_date)

				// Setup questions
				if (helper.isArray(data.questions))
				{
					for (const questionData of data.questions)
						this.m_Questions.push(new AssignmentQuestion(questionData))
				}

				if (helper.isFunction(callback))
					callback()
			}
			catch (problematic_error_stupid)
			{
				console.log(problematic_error_stupid)
			}
		})
	}

	getQuestions()
	{
		return this.m_Questions
	}
}

export class AssignmentQuestion
{
	constructor(data)
	{
		const helper = Helper.assignToObject(this)

		this.m_iID = helper.getUnsignedNumber(data.id, false, 0)
		this.m_strText = helper.getString(data.text)
		this.m_strType = helper.getString(data.type)
		this.m_iPoints = helper.getNumber(data.points, false, 0)

		this.m_Options = []

		// Setup options
		if (helper.isArray(data.options))
		{
			for (const optionData of data.options)
				this.m_Options.push(new AssignmentQuestionOption(optionData))
		}
	}

	getID()
	{
		return this.m_iID
	}

	getText()
	{
		return this.m_strText
	}

	setText(text)
	{
		this.m_strText = this.getHelper().getString(text)
	}

	getType()
	{
		return this.m_strType
	}

	getPoints()
	{
		return this.m_iPoints
	}

	setPoints(points)
	{
		this.m_iPoints = helper.getNumber(points, false, 0)
	}

	getOptions()
	{
		return this.m_Options
	}
}

export class AssignmentQuestionOption
{
	constructor(data)
	{
		const helper = Helper.assignToObject(this)

		this.m_iID = helper.getUnsignedNumber(data.id, false, 0)
		this.m_strText = helper.getString(data.text)
		this.m_bCorrect = helper.getBoolean(data.is_correct)
	}

	getID()
	{
		return this.m_iID
	}

	getText()
	{
		return this.m_strText
	}

	setText(text)
	{
		this.m_strText = this.getHelper().getString(text)
	}

	getCorrect()
	{
		return this.m_bCorrect
	}

	setCorrect(correct)
	{
		this.m_bCorrect = this.getHelper().getBoolean(correct)
	}
}
