import matplotlib.pyplot as plt
import seaborn as sns

# 1. DATA INPUT & VALIDATION (Error Checking)
# =================================================================

def positive_float_input(prompt): 
    """
    Ensures data integrity by validating inputs as positive numerical values.
    """
    while True:
        user_input = input(prompt)
        try:
            value = float(user_input)
            if value >= 0: 
                return value
            else: 
                print("Error: Please input a positive value.")
        except ValueError:
            print("Error: Input must be a number.")

def setup_budget():
    """
    Initializes budget parameters including income, savings goals, and categories.
    """
    print(" | - - - Setting Up Your Dynamic Budget - - - |")
    expected_income = positive_float_input("Monthly Income: $")
    savings_goal = positive_float_input("Monthly Savings Goal: $")
    
    while True:
        try: 
            num_categories = int(input("How many categories do you want to track? "))
            if num_categories > 0: break
            print("Please enter at least 1 category.")
        except ValueError:
            print("Please enter a valid number.")

    expenses_by_category = {}
    for i in range(num_categories): 
        cat_name = input(f"Enter name for category #{i+1}: ").strip() or f"Category {i+1}"
        expenses_by_category[cat_name] = positive_float_input(f" - Estimated cost of {cat_name}: $")

    return expected_income, savings_goal, expenses_by_category 

# 2. BUDGET CALCULATIONS & ANALYSIS
# =================================================================

def calculate_budget(expected_income, expenses_by_category, savings_goal):
    """
    Performs core financial analysis to determine net savings and goal variances.
    """
    total_expenses = sum(expenses_by_category.values())
    projected_savings = expected_income - total_expenses
    diff_savings_goal = projected_savings - savings_goal

    return total_expenses, projected_savings, diff_savings_goal

# 3. VISUALIZATION DASHBOARD (Seaborn & Matplotlib)
# =================================================================

def display_dashboard(income, goal, expenses, total_exp, savings, diff):
    """
    Generates a professional 3-panel financial dashboard.
    """
    # Styling and Palette Setup
    num_cats = len(expenses)
    mako_palette = sns.color_palette('mako', n_colors=num_cats + 1)
    
    plt.figure(figsize=(16, 7), facecolor='#f0f0f0')

    # Panel 1: Financial Insights Summary
    ax1 = plt.subplot(1, 3, 1)
    plt.axis('off')
    status = "Goal Met!" if diff >= 0 else "Goal Deficit!"
    report_text = (
        f"FINANCIAL SUMMARY\n\n"
        f"Income:    ${income:>10,.2f}\n"
        f"Expenses:  ${total_exp:>10,.2f}\n"
        f"Savings:   ${savings:>10,.2f}\n"
        f"----------------------\n"
        f"Goal:      ${goal:>10,.2f}\n"
        f"Status:    {status:>10}\n"
        f"Diff:      ${abs(diff):>10,.2f}"
    )
    plt.text(0.5, 0.5, report_text, fontsize=13, weight='bold', family='sans-serif',
             ha='center', va='center', bbox=dict(boxstyle="round,pad=1.5", 
             facecolor=mako_palette[1], edgecolor='none', alpha=0.9, color='white'))
    plt.title("Financial Insights", fontsize=15, fontweight='bold', pad=20)

    # Panel 2: Expense Distribution (Pie)
    plt.subplot(1, 3, 2)
    plt.pie(expenses.values(), labels=expenses.keys(), colors=mako_palette[1:], 
            autopct='%1.1f%%', startangle=140, shadow=True, textprops={'fontweight': 'bold'})
    plt.title('Expense Distribution', fontsize=15, fontweight='bold')

    # Panel 3: Cost Comparison (Bar)
    plt.subplot(1, 3, 3)
    sns.barplot(x=list(expenses.keys()), y=list(expenses.values()), palette="mako")
    plt.title('Cost Comparison', fontsize=15, fontweight='bold')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    income, goal, expenses = setup_budget()
    total_exp, savings, diff = calculate_budget(income, expenses, goal)
    display_dashboard(income, goal, expenses, total_exp, savings, diff)
