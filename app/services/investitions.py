from datetime import datetime

from app.models.base import CharityDonationBase


def invest_donation(
    target: CharityDonationBase,
    sources: CharityDonationBase,
) -> tuple[CharityDonationBase, list]:
    target_invested = target.invested_amount or 0
    remaining_amount = target.full_amount - target_invested

    for source in sources:
        if remaining_amount <= 0:
            break
        source_invested = source.invested_amount or 0
        needed_amount = source.full_amount - source_invested
        to_invest = min(needed_amount, remaining_amount)

        source.invested_amount = source_invested + to_invest
        target.invested_amount = target_invested + to_invest
        remaining_amount -= to_invest
        if source.invested_amount == source.full_amount:
            source.fully_invested = True
            source.close_date = datetime.utcnow()

    if target.invested_amount == target.full_amount:
        target.fully_invested = True
        target.close_date = datetime.utcnow()

    return target, sources
