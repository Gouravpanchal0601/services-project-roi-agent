import copy


class ROISpreadsheetEngine:

    def __init__(self, workbook_data):

        self.original_data = workbook_data

        self.scenario_data = copy.deepcopy(
            workbook_data
        )

        self.assumptions = {}

    def set_assumption(self, name, value):

        self.assumptions[name] = value

    def get_assumption(self, name):

        return self.assumptions.get(name)

    def calculate(self):

        results = {}

        # Example assumption
        talent_cost = self.assumptions.get(
            "current_talent_fte_cost"
        )

        if talent_cost is not None:

            results[
                "current_talent_fte_cost"
            ] = talent_cost

        return results

    def reset(self):

        self.scenario_data = copy.deepcopy(
            self.original_data
        )

        self.assumptions = {}