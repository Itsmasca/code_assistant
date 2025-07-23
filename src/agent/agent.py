### Parameter
from langgraph.graph import END, StateGraph, START
from src.agent.state import GraphState
from src.service.LCEL_langchain import concatenated_content
from src.api.core.dependencies.container import Container
from src.api.core.decorators.service_error_handler import service_error_handler
# Max tries
max_iterations = 3
# Reflect
# flag = 'reflect'
flag = "do not reflect"

### Nodes
@service_error_handler(module="code.generation.error")
async def generate(state: GraphState):
    """
    Generate a code solution

    Args:
        state (dict): The current graph state

        
    Returns:
        state (dict): New key added to state, generation
    """

    print("---GENERATING CODE SOLUTION---")

    # State
    messages = state["messages"]
    iterations = state["iterations"]
    error = state["error"]
    agent_name = state["agentName"]
    improved_prompt = state["improvedPrompt"]
    agent_json = state["agentJson"]
    input = state["input"]

    # We have been routed back to generation with an error
    if error == "yes":
        messages += [
            (
                "user",
                "Now, try again. Invoke the code tool to structure the output with a prefix, imports, and code block:",
            )
        ]
    Llmservice = Container.resolve("llm_service")
    code_gen_chain = await Llmservice.retrieve_chain(state)
    # Solution
    code_solution = await code_gen_chain.ainvoke(
        {"context": concatenated_content, 
         "agentName": agent_name,
         "improvedPrompt": improved_prompt,
         "agentJson": agent_json,
         "messages": messages,
         "input": input,
         "agentId": "test"
         }
    )
    print("=== CODE SOLUTION GENERATED ===")
    print("Prefix:", getattr(code_solution, "prefix", ""))
    print("Imports:", getattr(code_solution, "imports", ""))
    print("Code:\n", getattr(code_solution, "code", ""))
    print("================================")
    messages += [
        (
            "assistant",
            f"{code_solution.prefix} \n Imports: {code_solution.imports} \n Code: {code_solution.code}",
        )
    ]

    # Increment
    iterations = iterations + 1
    return {"generation": code_solution, "messages": messages, "iterations": iterations}
@service_error_handler(module="code.check.error")
def code_check(state: GraphState):
    """
    Check code

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, error
    """

    print("---CHECKING CODE---")

    # State
    messages = state["messages"]
    code_solution = state["generation"]
    iterations = state["iterations"]

    # Get solution components
    imports = code_solution.imports
    code = code_solution.code

    # Check imports
    try:
        check_code = Container.resolve("check_code_service")
        check_code(imports, "")
    except Exception as e:
        print("---TS COMPILATION FAILED---")
        messages.append(("user", f"TypeScript error: {e}"))
        return {
            **state,
            "messages": messages,
            "error": "yes",
        }
    # Check code
    try:
        check_code = Container.resolve("check_code_service")
        check_code(imports, code)
    except Exception as e:
        print("---TS COMPILATION FAILED---")
        messages.append(("user", f"TypeScript error: {e}"))
        return {
            **state,
            "messages": messages,
            "error": "yes",
        }
    # No errors
    print("---NO CODE TEST FAILURES---")
    return {
        "generation": code_solution,
        "messages": messages,
        "iterations": iterations,
        "error": "no",
    }


@service_error_handler(module="code.reflect.error")
async def reflect(state: GraphState):
    """
    Reflect on errors

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, generation
    """

    print("---GENERATING CODE SOLUTION---")

    # State
    messages = state["messages"]
    iterations = state["iterations"]
    code_solution = state["generation"]

    # Prompt reflection

    # Add reflection
    Llmservice = Container.resolve("llm_service")
    code_gen_chain = await Llmservice.retrieve_chain(state) 
    reflections = await code_gen_chain.ainvoke(
        {"context": concatenated_content, 
         "agnetName": state["agentName"],
         "improvedPrompt": state["improvedPrompt"],
         "agentJson": state["agentJson"],
         "messages": messages,
         "input": state["input"],
         "agentId": "test"
         }
    )
    messages += [("assistant", f"Here are reflections on the error: {reflections}")]
    return {"generation": code_solution, "messages": messages, "iterations": iterations}



### Edges
@service_error_handler(module="code.decision.error")
def decide_to_finish(state: GraphState):
    """
    Determines whether to finish.

    Args:
        state (dict): The current graph state

    Returns:
        str: Next node to call
    """
    error = state["error"]
    iterations = state["iterations"]

    if error == "no" or iterations == max_iterations:
        print("---DECISION: FINISH---")
        return "end"
    else:
        print("---DECISION: RE-TRY SOLUTION---")
        if flag == "reflect":
            return "reflect"
        else:
            return "generate"
@service_error_handler(module="code.graph.create.error")        
def create_graph():
    """
    Creates the graph for code generation.
    
    Returns:
        StateGraph: The generated state graph.
    """
    workflow = StateGraph(GraphState)

    # Define the nodes
    workflow.add_node("generate", generate)  # generation solution
    workflow.add_node("check_code", code_check)  # check code
    workflow.add_node("reflect", reflect)  # reflect

    # Build graph
    workflow.add_edge(START, "generate")
    workflow.add_edge("generate", "check_code")
    workflow.add_conditional_edges(
        "check_code",
        decide_to_finish,
        {
            "end": END,
            "reflect": "reflect",
            "generate": "generate",
        },
    )
    workflow.add_edge("reflect", "generate")
    app = workflow.compile()
    return app  