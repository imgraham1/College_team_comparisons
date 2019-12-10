import unittest
from final_project import *


class TestStringMethods(unittest.TestCase):

    def test_pictures(self):
        self.assertEqual(pictures["Team"][50],"Central Michigan")
        self.assertEqual(pictures["Team"][100],"Gardner-Webb")
        self.assertEqual(pictures["Team"][150],"Long Beach State")
        self.assertEqual(pictures["Team"][200],"New Mexico State")

    def test_locations(self):
        self.assertEqual(locations['lats'][60], 42.7355416)
        self.assertEqual(locations['lons'][60], -84.4852469)
        self.assertEqual(locations['state'][60], "Michigan")
        self.assertEqual(locations['abbr'][60], "MI")

        self.assertEqual(locations['lats'][119], 41.311367)
        self.assertEqual(locations['lons'][119], -105.59110100000001)
        self.assertEqual(locations['state'][119], "Wyoming")
        self.assertEqual(locations['abbr'][119], "WY")

    def test_totals(self):
        self.assertEqual(len(totals_df), 120)
        self.assertEqual(totals_df["Bball_drtg"][75], 204.2)
        self.assertEqual(totals_df["Fball_drtg"][15], 36.0)
        self.assertEqual(totals_df["Team"][56], "Memphis")
        self.assertEqual(totals_df["Recruiting"][111], "Football")

    def test_2019(self):
        self.assertEqual(len(df_2019), 119)
        self.assertEqual(df_2019["Bball_drtg"][75], "96")
        self.assertEqual(df_2019["Fball_drtg"][15], "48")
        self.assertEqual(df_2019["Team"][56], "Miami (FL)")
        self.assertEqual(df_2019["Recruiting"][111], "Football")

    def test_2018(self):
        self.assertEqual(len(df_2018), 119)
        self.assertEqual(df_2018["Bball_drtg"][75], "57")
        self.assertEqual(df_2018["Fball_drtg"][15], "24")
        self.assertEqual(df_2018["Team"][56], "Miami (FL)")
        self.assertEqual(df_2018["Recruiting"][111], "Basketball")

    def test_2017(self):
        self.assertEqual(len(df_2017), 119)
        self.assertEqual(df_2017["Bball_drtg"][75], "142")
        self.assertEqual(df_2017["Fball_drtg"][92], "35")
        self.assertEqual(df_2017["Team"][56], "Miami (FL)")
        self.assertEqual(df_2017["Recruiting"][111], "Basketball")

    def test_2016(self):
        self.assertEqual(len(df_2016), 118)
        self.assertEqual(df_2016["Bball_drtg"][75], "243")
        self.assertEqual(df_2016["Fball_drtg"][92], "120")
        self.assertEqual(df_2016["Team"][56], "Miami (OH)")
        self.assertEqual(df_2016["Recruiting"][111], "Football")

    def test_2015(self):
        self.assertEqual(len(df_2015), 118)
        self.assertEqual(df_2015["Bball_drtg"][75], "302")
        self.assertEqual(df_2015["Fball_drtg"][92], "90")
        self.assertEqual(df_2015["Team"][56], "Miami (OH)")
        self.assertEqual(df_2015["Recruiting"][111], "Football")


if __name__ == "__main__":
	unittest.main(verbosity=2)
