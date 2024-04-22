// Imports
import { Helper } from "../JSModules/helper.js"
import { DOMBuilder } from "../JSModules/dom_builder.js"

import { Assignment } from "./assignment.js"

// Globals
const g_Helper = new Helper()
var g_Assignment = null

// Functions


// Hooks
g_Helper.hookEvent(window, "load", false, () =>
{
	g_Assignment = new Assignment(g_AssignmentData)
})
