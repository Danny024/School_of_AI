from agents.search_agent import run_search
from agents.summarize_agent import summarize_text
from agents.checker_agent import fact_check
from agents.report_agent import generate_report

def run_research_pipeline(topic: str):
    search_results = run_search(topic)
    summary = summarize_text(search_results)
    corrections = fact_check(summary)
    report = generate_report(summary, corrections)
    return {
        "search": search_results,
        "summary": summary,
        "corrections": corrections,
        "report": report
    }