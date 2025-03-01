# 🗺️ Tour Planner - AI-Powered Travel Itinerary Generator  

## 🚀 Overview  
The **Tour Planner** automates travel planning using **LangGraph** and **Groq's LLM**. It takes user input, generates a structured itinerary, executes travel-related tasks, and synthesizes the final tour plan.  

![image](https://github.com/user-attachments/assets/9dc52b0c-1137-4d6c-9743-ab391ce55688)


## 🏗️ System Architecture  
### 🔹 Components:  
1. **Planner Agent** - Breaks user input into travel-related tasks.  
2. **Worker Agent** - Processes and executes each travel task.  
3. **Synthesizer Agent** - Combines all processed tasks into a final itinerary.  
4. **LangGraph Workflow** - Manages execution flow between agents.  

## 🔧 Implementation Details  
- **Task Definitions**: Each task has a name, description, and completion tracking.  
- **Planner Function**: Generates a list of tasks from user input.  
- **Worker Function**: Completes assigned tasks based on predefined logic.  
- **Synthesizer Function**: Combines completed tasks into a structured itinerary.  

## ▶️ Running the Workflow  
1. **Install Dependencies**  
2. **Set API Key** (Groq LLM)  
3. **Run the Planner**  

## 🎯 Expected Output  
### ✅ Input:  
**"Plan a 5-day trip to Italy from Chennai from 22 March 2025 to 27 March 2025."**  

### ✅ Output:  
A well-structured travel itinerary with:  
- Day-wise activities  
- Travel & accommodation details  
- Key highlights  

## 🔮 Future Enhancements  
🔸 Multi-user collaboration  
🔸 Real-time flight & hotel booking APIs  
🔸 Custom tour packages  

---  

💡 **Contributors:** Tamilselvan
📌 **License:** MIT  

