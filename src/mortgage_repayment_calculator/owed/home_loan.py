from typing_extensions import Self

from mortgage_repayment_calculator.account import Value
from mortgage_repayment_calculator.owed import Base
from mortgage_repayment_calculator.plan import Schedule


class HomeLoan(Base):
    def required_payment(self, schedule: Schedule, n_days: int) -> Value:
        return Value(
            self.starting_balance.total_cents
            / schedule.total_number_of_days
            * n_days
        )

    def make_scheduled_payment(
        self,
        schedule: Schedule,
        n_days: int = 1,
        extra_repayment: Value = None,
        flat: bool = False,
    ) -> Self:
        if extra_repayment is None:
            extra_repayment = Value(0)
        if schedule.days_left > 0:
            if not flat:
                return self.make_payment(
                    schedule.current_date,
                    Value(
                        self.balance.total_cents / schedule.days_left * n_days
                    )
                    + extra_repayment,
                )
            else:
                return self.make_payment(
                    schedule.current_date,
                    Value(
                        self.starting_balance.total_cents
                        / schedule.total_number_of_days
                        * n_days
                    )
                    + extra_repayment,
                )
        return self
