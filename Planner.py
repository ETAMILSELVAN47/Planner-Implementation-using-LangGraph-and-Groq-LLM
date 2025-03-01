import os
from dotenv import load_dotenv
load_dotenv()

from langchain_core.messages import SystemMessage,HumanMessage,AIMessage

from pydantic import BaseModel,Field
from typing import List


from typing_extensions import TypedDict
from typing import Annotated
import operator

from langgraph.constants import Send

from langgraph.graph import StateGraph,START,END
from langgraph.checkpoint.memory import MemorySaver
from IPython.display import Image,display


os.environ['GROQ_API_KEY']=os.getenv(key='GROQ_API_KEY')

from langchain_groq import ChatGroq
llm=ChatGroq(model='qwen-2.5-32b')
llm.invoke('Hello').content



class Task(BaseModel):
    name:str=Field(description='Name of the task')
    description:str=Field(description='Description of the task')

class Tasks(BaseModel):
    tasks:List[Task]=Field(description='List of tasks')    


#graph state
class State(TypedDict):
    user_input:str
    tasks:List[Task]
    completed_tasks:Annotated[list,operator.add]
    final_plan:str

class WorkerState(TypedDict):
    task:Task
    completed_tasks:Annotated[list,operator.add]    



def planner(state: State):
    """Generates a plan for the tour."""
    # Safely retrieve user input
    user_input = state.get('user_input', '')

    # Configure the LLM to output in the Tasks structure
    planner_llm = llm.with_structured_output(Tasks)

    # Invoke the LLM with the system and human messages
    response = planner_llm.invoke([
        SystemMessage(content='Generate a plan based on the user input'),
        HumanMessage(content=f"Here is the user input: {user_input}")
    ])

    # Return the response containing the plan
    return {'tasks':response.tasks}


def worker(state:WorkerState):
    """Works on an assigned task and returns the completed task response."""
    task=state.get('task',None)
    # Invoke LLM to process the assigned task
    response = llm.invoke([
        SystemMessage(content="Provide the below task name and description and work accordingly. Include no preamble for each section. Use markdown formatting."),
        HumanMessage(content=f"Here is the task name: {task.name} and description: {task.description}")
    ])

    return {'completed_tasks':[response.content]}


def synthesizer(state:State):
    """Combines all worker outputs into a final tour plan."""
    
    completed_tasks=state.get('completed_tasks')
    
     # Join completed tasks into a structured plan
    completed_task_plan = "\n\n---\n\n".join(completed_tasks) if completed_tasks else "No tasks completed."

    return {"final_plan": completed_task_plan}

def assign_workers(state:State):
    ''' Assign a task to each worker'''
    return [Send("Worker",{"task":s}) for s in state['tasks']]



# Build the Workflow
builder=StateGraph(State)

# Define the nodes
builder.add_node("Planner",planner)
builder.add_node("Worker",worker)
builder.add_node('Synthesizer',synthesizer)


# Define the edges
builder.add_edge(START,"Planner")
builder.add_conditional_edges("Planner",assign_workers,["Worker"])
builder.add_edge("Worker","Synthesizer")
builder.add_edge("Synthesizer",END)

memory=MemorySaver()
planner=builder.compile(checkpointer=memory)
