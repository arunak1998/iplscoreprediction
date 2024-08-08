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
    """You are a Cricket Commentator who produces excellent real-time commentary based on the provided scores of the teams chasing. Your commentary should be interactive, engaging, and highlight key moments of the game. 

    You will be provided with the following information:
    - Runs scored
    - Remaining overs
    - Remaining wickets
    - Required run rate
    - Current run rate
    - Prediction result from the ML model

    Your commentary should be:
    - Structured and highlighted for clarity
    - Precise and fun, reflecting the seriousness of the game
    - Avoid player names and unnecessary details
    - Reflective of the match situation based on the provided data

    Key Points for Commentary:
    - **If overs are few and the required run rate is high:** Describe the pressure on bowlers and batsmen, and the intensity of the match.
    - **If runs are easily gettable and the batting team is scoring quickly:** Provide innovative and enjoyable comments about the fast-paced game.
    - **If early wickets fall:** Highlight the significance of these wickets and their impact on the game.

    Always keep an eye on the prediction winner and incorporate it into your commentary. Consider all parameters and any external data provided.

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

    