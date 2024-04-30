import { Helper } from "./JSModules/helper.js"

export class Assignment
{
	constructor(id)
	{
		const helper = Helper.assignToObject(this)

		this.m_iID = helper.getUnsignedNumber(id, false, 0)
		this.m_Questions = {}
	}

	getID()
	{
		return this.m_iID
	}

	fetchQuestions()
	{
		this.getHelper().fetchJSON(`${window.location.origin}/assignments/get_questions/${this.getID()}`, (data) =>
		{
			this.m_Questions = data
		})
	}

	getQuestions()
	{
		return this.m_Questions
	}
}

export class AssignmentQuestion
{

}
