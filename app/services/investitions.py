from datetime import datetime

from app.models.base import InvestitionBase


def invest_donation(
    target: InvestitionBase,
    sources: list[InvestitionBase],
) -> list[InvestitionBase]:
    for source in sources:
        to_invest = min(
            (source.full_amount - source.invested_amount),
            (target.full_amount - target.invested_amount)
        )

        for obj in [source, target]:
            obj.invested_amount += to_invest

            if obj.invested_amount == obj.full_amount:
                obj.fully_invested = True
                obj.close_date = datetime.utcnow()

    return sources
