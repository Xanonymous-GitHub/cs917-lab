from typing import Final

next_average_test_data: Final[tuple[dict[str, ...], ...]] = (
    dict(
        start_date='04/05/2015',
        end_date='27/05/2015',
        next_average=237.72045957687828,
    ),
    dict(
        start_date='01/02/2016',
        end_date='28/02/2016',
        next_average=441.4238016565723,
    ),
    dict(
        start_date='08/12/2016',
        end_date='11/12/2016',
        next_average=778.1930137752934,
    ),
)

market_trend_test_data: Final[tuple[dict[str, ...], ...]] = (
    dict(
        start_date='04/05/2015',
        end_date='27/05/2015',
        classified_trend='other'
    ),
    dict(
        start_date='01/02/2016',
        end_date='28/02/2016',
        classified_trend='increasing'
    ),
    dict(
        start_date='08/12/2016',
        end_date='11/12/2016',
        classified_trend='increasing'
    ),
)
