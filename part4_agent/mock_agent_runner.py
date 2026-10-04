import sys
import os
import json
import csv

# --- IMPORTANT PATH FIX ---
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from part2_engine.growth_engine import mom_growth, is_flagged, validate_feed

def load_monthly_revenue(csv_path, target_month=None):
    """Helper to load a Part 1 CSV into a dictionary, optionally filtering by month."""
    data = {}
    if not os.path.exists(csv_path):
        return data
    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # If a target month is specified, skip rows that don't match
            if target_month and row.get('month', '').strip() != target_month:
                continue
                
            cat = row.get('category', '').strip()
            rev = row.get('revenue', '').strip()
            orders = row.get('n_orders', '').strip()
            
            if cat and rev:
                data[cat] = {
                    'revenue': float(rev),
                    'n_orders': int(''.join(filter(str.isdigit, orders))) if orders else 0
                }
    return data

def run(month: str, previous_month: str, previous_month_csv: str, current_month_csv: str) -> dict:
    """Executes the mock agent pipeline."""
    
    is_valid, errors = validate_feed(current_month_csv)
    
    if not is_valid:
        return {
            "run_month": month,
            "validation_status": "invalid",
            "validation_errors": errors,
            "flagged_categories": [],
            "suppressed_categories": [],
            "escalated_categories": [],
            "action_taken": "hard_stop"
        }
    
    # Load the specific months from the combined CSV
    current_data = load_monthly_revenue(current_month_csv, target_month=month)
    previous_data = load_monthly_revenue(previous_month_csv, target_month=previous_month)
    
    flagged = []
    escalated = []
    
    for category, curr_stats in current_data.items():
        if category in previous_data:
            prev_rev = previous_data[category]['revenue']
            curr_rev = curr_stats['revenue']
            
            mom_pct = mom_growth(prev_rev, curr_rev)
            flag_status = is_flagged(mom_pct)
            
            if flag_status == "flagged":
                flagged.append({
                    "category": category,
                    "mom_pct": mom_pct,
                    "previous_revenue": prev_rev,
                    "current_revenue": curr_rev,
                    "drafted": False,
                    "message": None
                })
            elif flag_status == "escalate_exact_boundary":
                escalated.append(category)
    
    flagged.sort(key=lambda x: abs(x['mom_pct']), reverse=True)
    
    drafted_categories = []
    suppressed_categories = []
    
    for i, item in enumerate(flagged):
        if i < 3: 
            message = (
                f"Context: Month-on-month performance for {item['category']} in {month}. "
                f"Insight: Fact - Revenue moved {item['mom_pct']}%, from {item['previous_revenue']} to {item['current_revenue']}. "
                f"Implication: Hypothesis - Review this category for potential causes."
            )
            item['drafted'] = True
            item['message'] = message
            drafted_categories.append(item)
        else: 
            suppressed_categories.append(item['category'])
            
    return {
        "run_month": month,
        "validation_status": "valid",
        "validation_errors": [],
        "flagged_categories": drafted_categories,
        "suppressed_categories": suppressed_categories,
        "escalated_categories": escalated,
        "action_taken": "drafted_and_held_for_approval"
    }

if __name__ == "__main__":
    print("--- Running Scenario: May vs April ---")
    # Now we explicitly tell the runner which months to compare!
    result = run(
        month="May",
        previous_month="April",
        previous_month_csv="part2_engine/fixtures/monthly_category_revenue.csv", 
        current_month_csv="part2_engine/fixtures/monthly_category_revenue.csv"
    )
    print(json.dumps(result, indent=2))
    
    print("\n--- Running Scenario: Corrupted Feed (Hard Stop) ---")
    corrupted_result = run(
        month="July",
        previous_month="June",
        previous_month_csv="part2_engine/fixtures/monthly_category_revenue.csv",
        current_month_csv="part2_engine/fixtures/corrupted_feed.csv"
    )
    print(json.dumps(corrupted_result, indent=2))