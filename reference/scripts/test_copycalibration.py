import unittest

import copycalibration
import common


class TestCopyCalibration(unittest.TestCase):
    directory_lights=r"c:\lights"
    directory_darkslibrary=r"c:\darkslibrary"
    directory_calibration=r"c:\calibration"

    # set filename as it would be normally set.  use get_file_headers independently to easily manage headers

    data_mock_calibration = {
        r"c:\calibration\masterDark_SETTEMP_-10.00_EXPOSURE_60.00_GAIN_100_OFFSET_50.xisf": 
            common.get_file_headers("INSTRUME_AP26CC_TYPE_MASTER DARK_EXP_60.00_GAIN_100_OFFSET_50_SETTEMP_-10.00.xisf", profileFromPath=False),
        r"c:\calibration\masterDark_SETTEMP_-10.00_EXPOSURE_120.00_GAIN_100_OFFSET_50.xisf": 
            common.get_file_headers("INSTRUME_AP26CC_TYPE_MASTER DARK_EXP_120.00_GAIN_100_OFFSET_50_SETTEMP_-10.00.xisf", profileFromPath=False),
        r"c:\calibration\masterFlat_FILTER_F_INSTRUME_AP26CC_DATE_2023-12-12_SETTEMP_-10.00_GAIN_100_OFFSET_50.xisf": 
            common.get_file_headers("TELESCOP_R135_TYPE_MASTER FLAT_FILTER_F_INSTRUME_AP26CC_DATE_2023-12-12_SETTEMP_-10.00_GAIN_100_OFFSET_50.xisf", profileFromPath=False),
        r"c:\calibration\masterFlat_FILTER_F_INSTRUME_AP26CC_DATE_2023-12-12_SETTEMP_-10.00_GAIN_999_OFFSET_50.xisf": 
            common.get_file_headers("TELESCOP_R135_TYPE_MASTER FLAT_FILTER_F_INSTRUME_AP26CC_DATE_2023-12-12_SETTEMP_-10.00_GAIN_999_OFFSET_50.xisf", profileFromPath=False),
        r"c:\calibration\masterFlat_FILTER_X_INSTRUME_AP26CC_DATE_2023-12-12_SETTEMP_-10.00_GAIN_999_OFFSET_50_duplicate1.xisf": 
            common.get_file_headers("TELESCOP_R135_TYPE_MASTER FLAT_FILTER_X_INSTRUME_AP26CC_DATE_2023-12-12_SETTEMP_-10.00_GAIN_999_OFFSET_50.xisf", profileFromPath=False),
        r"c:\calibration\masterFlat_FILTER_X_INSTRUME_AP26CC_DATE_2023-12-12_SETTEMP_-10.00_GAIN_999_OFFSET_50_duplicate2s.xisf": 
            common.get_file_headers("TELESCOP_R135_TYPE_MASTER FLAT_FILTER_X_INSTRUME_AP26CC_DATE_2023-12-12_SETTEMP_-10.00_GAIN_999_OFFSET_50.xisf", profileFromPath=False),
    }

    data_mock_darkslibrary = {
        r"c:\darkslibrary\masterDark_SETTEMP_-10.00_EXPOSURE_60.00_GAIN_100_OFFSET_50.xisf": 
            common.get_file_headers("INSTRUME_AP26CC_TYPE_MASTER DARK_EXP_60.00_GAIN_100_OFFSET_50_SETTEMP_-10.00.xisf", profileFromPath=False),
        r"c:\darkslibrary\masterDark_SETTEMP_-10.00_EXPOSURE_120.00_GAIN_100_OFFSET_50.xisf": 
            common.get_file_headers("INSTRUME_AP26CC_TYPE_MASTER DARK_EXP_120.00_GAIN_100_OFFSET_50_SETTEMP_-10.00.xisf", profileFromPath=False),
    }
    
    data_mock_lights = {
        r"c:\lights\target1\accept\DATE_2023-12-12\FILTER_F_EXP_120.00_SETTEMP_-10.00\light1.fits":
            common.get_file_headers("c:\TELESCOP_R135_INSTRUME_AP26CC_GAIN_100_OFFSET_50\DATE_2023-12-12\FILTER_F_EXP_120.00_SETTEMP_-10.00", profileFromPath=False),
        r"c:\lights\target1\accept\DATE_2023-12-12\FILTER_F_EXP_120.00_SETTEMP_-10.00\light2.fits":
            common.get_file_headers("c:\TELESCOP_R135_INSTRUME_AP26CC_GAIN_100_OFFSET_50\DATE_2023-12-12\FILTER_F_EXP_120.00_SETTEMP_-10.00", profileFromPath=False),
        r"c:\lights\target2\accept\DATE_2023-12-12\FILTER_F_EXP_60.00_SETTEMP_-10.00\light1.fits":
            common.get_file_headers("c:\TELESCOP_R135_INSTRUME_AP26CC_GAIN_100_OFFSET_50\DATE_2023-12-12\FILTER_F_EXP_60.00_SETTEMP_-10.00", profileFromPath=False),
        r"c:\lights\targetMissingDarks1\accept\DATE_2023-12-12\FILTER_F_EXP_45.00_SETTEMP_-10.00\light1.fits":
            common.get_file_headers("c:\TELESCOP_R135_INSTRUME_AP26CC_GAIN_100_OFFSET_50\DATE_2023-12-12\FILTER_F_EXP_45.00_SETTEMP_-10.00", profileFromPath=False),
        r"c:\lights\targetMissingDarksFlats1\accept\DATE_2023-12-12\FILTER_X_EXP_45.00_SETTEMP_-10.00\light1.fits":
            common.get_file_headers("c:\TELESCOP_R135_INSTRUME_AP26CC_GAIN_100_OFFSET_50\DATE_2023-12-12\FILTER_X_EXP_45.00_SETTEMP_-10.00", profileFromPath=False),
    }

    data_mock_lights_duplicateFlats = {
        r"c:\lights\duplicateFlats\accept\DATE_2023-12-12\FILTER_X_EXP_120.00_SETTEMP_-10.00\light1.fits":
            common.get_file_headers("c:\TELESCOP_R135_INSTRUME_AP26CC_GAIN_999_OFFSET_50\DATE_2023-12-12\FILTER_X_EXP_120.00_SETTEMP_-10.00", profileFromPath=False),
    }

    def test_GetCopyList_calibration_to_darkslibrary(self):
        cc = copycalibration.CopyCalibration(
            src_bias_dir=None,
            src_flat_dir=None,
            src_dark_dir=self.directory_calibration,
            dest_bias_dir=None,
            dest_dark_dir=self.directory_darkslibrary,
            dest_flat_dir=None,
            dest_light_dir=None,
            debug=False,
            dryrun=True,
        )
        # cannot directly test GetCopyList_calibration_to_darkslibrary
        # rely on mocking data and calling utility funciton 
        copy_list = cc.GetCopyList_to_dest_dark()
        print(copy_list)
        self.assertIsNotNone(copy_list)
        self.assertEqual(len(copy_list), 2)
        self.assertEqual(copy_list[0][0], r"c:\calibration\masterDark_SETTEMP_-10.00_EXPOSURE_60.00_GAIN_100_OFFSET_50.xisf")
        self.assertEqual(copy_list[0][1], r"c:\darkslibrary\AP26CC\masterDark_EXPTIME_60.00_SETTEMP_-10.00_GAIN_100_OFFSET_50.xisf")
        self.assertEqual(copy_list[1][0], r"c:\calibration\masterDark_SETTEMP_-10.00_EXPOSURE_120.00_GAIN_100_OFFSET_50.xisf")
        self.assertEqual(copy_list[1][1], r"c:\darkslibrary\AP26CC\masterDark_EXPTIME_120.00_SETTEMP_-10.00_GAIN_100_OFFSET_50.xisf")

    def test_GetCopyList_darks_to_lights(self):
        cc = copycalibration.CopyCalibration(
            src_bias_dir=None,
            src_flat_dir=None,
            src_dark_dir=self.directory_darkslibrary,
            dest_bias_dir=None,
            dest_dark_dir=None,
            dest_flat_dir=None,
            dest_light_dir=self.directory_lights,
            debug=False,
            dryrun=True,
        )
        # cannot directly test GetCopyList_darks_to_lights
        # rely on mocking data and calling utility funciton 
        copy_list = cc.GetCopyList_darks_to_lights(required_properties=cc.darks_required_properties)
        
        # targetname will be stripped
        self.assertIsNotNone(copy_list)
        self.assertEqual(len(copy_list), 4)
        self.assertEqual(copy_list[0][0], r"c:\darkslibrary\masterDark_SETTEMP_-10.00_EXPOSURE_120.00_GAIN_100_OFFSET_50.xisf")
        self.assertEqual(copy_list[0][1], r"c:\lights\target1\accept\DATE_2023-12-12\masterDark_SETTEMP_-10.00_EXPOSURE_120.00_GAIN_100_OFFSET_50.xisf")
        self.assertEqual(copy_list[1][0], r"c:\darkslibrary\masterDark_SETTEMP_-10.00_EXPOSURE_60.00_GAIN_100_OFFSET_50.xisf")
        self.assertEqual(copy_list[1][1], r"c:\lights\target2\accept\DATE_2023-12-12\masterDark_SETTEMP_-10.00_EXPOSURE_60.00_GAIN_100_OFFSET_50.xisf")
        self.assertIsNone(copy_list[2][0])
        self.assertEqual(copy_list[2][1], r"c:\lights\targetMissingDarks1\accept\DATE_2023-12-12\FILTER_F_EXP_45.00_SETTEMP_-10.00")
        self.assertIsNone(copy_list[3][0])
        self.assertEqual(copy_list[3][1], r"c:\lights\targetMissingDarksFlats1\accept\DATE_2023-12-12\FILTER_X_EXP_45.00_SETTEMP_-10.00")

    def test_GetCopyList_flats_to_lights(self):
        cc = copycalibration.CopyCalibration(
            src_bias_dir=None,
            src_flat_dir=self.directory_calibration,
            src_dark_dir=None,
            dest_bias_dir=None,
            dest_dark_dir=None,
            dest_flat_dir=None,
            dest_light_dir=self.directory_lights,
            debug=False,
            dryrun=True,
        )
        # cannot directly test GetCopyList_flats_to_lights
        # rely on mocking data and calling utility funciton 
        copy_list = cc.GetCopyList_flats_to_lights(required_properties=cc.flats_required_properties)

        # 'targetname' and 'type' are stripped from required properties
        self.assertIsNotNone(copy_list)
        self.assertEqual(len(copy_list), 4)
        self.assertEqual(copy_list[0][0], r"c:\calibration\masterFlat_FILTER_F_INSTRUME_AP26CC_DATE_2023-12-12_SETTEMP_-10.00_GAIN_100_OFFSET_50.xisf")
        self.assertEqual(copy_list[0][1], r"c:\lights\target1\accept\DATE_2023-12-12\masterFlat_FILTER_F_INSTRUME_AP26CC_DATE_2023-12-12_SETTEMP_-10.00_GAIN_100_OFFSET_50.xisf")
        self.assertEqual(copy_list[1][0], r"c:\calibration\masterFlat_FILTER_F_INSTRUME_AP26CC_DATE_2023-12-12_SETTEMP_-10.00_GAIN_100_OFFSET_50.xisf")
        self.assertEqual(copy_list[1][1], r"c:\lights\target2\accept\DATE_2023-12-12\masterFlat_FILTER_F_INSTRUME_AP26CC_DATE_2023-12-12_SETTEMP_-10.00_GAIN_100_OFFSET_50.xisf")
        self.assertEqual(copy_list[2][0], r"c:\calibration\masterFlat_FILTER_F_INSTRUME_AP26CC_DATE_2023-12-12_SETTEMP_-10.00_GAIN_100_OFFSET_50.xisf")
        self.assertEqual(copy_list[2][1], r"c:\lights\targetMissingDarks1\accept\DATE_2023-12-12\masterFlat_FILTER_F_INSTRUME_AP26CC_DATE_2023-12-12_SETTEMP_-10.00_GAIN_100_OFFSET_50.xisf")
        self.assertIsNone(copy_list[3][0])
        self.assertEqual(copy_list[3][1], r"c:\lights\targetMissingDarksFlats1\accept\DATE_2023-12-12\FILTER_X_EXP_45.00_SETTEMP_-10.00")

    def test_GetCopyList_flats_to_lights_multipleFlatsMatch(self):
        cc = copycalibration.CopyCalibration(
            src_bias_dir=None,
            src_flat_dir=self.directory_calibration,
            src_dark_dir=None,
            dest_bias_dir=None,
            dest_dark_dir=None,
            dest_flat_dir=None,
            dest_light_dir=self.directory_lights,
            debug=False,
            dryrun=True,
        )
        # cannot directly test GetCopyList_flats_to_lights
        # rely on mocking data and calling utility funciton 
        # use default input for required_properties
        data_flats = common.filter_metadata(
            data=self.data_mock_calibration,
            filters={"type": "MASTER FLAT"},
        )
        try:
            cc.GetCopyList_flats_to_lights(required_properties=cc.flats_required_properties)
            self.fail("expected exception raised for duplicate flats found")
        except:
            pass

if __name__ == '__main__':
    unittest.main()
