import { Helper } from "./JSModules/helper.js"

const g_Helper = new Helper()

g_Helper.hookEvent(window, "load", false, () =>
{
	console.log("hey")
})
