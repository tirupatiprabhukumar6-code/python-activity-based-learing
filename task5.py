from dataclasses import dataclass


@dataclass
class MobilePlan:
    name: str
    monthly_fee: float
    included_minutes: int
    included_data_gb: float
    included_sms: int
    validity_days: int
    extra_minute_rate: float
    extra_data_rate_per_gb: float
    extra_sms_rate: float


@dataclass
class Usage:
    minutes: int
    data_gb: float
    sms: int
    required_validity_days: int
    budget: float


def evaluate_plan(plan: MobilePlan, usage: Usage) -> dict:
    """Calculate total cost and eligibility for a plan."""
    numeric_values = [
        plan.monthly_fee, plan.included_minutes, plan.included_data_gb,
        plan.included_sms, plan.validity_days, plan.extra_minute_rate,
        plan.extra_data_rate_per_gb, plan.extra_sms_rate,
        usage.minutes, usage.data_gb, usage.sms,
        usage.required_validity_days, usage.budget,
    ]
    if any(value < 0 for value in numeric_values):
        raise ValueError("Plan details and usage cannot be negative.")

    extra_minutes = max(0, usage.minutes - plan.included_minutes)
    extra_data = max(0.0, usage.data_gb - plan.included_data_gb)
    extra_sms = max(0, usage.sms - plan.included_sms)

    excess_charge = (
        extra_minutes * plan.extra_minute_rate
        + extra_data * plan.extra_data_rate_per_gb
        + extra_sms * plan.extra_sms_rate
    )
    total_cost = plan.monthly_fee + excess_charge

    valid_for_period = plan.validity_days >= usage.required_validity_days
    within_budget = total_cost <= usage.budget

    return {
        "plan": plan.name,
        "base_fee": plan.monthly_fee,
        "excess_minutes": extra_minutes,
        "excess_data_gb": extra_data,
        "excess_sms": extra_sms,
        "excess_charge": excess_charge,
        "total_cost": total_cost,
        "validity_ok": valid_for_period,
        "within_budget": within_budget,
        "eligible": valid_for_period and within_budget,
    }


def find_best_plan(plans: list[MobilePlan], usage: Usage) -> tuple[dict | None, list[dict]]:
    evaluations = [evaluate_plan(plan, usage) for plan in plans]
    eligible = [result for result in evaluations if result["eligible"]]

    if not eligible:
        return None, evaluations

    # Lowest total cost wins; plan name breaks equal-cost ties.
    best = min(eligible, key=lambda result: (result["total_cost"], result["plan"]))
    return best, evaluations


if __name__ == "__main__":
    plans = [
        MobilePlan("Basic", 15, 300, 5, 100, 30, 0.10, 2.00, 0.05),
        MobilePlan("Plus", 25, 800, 15, 300, 30, 0.08, 1.50, 0.03),
        MobilePlan("Travel 60", 40, 1000, 20, 500, 60, 0.05, 1.00, 0.02),
    ]

    usage = Usage(
        minutes=650,
        data_gb=12,
        sms=250,
        required_validity_days=30,
        budget=35,
    )

    best, evaluations = find_best_plan(plans, usage)

    print("Plan comparison:")
    for result in evaluations:
        status = "Eligible" if result["eligible"] else "Not eligible"
        print(
            f'{result["plan"]}: total={result["total_cost"]:.2f}, '
            f'excess={result["excess_charge"]:.2f}, {status}'
        )

    if best:
        print(f'\nMost economical eligible plan: {best["plan"]}')
        print(f'Total cost: {best["total_cost"]:.2f}')
    else:
        print("\nNo plan meets both the validity and budget requirements.")