import { Helper } from "../JSModules/helper.js"
import { Enum } from "../JSModules/enum.js"

export const QUESTION_TYPE = new Enum([ "OPEN_ENDED", "MULTIPLE_CHOICE" ])

export class Question
{
	constructor(data)
	{
		const helper = Helper.assignToObject(this)

		this.m_RawData = data

		this.m_iID = helper.getNumber(data.get("id"), false, -1)
		this.m_iAssignmentID = helper.getNumber(data.get("assignment_id"), false, -1)
		this.m_strText = helper.getString(data.get("text"), "INVALID QUESTION")
		this.m_iType = QUESTION_TYPE.lookupValue(helper.getString(data.get("type"), QUESTION_TYPE.translateValue(QUESTION_TYPE.MIN)))
		this.m_iPoints = helper.getNumber(data.get("points"), false, 0)
	}
}
