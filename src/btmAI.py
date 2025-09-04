import os
import groq
import json
import traceback

from groq import Groq


class BenthamGroq:
	def __init__(self, api_key = None, user_skills = [], post_content = ""):
		self.api_key = api_key
		self.user_skills = user_skills
		self.post_content = post_content.encode("utf-16", "surrogatepass").decode("utf-16")
		#create the client with given informations
		self.client = Groq(api_key = self.api_key)
		#create prompts for the AI
		self.prompt_system = '''
You are an assistant specialized in analyzing LinkedIn posts to identify relevant job opportunities in the 3D field.
Your role is to determine if a LinkedIn post explicitly mentions recruitment in the user's 3D specialties.
You must be very precise and avoid false positives. Only respond positively IF the post contains clear recruitment indicators AND explicitly mentions 3D-related skills.
'''		
		self.prompt_user = f'''
Analyze this LinkedIn post to determine if it's a recruitment offer matching my 3D skills.

MY 3D SKILLS:
{self.user_skills}

POST CONTENT TO ANALYZE:
{self.post_content}

EVALUATION CRITERIA:

1. RECRUITMENT INDICATORS:
   - Keywords: "hiring", "recruiting", "looking for", "seeking", "we're hiring", "join our team"
   - Mentions: "full-time", "part-time", "contract", "freelance", "position", "job", "career", "opportunity", "role"
   - Call to actions: "apply", "send CV", "contact us", "interested candidates", "submit portfolio"

2. 3D SKILLS MATCH (must be explicit):
   - Direct mention of one of my skills listed above
   - OR closely related terms (e.g., "3D artist" for "3D modeling", "Maya animator" for "Maya")
   - OR specific 3D technologies/software that I master

EXCLUSIONS (respond False):
- Generic company posts without recruitment
- Article shares or news
- Congratulations or internal announcements
- Recruitment in other fields (marketing, web dev, etc.)
- Vague mentions of "creativity" or "design" without 3D specification
- Educational content or tutorials
- Company culture posts
- Event announcements

MANDATORY RESPONSE FORMAT (valid PYTHON only):
{{
	"is_matching": True/False,
	"job_searched": "Exact job title as mentioned in the post" or None,
}}

IMPORTANT: 
- Respond with this PYTHON only, nothing else
- Be conservative: when in doubt, respond false
- The "job_searched" field must contain the exact job title if found

'''

	def run(self):
		try:
			response = self.client.chat.completions.create(
				model = "llama-3.3-70b-versatile",
				messages = [
					{"role":"system","content":self.prompt_system},
					{"role":"user","content":self.prompt_user}
				]
			)
			return response.choices[0].message.content
		except Exception as e:
			error_msg = f"Groq API Error: {str(e)}\nTraceback: {traceback.format_exc()}"
			raise Exception(error_msg) from e