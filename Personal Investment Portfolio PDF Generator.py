import os
from fpdf import FPDF

print("WELCOME")
print("MUTUAL FUND CALCULATOR")


class PDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 12)  # Use core font helvetica
        self.cell(0, 10, 'Investment Plan Summary', border=0, new_x="LMARGIN", new_y="NEXT", align='C')

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)  # Use core font helvetica
        self.cell(0, 10, f'Page {self.page_no()}', border=0, align='C')

    def chapter_title(self, title):
        self.set_font('helvetica', 'B', 12)  # Use core font helvetica
        self.cell(0, 10, title, border=0, new_x="LMARGIN", new_y="NEXT", align='L')
        self.ln(5)

    def chapter_body(self, body):
        self.set_font('helvetica', '', 12)  # Use core font helvetica
        self.multi_cell(0, 10, body)
        self.ln()


def calculate_custom_plan(initial_amount, monthly_amount, rate, years, step_up_amount=None, step_up_percentage=None):
    rate /= 100
    total_amount = initial_amount
    n = 12

    investment_details = []

    for year in range(1, years + 1):
        yearly_contributions = 0
        for month in range(12):
            total_amount = total_amount * (1 + rate / n)
            total_amount += monthly_amount
            yearly_contributions += monthly_amount

        #  step-up amount  after each year
        if step_up_amount:
            monthly_amount += step_up_amount
        elif step_up_percentage:
            monthly_amount += monthly_amount * step_up_percentage / 100

        detail = f"After year {year}, the total amount is: {total_amount:.2f}, with a monthly investment of {monthly_amount:.2f}"
        investment_details.append(detail)

    return total_amount, investment_details


def create_pdf(investor_name, salary, percentage, amount, investment_details, total_amount, years, investment_type,
               investment_plan, monthly_investment, step_up_amount=None, step_up_percentage=None, mix_details=None):
    pdf = PDF()
    pdf.add_page()

    pdf.set_font('helvetica', 'B', 12)  # Use core font helvetica
    pdf.cell(0, 10, f"Investor Name: {investor_name}", border=0, new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 10, f"Annual Salary: INR{salary:.2f}", border=0, new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 10, f"Investment Type: {investment_type}", border=0, new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 10, f"Investment Plan: {investment_plan}", border=0, new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 10, f"Monthly Investment: INR{monthly_investment:.2f}", border=0, new_x="LMARGIN", new_y="NEXT")

    if percentage:
        pdf.cell(0, 10, f"Investing Percentage of Salary: {percentage}%", border=0, new_x="LMARGIN", new_y="NEXT")
    if amount:
        pdf.cell(0, 10, f"Investing Fixed Amount: INR{amount:.2f}", border=0, new_x="LMARGIN", new_y="NEXT")

    if step_up_amount is not None:
        pdf.cell(0, 10, f"Step-up Amount: INR{step_up_amount:.2f}", border=0, new_x="LMARGIN", new_y="NEXT")
    if step_up_percentage is not None:
        pdf.cell(0, 10, f"Step-up Percentage: {step_up_percentage}%", border=0, new_x="LMARGIN", new_y="NEXT")

    pdf.ln(10)
    pdf.chapter_title("Investment Plan Details:")
    for detail in investment_details:
        pdf.chapter_body(detail)

    if mix_details:
        pdf.ln(10)
        pdf.chapter_title("Mix Investment Details:")
        for detail in mix_details:
            pdf.chapter_body(detail)

    pdf.ln(10)
    pdf.cell(0, 10, f"Total Amount after {years} years: INR{total_amount:.2f}", border=0, new_x="LMARGIN", new_y="NEXT")

    #Directory
    directory = "C:/Users/laksh/Desktop/Python PDF"
    pdf_file = os.path.join(directory, f"{investor_name}_investment_plan.pdf")


    os.makedirs(directory, exist_ok=True)

    pdf.output(pdf_file)
    print(f"Investment plan saved as {pdf_file}")


