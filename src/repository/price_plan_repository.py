import json
from ..domain.price_plan import PricePlan


class PricePlanRepository:
    def __init__(self):
        self.price_plans = []

    def store(self, new_price_plans):
        self.price_plans += new_price_plans

    def get(self):
        return self.price_plans.copy()

    def clear(self):
        self.price_plans = []

    def get_price_plan(self, name):
        return next((price_plan for price_plan in self.price_plans if price_plan.name == name), None)

    def store_peak_multipliers(self, name, peak_time_multipliers):

        # Get price plan
        price_plan = self.get_price_plan(name)

        # Create hash table to find the position in the list is a given day of the week
        idx = {}
        for i in range(len(price_plan.peak_time_multipliers)):
            peak_time_multiplier = price_plan.peak_time_multipliers[i]
            idx[peak_time_multiplier.day_of_week] = i

        # Create hash table to store the multiplier for a given day of the week
        to_update = {}
        for peak_time_multiplier in peak_time_multipliers:
            to_update[peak_time_multiplier.day_of_week] = peak_time_multiplier.multiplier

        # Upsert
        for day_of_week in range(7):

            # Update current day of the week with new multiplier
            if day_of_week in idx and day_of_week in to_update:
                index = idx[day_of_week]
                multiplier = to_update[day_of_week]
                price_plan.peak_time_multipliers[index].multiplier = multiplier

            # Insert new multiplier
            elif day_of_week in to_update:
                price_plan.peak_time_multipliers.append(
                    PricePlan.PeakTimeMultiplier(day_of_week, to_update[day_of_week])
                )

        return price_plan


price_plan_repository = PricePlanRepository()
