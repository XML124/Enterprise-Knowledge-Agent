from typing import TypedDict
from langgraph.graph import StateGraph, END
from app.agent.tools import search_documents
from app.providers.llm import get_answer_provider

class AgentState(TypedDict, total=False):
    question: str
    retrieved: list[dict]
    answer: str
    sources: list[dict]

def retrieve_node(state: AgentState):
    return {"retrieved": search_documents(state["question"], top_k=4)}

def answer_node(state: AgentState):
    results = state.get("retrieved", [])
    context = "\n\n".join(f"SOURCE={r['source']} CHUNK={r['chunk_index']}\n{r['content']}" for r in results)
    answer = get_answer_provider().answer(state["question"], context)
    sources = [{"source": r["source"], "chunk_index": r["chunk_index"]} for r in results[:2]]
    return {"answer": answer, "sources": sources}

def build_graph():
    g = StateGraph(AgentState)
    g.add_node("retrieve", retrieve_node)
    g.add_node("answer", answer_node)
    g.set_entry_point("retrieve")
    g.add_edge("retrieve", "answer")
    g.add_edge("answer", END)
    return g.compile()

agent_graph = build_graph()

def ask_agent(question: str) -> dict:
    r = agent_graph.invoke({"question": question})
    return {"answer": r.get("answer", ""), "sources": r.get("sources", [])}
