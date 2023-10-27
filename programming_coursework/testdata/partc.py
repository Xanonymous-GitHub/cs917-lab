from typing import Final

strategy_test_data: Final[tuple[dict[str, ...], ...]] = (
    dict(
        start_date='01/05/2017',
        end_date='12/06/2017',
        buy_list=['01/06/2017'],
        sell_list=['28/05/2017']
    ),
    dict(
        start_date='05/09/2018',
        end_date='27/09/2018',
        buy_list=['15/09/2018', '21/09/2018'],
        sell_list=['06/09/2018', '19/09/2018', '27/09/2018']
    ),
    dict(
        start_date='03/11/2019',
        end_date='14/11/2019',
        buy_list=['06/11/2019'],
        sell_list=['04/11/2019', '08/11/2019']
    ),
)
