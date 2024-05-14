import { Helper } from "./JSModules/helper.js"
import { DOMBuilder } from "./JSModules/dom_builder.js"

const g_Helper = new Helper()
const g_Builder = new DOMBuilder()

g_Helper.hookEvent(window, "load", false, () =>
{
	const list = document.querySelector("div")

	g_Builder.start(list)
	{
		for (const block of USER_LIST)
		{
			const parsed = JSON.parse(block)

			g_Builder.startElement("div")
			{
				g_Builder.addClass("flexbox")
				g_Builder.addClass("flex_vcenter")

				g_Builder.startElement("p")
				{
					g_Builder.setProperty(
						"innerHTML",
						`(${parsed.id}) ${parsed.first_name} ${parsed.last_name} ${parsed.email_address} ${parsed.type}`
					)
				}
				g_Builder.endElement()
			}
			g_Builder.endElement()
		}
	}
	g_Builder.end()
})

// TODO: Come back
