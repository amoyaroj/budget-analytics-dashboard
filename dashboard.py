"""
Agustin Moya
IBE @ Purdue 

"""

import matplotlib.pyplot as plt
import seaborn as sns  #new library to enhance visualization 

#error_checking.py
def positive_float_input(prompt): 
    """
   turns input into a float, to handle decimals too, loops until a valid input 
   from the user is given, this being a positive value and a numerical one. 
   """
    while True: # infinite loop
        user_input = input(prompt) #string

        try:
            value = float(user_input) #tries to convert to float
            if value >= 0: 
                return value #worked!
            else: 
                print("yo! make sure you input a positive value!")
        
        except ValueError: #above failed (if user entered abc or *?%&° ) 
            print("yo! make sure you input a number!")

#UDF #1 Set Up Budget Preferences.  
def setup_budget():
    """
    ask the user for expected income, amount they want to allocate to 
    'savings', set the expected expenses in preset categories, check for errors too. 
    """
    print(" | - - - Setting Up Your Dynamic Budget: - - - |")
    
    #get the expected income and savings goal from the user: 
    expected_income = positive_float_input(
        "What's your monthly income?"
        )
    #get savings goal 
    savings_goal = positive_float_input(
        "How much do you want to save per month?"
        )
    
    #defining # of categories
    while True:
        try: 
            num_categories = int(input("How many categories do you want to track?"))
            if num_categories > 0: 
                break
            print("Please enter at least 1 category")
        except ValueError:
            print("Please enter a number")

    #names of each category
    custom_categories = []
    for i in range(num_categories): 
        cat_name = input(f" Enter name for category #{i+1}: ").strip()

        if not cat_name: 
            cat_name = f"Category {i+1}"
        custom_categories.append(cat_name)
    
    print("\nGreat, now let's estimate your expenses.")
    
    # for loop to get each expense per category

    expenses_by_category = {}

    for category in custom_categories:
        prompt = f" - Estimated cost of {category}: $" 
        amount = positive_float_input(prompt)       
        expenses_by_category[category] = amount     

    print("Preferences input sucessful!")
    return expected_income, savings_goal, expenses_by_category 

#UDF #2 Budget Calculations: 
def calculate_budget(expected_income, expenses_by_category, savings_goal):
    """
    this calculates the total expenses and calculates expected savings. 
    """
    print("\nCalculating Our Budget:")
    
    #calculating total expected expense: 
    total_expenses = 0
    expense_values = list(expenses_by_category.values())# turn dictionary values into a list to iterate over them, values is used to just get numbers not names
    for cost in expense_values: 
        total_expenses = total_expenses + cost 
    
    # Calculate expected savings: 
    projected_savings = expected_income - total_expenses
    
    #compares projected savings from prefered saving goal: 
    diff_savings_goal = projected_savings - savings_goal

    print("Calculations Successful!")

    return total_expenses, projected_savings, diff_savings_goal

def display_dashboard(expected_income, savings_goal, expenses_by_category, total_expenses, projected_savings, diff_savings_goal):
    """
    Displays the complete budget dashboard with dynamic category analysis and 
    auto-scaling visualizations.
    """
    print("\n | - - - Monthly Budget Report: - - - |")

    # Highest Spending Category Analysis
    if expenses_by_category:
        exclude_rent = 'Rent'
        highest_amount = 0
        highest_category = "None"

        for category, amount in expenses_by_category.items():
            if category.lower() == exclude_rent.lower():
                continue 
            if amount > highest_amount:
                highest_amount = amount
                highest_category = category

    # generating colors for the whole dashboard 
    num_cats = len(expenses_by_category)
    mako_palette = sns.color_palette('mako', n_colors=num_cats) 
    bg_color = mako_palette[1] #dark blue
    text_color = "white"

    # summary board
    status = "Goal met!" if diff_savings_goal >= 0 else "Goal Deficit!"
    
    report_text = (
        f"FINANCIAL SUMMARY\n"
        
        f"Income:    ${expected_income:>10,.2f}\n"
        f"Expenses:  ${total_expenses:>10,.2f}\n"
        f"Savings:   ${projected_savings:>10,.2f}\n"
        
        f"Goal:      ${savings_goal:>10,.2f}\n"
        f"Status:    {status:>10}\n"
        f"Diff:      ${abs(diff_savings_goal):>10,.2f}"
    )

    # Creating visuals 
    plt.figure(figsize=(16, 7), facecolor='#f0f0f0') # Light grey background for the whole window

    # Insights Card
    ax1 = plt.subplot(1, 3, 1)
    plt.axis('off')
    
    
    plt.text(0.5, 0.5, report_text, 
             fontsize=13, 
             color=text_color,
             weight='bold',
             family='Avenir',
             ha='center', va='center',
             bbox=dict(boxstyle="round,pad=1.5", 
                       facecolor=bg_color, 
                       edgecolor='none', 
                       alpha=0.9)) 
    
    plt.title("Insights", fontsize=15, fontweight='bold', pad=20)

    # pie chart 
    plt.subplot(1, 3, 2)
    labels_list = list(expenses_by_category.keys())
    values_list = list(expenses_by_category.values())
    plt.pie(values_list, labels=labels_list, colors=mako_palette[1:], 
            autopct='%1.1f%%', startangle=140, shadow=True,
            textprops={'fontweight': 'bold'})
    plt.title('Expense Distribution', fontsize=15, fontweight='bold')

    # bar chart 
    plt.subplot(1, 3, 3)
    sns.barplot(x=labels_list, y=values_list, palette="mako", hue=labels_list, legend=False)
    plt.title('Cost Comparison', fontsize=15, fontweight='bold')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.6) 

    plt.tight_layout()
    plt.show()


# Main function 
def main():
    
    # call udf 1 to get these 3 inputs 
    expected_income, savings_goal, expenses_by_category = setup_budget()
    
    # call udf 2 to perform calculations, passing the inputs we just got into this function
    total_expenses, projected_savings, diff_savings_goal = calculate_budget(
        expected_income, 
        expenses_by_category, 
        savings_goal
    )
    
    # call udf 3 to display dashboard, passing data to the final display function
    display_dashboard(
        expected_income, 
        savings_goal, 
        expenses_by_category, 
        total_expenses, 
        projected_savings, 
        diff_savings_goal
    )

if __name__ == "__main__":
    main()



