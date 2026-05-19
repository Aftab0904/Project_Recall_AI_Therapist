import time
from typing import List, Dict, Any
from .schemas import Memory, MemoryType

class Evaluator:
    def calculate_extraction_coverage(self, extracted_count: int, expected_count: int = 6) -> Dict[str, Any]:
        coverage = (extracted_count / expected_count) if expected_count > 0 else 0
        return {
            "expected": expected_count,
            "extracted": extracted_count,
            "score": coverage * 100
        }

    def calculate_retrieval_recall(self, retriever: Any, memories: List[Memory]) -> Dict[str, Any]:
        test_cases = [
            {
                "query": "How can I improve my work-life balance?",
                "expected_keywords": ["work", "life", "boundaries", "separation"]
            },
            {
                "query": "I keep waking up at 4 AM",
                "expected_keywords": ["sleep", "rumination", "4 am", "work conversations"]
            },
            {
                "query": "How should I talk to my sister?",
                "expected_keywords": ["sister", "family", "boundary", "boundary goal"]
            }
        ]
        
        passed = 0
        results = []
        for case in test_cases:
            top_3 = retriever.retrieve_memories(case["query"], memories, limit=3)
            # Check if any top memory contains any expected keyword in its summary
            found = False
            for r in top_3:
                summary_lower = r["summary"].lower()
                if any(kw in summary_lower for kw in case["expected_keywords"]):
                    found = True
                    break
            
            if found:
                passed += 1
            
            results.append({
                "query": case["query"],
                "top_retrieved": [r["summary"] for r in top_3],
                "pass": found
            })
            
        return {
            "total_tests": len(test_cases),
            "passed": passed,
            "score": (passed / len(test_cases)) * 100,
            "details": results
        }

    def calculate_human_recall_score(self, text: str, retrieved_summaries: List[str]) -> Dict[str, Any]:
        warm_terms = [
            "welcome back", "curious", "gently", "if you want", 
            "we can", "how has", "it sounds like"
        ]
        
        specificity_keywords = [
            "work", "meeting", "boundaries", "sleep", 
            "journaling", "sister", "walking", "manager", "personal time"
        ]
        
        text_lower = text.lower()
        
        warmth_pass = any(term in text_lower for term in warm_terms)
        
        # Specificity: check if it references keywords from the retrieved summaries
        # or general keywords
        specificity_pass = any(kw in text_lower for kw in specificity_keywords)
        
        score = 0.0
        if warmth_pass and specificity_pass:
            score = 1.0
        elif warmth_pass or specificity_pass:
            score = 0.5
            
        return {
            "warmth_pass": warmth_pass,
            "specificity_pass": specificity_pass,
            "score": score * 100
        }

    def calculate_safety_filter(self, retrieved_memories: List[Dict[str, Any]]) -> Dict[str, Any]:
        # High-sensitivity check: in this simple prototype, we check the metadata
        # or if the summary contains sensitive keywords not allowed in openers
        high_sens_count = 0
        push_violation_count = 0
        
        # For the demo, we'll check if any retrieved memory is marked as high sensitivity
        # (Assuming the retriever might have filtered them already, but we check again)
        # In this simple app, we'll just check if the summary contains 'crisis' or 'harm'
        for m in retrieved_memories:
            # This is a proxy for the actual safety check
            if "crisis" in m["summary"].lower() or "harm" in m["summary"].lower():
                high_sens_count += 1
                
        return {
            "high_sensitivity_used": high_sens_count,
            "push_violations": push_violation_count,
            "status": "Pass" if high_sens_count == 0 and push_violation_count == 0 else "Fail"
        }

    def get_latency_metrics(self, retrieval_ms: float, generation_ms: float) -> Dict[str, Any]:
        total = retrieval_ms + generation_ms
        return {
            "retrieval": retrieval_ms,
            "generation": generation_ms,
            "total": total,
            "status": "Pass" if total < 2000 else "Fail"
        }

evaluator = Evaluator()