while True:
    print("\n---Choose in which you want to invest---")
    print("1. NIFTY50")
    print("2. SMALLCAP")
    print("3. MIDCAP")
    print("4. PSU Fund")
    print("5. MIX OF NIFTY50, MIDCAP, SMALLCAP")

    choice = input("Enter your choice (1-5): ")

    investment_type = None
    mix_details = None
    investment_details = []
    total_amount = 0
    monthly_investment = 0
    step_up_amount = None
    step_up_percentage = None

    if choice in ["1", "2", "3", "4"]:
        invest_type = input(
            "Do you want a one-time investment, SIP, or YIP (Yearly Increment plan)? (one-time/sip/YIP): ").strip().lower()

        investor_name = input("Enter investor name: ")
        salary = float(input("Enter annual salary: "))
        percentage = None
        amount = None

        if invest_type == "yip":
            invest_from_salary = input("Do you want to invest a percentage of your salary? (yes/no): ").strip().lower()
            if invest_from_salary == "yes":
                percentage = float(input("Enter the percentage of salary to invest: "))
                amount = (percentage / 100) * salary / 12  # Monthly amount from salary
            else:
                amount = float(input("Enter the monthly investment amount: "))

            b = float(input("Enter the annual rate (in %): "))
            c = int(input("Enter the time in years: "))
            step_up_type = input(
                "Do you want to step-up by a fixed amount or percentage? (amount/percentage/none): ").strip().lower()

            if step_up_type == "amount":
                step_up_amount = float(input("Enter the step-up amount: "))
            elif step_up_type == "percentage":
                step_up_percentage = float(input("Enter the step-up percentage: "))

            total_amount, investment_details = calculate_custom_plan(amount, amount, b, c, step_up_amount,
                                                                     step_up_percentage)
            monthly_investment = amount
            investment_type = {
                "1": "NIFTY50",
                "2": "SMALLCAP",
                "3": "MIDCAP",
                "4": "PSU Fund",
            }[choice]

        else:
            invest_from_salary = input("Do you want to invest a percentage of your salary? (yes/no): ").strip().lower()
            if invest_from_salary == "yes":
                percentage = float(input("Enter the percentage of salary to invest: "))
                amount = (percentage / 100) * salary / 12
            else:
                amount = float(input("Enter the investment amount: "))
            b = float(input("Enter the annual rate (in %): ")) / 100
            c = int(input("Enter the time in years: "))
            compounding = input(
                "Enter the compounding frequency (annual, semi-annual, quarterly, monthly): ").strip().lower()

            if compounding == "annual":
                n = 1
            elif compounding == "semi-annual":
                n = 2
            elif compounding == "quarterly":
                n = 4
            elif compounding == "monthly":
                n = 12
            else:
                print("Invalid compounding frequency. Defaulting to annual.")
                n = 1

            total_amount = amount * (1 + b / n) ** (n * c)
            investment_details.append(f"After {c} years, the total amount is: {total_amount:.2f}")
            monthly_investment = amount
            investment_type = {
                "1": "NIFTY50",
                "2": "SMALLCAP",
                "3": "MIDCAP",
                "4": "PSU Fund",
            }[choice]

    elif choice == "5":
        investor_name = input("Enter investor name: ")
        salary = float(input("Enter annual salary: "))

        a = float(input("Enter the investment amount in NIFTY50: "))
        a1 = float(input("Enter the investment amount in MIDCAP: "))
        a2 = float(input("Enter the investment amount in SMALLCAP: "))
        b = float(input("Enter the annual rate of NIFTY50 (in %): ")) / 100
        b1 = float(input("Enter the annual rate of MIDCAP (in %): ")) / 100
        b2 = float(input("Enter the annual rate of SMALLCAP (in %): ")) / 100
        c = int(input("Enter the time in years: "))
        compounding = input(
            "Enter the compounding frequency (annual, semi-annual, quarterly, monthly): ").strip().lower()

        if compounding == "annual":
            n = 1
        elif compounding == "semi-annual":
            n = 2
        elif compounding == "quarterly":
            n = 4
        elif compounding == "monthly":
            n = 12
        else:
            print("Invalid compounding frequency. Defaulting to annual.")
            n = 1

        d = a * (1 + b / n) ** (n * c)
        d1 = a1 * (1 + b1 / n) ** (n * c)
        d2 = a2 * (1 + b2 / n) ** (n * c)
        total_amount = d + d1 + d2

        mix_details = [
            f"NIFTY50: Initial Investment: INR{a}, Annual Rate: {b * 100:.2f}%, Total after {c} years: INR{d:.2f}",
            f"MIDCAP: Initial Investment: INR{a1}, Annual Rate: {b1 * 100:.2f}%, Total after {c} years: INR{d1:.2f}",
            f"SMALLCAP: Initial Investment: INR{a2}, Annual Rate: {b2 * 100:.2f}%, Total after {c} years: INR{d2:.2f}"
        ]
        investment_type = "Mix of NIFTY50, MIDCAP, SMALLCAP"
        monthly_investment = a + a1 + a2

    else:
        print("Invalid choice. Please try again.")
        continue

    create_pdf(investor_name, salary, percentage, amount, investment_details, total_amount, c, investment_type,
               invest_type if choice != "5" else "one-time", monthly_investment, step_up_amount, step_up_percentage,
               mix_details)

    print(f"The total amount would be INR{total_amount:.2f} in {c} years")

    another = input("Do you want to perform another calculation? (yes/no): ").strip().lower()

    if another != 'yes':
        break

print("Thank you for using the Mutual Fund Calculator!")


