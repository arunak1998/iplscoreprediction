import pymongo
from src.llmcall.mongo import readmango
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from langsmith import traceable


groq_api_key=os.getenv('GROQ_API_KEY')

def get_model():
    model=ChatGroq(api_key=groq_api_key,model='llama3-70b-8192')
    return model

def getprompt():
    prompt_template = PromptTemplate.from_template(
    """You are a Cricket Commentator tasked with providing real-time, engaging commentary based on the scores of the teams chasing. Your commentary should be natural, flowing, and reflective of the current match situation.

You will receive the following information:

Runs scored
Remaining overs
Remaining wickets
Required run rate
Current run rate
Insight from the ML model
In your commentary:

Don't Include any Unknown Stats or Players Name 

Reflect on the Pressure: If the overs are few and the required run rate is high, describe the pressure on both teams. Highlight critical moments and strategies naturally within the flow of the commentary.

Emphasize Fast-Paced Scoring: When the batting team is scoring quickly and the target is within reach, convey the excitement and fast-paced nature of the game without overly emphasizing specific points.

Discuss Early Wickets: If early wickets have fallen, address their impact on the batting team’s strategy and the overall game in a smooth, integrated manner.

Incorporate ML Insight: Integrate the insight from the ML model into your analysis, mentioning it as part of the ongoing assessment of the match situation. Ensure that this insight adds depth rather than serving as a definitive prediction.

Input Data: {input}
External Data: {external}
    """
)


   
    return prompt_template

@traceable
async def createchain(input_data):

    chain=getprompt() | get_model() | StrOutputParser()

   
    external_data=readmango(input_data.get('batting_team'),input_data.get('bowling_team'))


    result=(chain.invoke({"input":input_data,"external":external_data}))
    return result

if __name__=='__main__':
    createchain()

    