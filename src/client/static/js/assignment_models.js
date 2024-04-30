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
		this.getHelper().fetchJSON(`/assignments/get_questions/${this.getID()}`, (json) =>
		{
			console.log(json)
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
