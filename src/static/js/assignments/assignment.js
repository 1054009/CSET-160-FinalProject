import { Helper } from "../JSModules/helper.js"

export class Assignment
{
	constructor(data)
	{
		const helper = Helper.assignToObject(this)

		this.m_RawData = data

		this.m_iID = helper.getNumber(data.get("id"), false, -1)
		this.m_iTeacherID = helper.getNumber(data.get("teacher_id"), false, -1)
		this.m_strTitle = helper.getString(data.get("title"), "INVALID ASSIGNMENT")
		this.m_strDueDate = helper.getString(data.get("due_date"), "9999-12-31 00:00:00") // TODO: Make this an actual date object
		this.m_Questions = data.get("questions") || []
	}

	setTitle(title)
	{
		this.m_strTitle = this.getHelper().getString(title, "INVALID ASSIGNMENT")
	}

	setDueDate(dueDate)
	{
		this.m_strDueDate = this.getHelper().getString(dueDate, "9999-12-31 00:00:00") // TODO: Make this an actual date object
	}

	getID()
	{
		return this.m_iID
	}

	getTeacherID()
	{
		return this.m_iTeacherID
	}

	getTitle()
	{
		return this.m_strTitle
	}

	getDueDate()
	{
		return this.m_strDueDate
	}

	getQuestions()
	{
		return this.m_Questions
	}

	getQuestion(index)
	{
		return this.getQuestions()[index + 1]
	}
}
