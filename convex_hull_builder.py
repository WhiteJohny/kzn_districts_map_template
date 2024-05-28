import pandas as pd


class ConvexHullBuilder:
    def __init__(self, points: pd.DataFrame):
        self.__points = points

    def get_convex_hull(self) -> pd.DataFrame:
        data = {
           "district": [],
           "points": [],
           "center": [],
           "color": ["red", "blue", "green", "yellow", "orange", "white", "black", "purple"]
        }
        districts = {}
        for district in self.__points["district"].unique():
            lats = self.__points[self.__points["district"] == district]['lat'].to_list()
            lons = self.__points[self.__points["district"] == district]['lon'].to_list()

            districts[district] = [(lats[i], lons[i]) for i in range(len(lons))]

            points = self.__grahamscan(districts[district])
            center = self.__center_finder(points)

            data["district"].append(district)
            data["points"].append(points)
            data["center"].append(center)

        df = pd.DataFrame(data)
        return df

    @staticmethod
    def __center_finder(points) -> tuple:
        n = len(points)
        lats_sum = lons_sum = 0
        for i in range(n):
            lats_sum += points[i][0]
            lons_sum += points[i][1]
        lat = lats_sum / n
        lon = lons_sum / n

        return lat, lon

    @staticmethod
    def __rotate(A, B, C) -> float:
        return (B[0] - A[0]) * (C[1] - B[1]) - (B[1] - A[1]) * (C[0] - B[0])

    def __grahamscan(self, points) -> list:

        n = len(points)
        points_id = [i for i in range(n)]

        for i in range(1, n):
            if points[points_id[i]][0] < points[points_id[0]][0]:
                points_id[i], points_id[0] = points_id[0], points_id[i]

        for i in range(2, n):
            j = i

            while j > 1 and (self.__rotate(points[points_id[0]], points[points_id[j - 1]], points[points_id[j]]) < 0):
                points_id[j], points_id[j - 1] = points_id[j - 1], points_id[j]
                j -= 1

        stack = [points_id[0], points_id[1]]
        for i in range(2, n):
            while self.__rotate(points[stack[-2]], points[stack[-1]], points[points_id[i]]) < 0:
                del stack[-1]
            stack.append(points_id[i])

        return [points[i] for i in stack]
