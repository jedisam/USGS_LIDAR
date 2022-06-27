"""A set for transformation calculating TWI, standardization."""
import geopandas as gpd
import numpy as np
from scipy.interpolate import griddata
from shapely.geometry import Point
from matplotlib.tri import Triangulation, LinearTriInterpolator

from logger import Logger


class Transform:
    def __init__(self) -> None:
        """Initialize transform Class."""
        self.logger = Logger("transform.log").get_app_logger()
        self.logger.info("Successfully Instantiated Lidar Class Object")

    def neighbors(self, mat, row, col, radius=1):
        """Generate neigbors matrix for point.
        Args:
            mat (array): Matrix from which the neighbors will be extracted
            row (int): Row of the value for which we are fining the neighbors
            col (int): Col of of the value for which we are fining the neighbors    
            radius (int, optional): Radius of neighbors. Defaults to 1.
        Returns:
            [array]: Returns a matrix of the neighbors with the value of the requred index in the middle 
        """

        rows, cols = len(mat), len(mat[0])
        out = []
        self.logger.info("Generating neighbours matrix for each point.")
        for i in range(row - radius - 1, row + radius):
            row = []
            for j in range(col - radius - 1, col + radius):

                if 0 <= i < rows and 0 <= j < cols:
                    try:
                        row.append(mat[i][j])
                    except Exception as e:
                        print(e)

                else:
                    row.append(np.nan)

            out.append(row)

        return out

    def twi(self, matrix, res):
        """Generate TWI for Matrix
        Args:
            matrix (array): Array Containing our point and its neighbors
            res (int): Resolution of our matrix
        Returns:
            float: Return TWI for the center point of our matrix
        """
        self.logger.info("Generating TWI matrix.")
        if not np.isnan(np.sum(matrix)):
            mat = np.array(matrix)
            fx = (
                mat[2, 0] - mat[2, 2] + mat[1, 0] - mat[1, 2] + mat[0, 0] - mat[0, 2]
            ) / (6 * res)
            fy = (
                mat[0, 2] - mat[2, 2] + mat[0, 1] - mat[2, 1] + mat[0, 0] - mat[2, 0]
            ) / (6 * res)
            slope = ((fx ** 2) + (fy ** 2)) ** 0.5
            arr = np.array(matrix)
            contributingarea = len(arr[arr > arr[1, 1]]) * (res ** 2)
            if contributingarea == 0:
                return 0
            if abs(slope) == 0.0:
                return 0
            index = np.log(contributingarea / slope)

            return index
        else:
            return 0

    def topographic_wetness_index(self, data, resolution):
        """Calculate Topographic Wetness Index for elevations
            Args:
                data (GeoDataFRame): GeoDataFrame containing points and thier elevation
                resolution (int): Resolution of the generated TWI 
            Returns:
                GeoDataFrame: GeoDataFrame With a new Column For the index
            """

        data_meters = data.to_crs({"init": "epsg:3395"})

        rasterRes = resolution
        try:
            self.logger.info("Calculating twi for elevations.")
            points = [[i.x, i.y] for i in data_meters.geometry.values]
        except Exception as e:
            self.logger.error("Error calculating twi for elevations.")
            print(e)
            pass

        try:
            values = data_meters["elevation"].values

        except Exception as e:
            self.logger.error("Error calculating twi values.")
            print(e)

        xDim = round(data_meters.total_bounds[2]) - round(data_meters.total_bounds[0])
        yDim = round(data_meters.total_bounds[3]) - round(data_meters.total_bounds[1])
        # rasterRes = 0.5
        nCols = xDim // rasterRes
        nRows = yDim // rasterRes

        grid_y, grid_x = np.mgrid[
            round(data_meters.total_bounds[1])
            + rasterRes / 2 : round(data_meters.total_bounds[3])
            - rasterRes / 2 : nRows * 1j,
            round(data_meters.total_bounds[0])
            + rasterRes / 2 : round(data_meters.total_bounds[2])
            + rasterRes / 2 : nCols * 1j,
        ]
        mtop = griddata(points, values, (grid_x, grid_y), method="linear")
        slopes = []

        slopeMatrix = np.zeros([nRows, nCols])
        for indexX in range(0, nCols):
            for indexY in range(0, nRows):
                mat = self.neighbors(mtop, indexY + 1, indexX + 1)
                ind = self.twi(mat, rasterRes)
                slopeMatrix[indexY, indexX] = ind
                slopes.append(ind)

        x = grid_x.flatten()
        y = grid_y.flatten()
        geometry_points = [Point(x, y) for x, y in zip(x, y)]
        elevetions = mtop.flatten()
        g_df = gpd.GeoDataFrame(columns=["elevation", "geometry"])
        g_df["elevation"] = elevetions
        g_df["geometry"] = geometry_points
        g_df["twi"] = slopes
        g_df.set_geometry("geometry", inplace=True)
        g_df.set_crs("epsg:3395", inplace=True)
        self.logger.info("Calculated TWI.")

        return g_df.to_crs(data.crs)

    def standardize(self, data, resolution):
        """Standardize and interpolate dataframe
        Args:
            data (GeoDataFrame): Dataframe to be standardized
            resolution (int): Resolution of the standardization
        Returns:
            GeoDataFrame: Returns the interpolated and standardized dataframe
        """

        self.logger.info("Standardizing...")

        data_meters = data.to_crs({"init": "epsg:3395"})

        rasterRes = resolution

        totalPointsArray = np.zeros([data_meters.shape[0], 3])
        for index, point in data_meters.iterrows():
            pointArray = np.array(
                [
                    point.geometry.coords.xy[0][0],
                    point.geometry.coords.xy[1][0],
                    point["elevation"],
                ]
            )
            totalPointsArray[index] = pointArray
        xCoords = np.arange(
            totalPointsArray[:, 0].min(),
            totalPointsArray[:, 0].max() + rasterRes,
            rasterRes,
        )
        yCoords = np.arange(
            totalPointsArray[:, 1].min(),
            totalPointsArray[:, 1].max() + rasterRes,
            rasterRes,
        )
        zCoords = np.zeros([yCoords.shape[0], xCoords.shape[0]])
        polygons = []
        elevations = []

        self.logger.info("Grid Created Proceeding to interpolation")
        triFn = Triangulation(totalPointsArray[:, 0], totalPointsArray[:, 1])
        # linear triangule interpolator funtion
        linTriFn = LinearTriInterpolator(triFn, totalPointsArray[:, 2])
        # loop among each cell in the raster extension
        for indexX, x in np.ndenumerate(xCoords):
            for indexY, y in np.ndenumerate(yCoords):
                tempZ = linTriFn(x, y)
                # filtering masked values
                if tempZ == tempZ:
                    zCoords[indexY, indexX] = tempZ

                    polygons.append(Point(x, y))
                    elevations.append(float(tempZ.data[()]))
                else:
                    zCoords[indexY, indexX] = np.nan
        self.logger.info("Interploation Completed")
        frame = gpd.GeoDataFrame(columns=["elevation", "geometry"])
        frame["elevation"] = elevations
        frame["geometry"] = polygons
        frame.set_geometry("geometry", inplace=True)
        frame.set_crs(crs=data_meters.crs, inplace=True)

        self.logger.info("Successfully Standardized dataframe.")
        return frame.to_crs(data.crs)
