from dataclasses import dataclass


@dataclass
class Employee:
    employee_id: str
    name: str
    basic_pay: float
    allowances: float
    overtime_hours: float
    overtime_rate: float
    incentives: float


# Example progressive income tax brackets: (income up to, rate).
# Replace these rates and limits with your organization's policy.
TAX_BRACKETS = [
    (30_000, 0.05),      # First 30,000 at 5%
    (60_000, 0.10),      # Next 30,000 at 10%
    (float("inf"), 0.20) # Remaining income at 20%
]


def progressive_deduction(amount: float, brackets: list[tuple[float, float]]) -> float:
    """Calculate a progressive deduction on amount using marginal brackets."""
    if amount < 0:
        raise ValueError("Deduction base cannot be negative.")

    deduction = 0.0
    previous_limit = 0.0

    for upper_limit, rate in brackets:
        if not 0 <= rate <= 1:
            raise ValueError("Each deduction rate must be between 0 and 1.")

        taxable_in_bracket = min(amount, upper_limit) - previous_limit
        if taxable_in_bracket > 0:
            deduction += taxable_in_bracket * rate

        if amount <= upper_limit:
            break
        previous_limit = upper_limit

    return deduction


def create_salary_statement(employee: Employee) -> dict:
    if not employee.employee_id.strip() or not employee.name.strip():
        raise ValueError("Employee ID and name are required.")

    earnings = [
        employee.basic_pay,
        employee.allowances,
        employee.overtime_hours,
        employee.overtime_rate,
        employee.incentives,
    ]
    if any(value < 0 for value in earnings):
        raise ValueError("Pay, hours, rates, and incentives cannot be negative.")

    overtime_pay = employee.overtime_hours * employee.overtime_rate
    gross_salary = (
        employee.basic_pay
        + employee.allowances
        + overtime_pay
        + employee.incentives
    )
    deductions = progressive_deduction(gross_salary, TAX_BRACKETS)
    net_salary = gross_salary - deductions

    return {
        "employee_id": employee.employee_id,
        "name": employee.name,
        "basic_pay": employee.basic_pay,
        "allowances": employee.allowances,
        "overtime_pay": overtime_pay,
        "incentives": employee.incentives,
        "gross_salary": gross_salary,
        "deductions": deductions,
        "net_salary": net_salary,
    }


def print_salary_statement(statement: dict) -> None:
    print("=" * 44)
    print("              SALARY STATEMENT")
    print("=" * 44)
    print(f'Employee ID       : {statement["employee_id"]}')
    print(f'Employee Name     : {statement["name"]}')
    print("-" * 44)
    print(f'Basic Pay         : {statement["basic_pay"]:>12,.2f}')
    print(f'Allowances        : {statement["allowances"]:>12,.2f}')
    print(f'Overtime Pay      : {statement["overtime_pay"]:>12,.2f}')
    print(f'Incentives        : {statement["incentives"]:>12,.2f}')
    print("-" * 44)
    print(f'Gross Salary      : {statement["gross_salary"]:>12,.2f}')
    print(f'Deductions        : {statement["deductions"]:>12,.2f}')
    print(f'Net Salary        : {statement["net_salary"]:>12,.2f}')
    print("=" * 44)


if __name__ == "__main__":
    employee = Employee(
        employee_id="E1001",
        name="Asha Kumar",
        basic_pay=40_000,
        allowances=8_000,
        overtime_hours=10,
        overtime_rate=300,
        incentives=2_500,
    )

    statement = create_salary_statement(employee)
    print_salary_statement(statement)