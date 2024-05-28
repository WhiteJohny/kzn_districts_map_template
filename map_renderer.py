import pandas as pd
from ipyleaflet import Map, Marker, Polygon, FullScreenControl, LegendControl
from ipywidgets import Layout


class MapRenderer:
    def __init__(self, district_data: pd.DataFrame, points_data: pd.DataFrame):
        self.__points_data = points_data
        self.__district_data = district_data

    def get_map(self) -> Map:
        legend = {}
        map = Map(
            center=(55.787893, 49.123328),
            zoom=12,
            layout=Layout(width='100%', height='800px')
        )

        for _, row in self.__district_data.iterrows():
            points = row['points'][2:-2]
            points = points.replace('(', '')
            points = [i for i in points.split('), ')]
            points = [i.split(', ') for i in points]
            polygon = Polygon(
                locations=points,
                color=row['color'],
                fill_color=row['color'],
            )
            map.add(polygon)

            center = row["center"]
            center = [float(i) for i in center[1:-1].split(', ')]
            marker = Marker(
                location=center,
                draggable=False,
                title=row['district'],
            )
            map.add(marker)

            legend[row['district']] = row['color']

        map.add(LegendControl(legend, title='Районы Казани', position='bottomleft'))
        map.add(FullScreenControl())

        return map
