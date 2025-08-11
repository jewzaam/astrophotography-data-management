import unittest

import json
import traceback
import xisf
import os
from astropy.io import fits

import common

DIRECTORY_TEST_DATA = os.path.join(os.getcwd(), "test_data")

class Test_env_vars(unittest.TestCase):
    def test_replace_env_vars(self):
        filename=r"%AppData%"
        output = common.replace_env_vars(filename)
        # do not do a fancy comparison, this may run on another system. just verify it's not empty and has changed
        self.assertIsNotNone(output)
        self.assertTrue(len(output) > 0)
        self.assertNotEqual(filename, output)

class Test_camelCase(unittest.TestCase):
    def test_camelCase(self):
        self.assertEqual(common.camelCase('all lower test'), 'allLowerTest')
        self.assertEqual(common.camelCase('all lower test'.upper()), 'allLowerTest')
        self.assertEqual(common.camelCase('mIxEd CaSe TEst'), 'mixedCaseTest')
        self.assertEqual(common.camelCase('test+with+punctuation!'), 'testWithPunctuation')
        self.assertEqual(common.camelCase('PROPERTY_VALUE'), 'propertyValue')

class Test_normalize(unittest.TestCase):
    def test_denormalize_header(self):
        # only care about a few of these...
        self.assertEqual(common.denormalize_header('camera'), 'INSTRUME')
        self.assertEqual(common.denormalize_header('optic'), 'TELESCOP')
        self.assertEqual(common.denormalize_header('exposureseconds'), 'EXPOSURE')

    def test_normalize_filename_bias(self):
        output = common.normalize_filename(
            output_directory=r"E:\output\BIAS",
            input_filename=r"E:\input\somefile.fits",
            headers={
                "type": "BIAS",
                "optic": "optic",
                "camera": "camera",
                "date": "2023-12-12",
                "exposureseconds": "120.00",
                "datetime": "2023-12-08_04-46-31",
                "filter": "F",
                "settemp": "-10.00",
                "temp": "-9.00",
            },
            statedir=None,
        )
        self.assertEqual(output, r"E:\output\BIAS\optic+camera\DATE_2023-12-12\FILTER_F_EXP_120.00_SETTEMP_-10.00\2023-12-08_04-46-31_TEMP_-9.00.fits")

    def test_normalize_filename_dark(self):
        output = common.normalize_filename(
            output_directory=r"E:\output\DARK",
            input_filename=r"E:\input\somefile.fits",
            headers={
                "type": "DARK",
                "optic": "optic",
                "camera": "camera",
                "date": "2023-12-12",
                "exposureseconds": "120.00",
                "datetime": "2023-12-08_04-46-31",
                "filter": "F",
                "settemp": "-10.00",
                "temp": "-9.00",
            },
            statedir=None,
        )
        self.assertEqual(output, r"E:\output\DARK\optic+camera\DATE_2023-12-12\FILTER_F_EXP_120.00_SETTEMP_-10.00\2023-12-08_04-46-31_TEMP_-9.00.fits")

    def test_normalize_filename_flat(self):
        output = common.normalize_filename(
            output_directory=r"E:\output\FLAT",
            input_filename=r"E:\input\somefile.fits",
            headers={
                "type": "FLAT",
                "optic": "optic",
                "focal_ratio": "2.0",
                "camera": "camera",
                "filter": "F",
                "date": "2023-12-12",
                "exposureseconds": "120.00",
                "datetime": "2023-12-08_04-46-31",
                "settemp": "-10.00",
                "temp": "-9.00",
            },
            statedir=None,
        )
        self.assertEqual(output, r"E:\output\FLAT\optic+camera\DATE_2023-12-12\FILTER_F_EXP_120.00_SETTEMP_-10.00\2023-12-08_04-46-31_TEMP_-9.00.fits")

    def test_normalize_filename_light(self):
        output = common.normalize_filename(
            output_directory=r"E:\output",
            input_filename=r"E:\input\somefile.fits",
            headers={
                "type": "LIGHT",
                "optic": "optic",
                "focal_ratio": "2.0",
                "camera": "camera",
                "targetname": "the target",
                "date": "2023-12-12",
                "filter": "F",
                "exposureseconds": "120.00",
                "datetime": "2023-12-08_04-46-31",
                "settemp": "-10.00",
                "temp": "-9.00",
            },
            statedir=common.DIRECTORY_BLINK,
        )
        self.assertEqual(output, r"E:\output\optic@f2.0+camera\10_Blink\the target\DATE_2023-12-12\FILTER_F_EXP_120.00_SETTEMP_-10.00\2023-12-08_04-46-31_TEMP_-9.00.fits")

    def test_normalize_filename_withPanel(self):
        output = common.normalize_filename(
            output_directory=r"E:\output",
            input_filename=r"E:\input\somefile.fits",
            headers={
                "type": "LIGHT",
                "optic": "optic",
                "focal_ratio": "2.0",
                "camera": "camera",
                "targetname": "the target",
                "panel": "14",
                "date": "2023-12-12",
                "filter": "F",
                "exposureseconds": "120.00",
                "datetime": "2023-12-08_04-46-31",
                "settemp": "-10.00",
                "temp": "-9.00",
            },
            statedir=common.DIRECTORY_BLINK,
        )
        self.assertEqual(output, r"E:\output\optic@f2.0+camera\10_Blink\the target\DATE_2023-12-12\FILTER_F_EXP_120.00_SETTEMP_-10.00_PANEL_14\2023-12-08_04-46-31_TEMP_-9.00.fits")

    def test_normalize_filename_withOptional(self):
        output = common.normalize_filename(
            output_directory=r"E:\output",
            input_filename=r"E:\input\somefile.fits",
            headers={
                "type": "LIGHT",
                "optic": "optic",
                "focal_ratio": "2.0",
                "camera": "camera",
                "targetname": "the target",
                "panel": "14",
                "date": "2023-12-12",
                "filter": "F",
                "exposureseconds": "120.00",
                "datetime": "2023-12-08_04-46-31",
                "hfr": "hfr",
                "stars": "stars",
                "rmsac": "rmsac",
                "settemp": "-10.00",
                "temp": "-9.00",
            },
            statedir=common.DIRECTORY_BLINK,
        )
        self.assertEqual(output, r"E:\output\optic@f2.0+camera\10_Blink\the target\DATE_2023-12-12\FILTER_F_EXP_120.00_SETTEMP_-10.00_PANEL_14\2023-12-08_04-46-31_HFR_hfr_STARS_stars_RMSAC_rmsac_TEMP_-9.00.fits")

    def test_normalize_filename_missingRequired(self):
        try:
            common.normalize_filename(
                output_directory=r"E:\output",
                input_filename=r"E:\input\somefile.fits",
                headers={
                    "type": "LIGHT",
                    #"optic": "optic",
                    "focal_ratio": "2.0",
                    "camera": "camera",
                    "targetname": "the target",
                    "date": "2023-12-12",
                    "filter": "F",
                    "exposureseconds": "120.00",
                    "datetime": "2023-12-08_04-46-31",
                },
                statedir=common.DIRECTORY_BLINK,
            )
            self.fail("expected exception with missing: optic")
        except:
            pass


    def test_normalize_date_sameDay(self):
        date_in = "2023-10-02T21:04:46.237"
        date_out = common.normalize_date(date_in)
        self.assertEqual(date_out, "2023-10-02")
        
    def test_normalize_date_dayPlusOne(self):
        date_in = "2023-10-02T01:04:46.237"
        date_out = common.normalize_date(date_in)
        self.assertEqual(date_out, "2023-10-01")

    def test_normalize_datetime_sameDay(self):
        date_in = "2023-10-02T21:04:46.237"
        date_out = common.normalize_datetime(date_in)
        self.assertEqual(date_out, "2023-10-02_21-04-46")
        
    def test_normalize_datetime_dayPlusOne(self):
        date_in = "2023-10-02T01:04:46.237"
        date_out = common.normalize_datetime(date_in)
        self.assertEqual(date_out, "2023-10-02_01-04-46")

    def test_normalize_filterNames(self):
        # [ ["Input", "Expected"] ]
        test_data = [
            ["BaaderUVIRCut", "UVIR"],
            ["OptolongLeXtreme", "LeXtr"],
            ["S2", "S"],
            ["Ha", "H"],
            ["O3", "O"],
            ["", "RGB"],
            ["R", "R"],
            ["SomethingElse", "SomethingElse"],
        ]
        for datum in test_data:
            filter_in = datum[0]
            filter_expect = datum[1]
            filter_out = common.normalize_filterName(filter_in)
            self.assertEqual(filter_out, filter_expect)

class Test_filesystem(unittest.TestCase):
    def test_get_file_headers_SET_TEMP(self):
        # why a non-standard key is used for 'SET-TEMP', I don't know.
        # test for it to make sure we can handle it.
        headers = common.get_file_headers(
            filename=r"C:\KEY1-value1_SET-TEMP--10_KEY2_value2.fits",
            profileFromPath=False,
            objectFromPath=False,
            normalize=False,
        )
        self.assertEqual(headers['KEY1'], 'value1')
        self.assertEqual(headers['SET-TEMP'], '-10')
        self.assertEqual(headers['KEY2'], 'value2')

    def test_get_file_headers_EXPOSURE_with_uom(self):
        # why a non-standard key is used for 'SET-TEMP', I don't know.
        # test for it to make sure we can handle it.
        headers = common.get_file_headers(
            filename=r"C:\KEY1-value1_EXPOSURE-120.00s_KEY2_value2.fits",
            profileFromPath=False,
            objectFromPath=False,
            normalize=False,
        )
        self.assertEqual(headers['KEY1'], 'value1')
        self.assertEqual(headers['EXPOSURE'], '120.00')
        self.assertEqual(headers['KEY2'], 'value2')

    def test_get_filenames_notRecursive(self):
        filenames = common.get_filenames(
            dirs=[DIRECTORY_TEST_DATA],
            recursive=False,
        )
        self.assertIsNotNone(filenames)
        self.assertEqual(len(filenames), 1)
        self.assertEqual(filenames[0], r"C:\Users\jewza\Dropbox\Family Room\Astrophotography\Data\scripts\test_data\test_GAIN_999.fits")

    def test_get_filenames_recursive(self):
        filenames = common.get_filenames(
            dirs=[DIRECTORY_TEST_DATA],
            recursive=True,
        )
        self.assertIsNotNone(filenames)
        self.assertTrue(len(filenames) > 1)
        self.assertEqual(filenames[0], r"C:\Users\jewza\Dropbox\Family Room\Astrophotography\Data\scripts\test_data\test_GAIN_999.fits")

class Test_headers(unittest.TestCase):
    def test_file_headers_profileFromPathFalse(self):
        # Want "OBJECT" (aka targetname) to be set from the directory that is parent of "accept".
        # But to treat as though "OBJECT_" was prepended to that directory name, so other attributes will come through
        filename = r"C:\sometbasepath\C8@f6.3+AP26CC\Target Name\accept\DATE_2023-12-12_OBJECT_Some Other Name\etc.fits"
        headers = common.get_file_headers(
            filename=filename,
            normalize=False,
            objectFromPath=False,
            profileFromPath=False,
        )
        self.assertTrue('TELESCOP' not in headers)
        self.assertTrue('FOCRATIO' not in headers)
        self.assertTrue('INSTRUME' not in headers)

    def test_file_headers_profileFromPathTrue(self):
        # Want "OBJECT" (aka targetname) to be set from the directory that is parent of "accept".
        # But to treat as though "OBJECT_" was prepended to that directory name, so other attributes will come through
        filename = r"C:\sometbasepath\C8@f6.3+AP26CC\Target Name\accept\DATE_2023-12-12_OBJECT_Some Other Name\etc.fits"
        headers = common.get_file_headers(
            filename=filename,
            normalize=False,
            objectFromPath=False,
            profileFromPath=True,
        )
        self.assertEqual(headers['TELESCOP'], 'C8')
        self.assertEqual(headers['FOCRATIO'], '6.3')
        self.assertEqual(headers['INSTRUME'], 'AP26CC')

    def test_file_headers_objectFromPathTrue(self):
        # Want "OBJECT" (aka targetname) to be set from the directory that is parent of "accept".
        # But to treat as though "OBJECT_" was prepended to that directory name, so other attributes will come through
        filename = r"C:\sometbasepath\profileid\Target Name_LOCATION_Home\accept\DATE_2023-12-12_OBJECT_Some Other Name\etc.fits"
        headers = common.get_file_headers(
            filename=filename,
            normalize=False,
            objectFromPath=True,
            profileFromPath=False,
        )
        self.assertEqual(headers['OBJECT'], 'Target Name')
        self.assertEqual(headers['LOCATION'], 'Home')
        self.assertEqual(headers['DATE'], '2023-12-12')
        self.assertEqual(headers['filename'], filename)

    def test_file_headers_objectFromPathFalse(self):
        # Want "OBJECT" (aka targetname) to be set from the directory that is parent of "accept".
        # But to treat as though "OBJECT_" was prepended to that directory name, so other attributes will come through
        filename = r"C:\sometbasepath\profileid\Target Name_LOCATION_Home\accept\DATE_2023-12-12_OBJECT_Some Other Name\etc.fits"
        headers = common.get_file_headers(
            filename=filename,
            normalize=False,
            objectFromPath=False,
            profileFromPath=False,
        )
        self.assertEqual(headers['OBJECT'], 'Some Other Name')
        self.assertEqual(headers['LOCATION'], 'Home')
        self.assertEqual(headers['DATE'], '2023-12-12')
        self.assertEqual(headers['filename'], filename)

    def test_file_headers_simple_underscore(self):
        headers = common.get_file_headers(os.path.join(DIRECTORY_TEST_DATA, "ONE_1_TWO_2_THREE_3"), normalize=False, profileFromPath=False)
        self.assertEqual(headers['ONE'], '1')
        self.assertEqual(headers['TWO'], '2')
        self.assertEqual(headers['THREE'], '3')

    def test_file_headers_simple_spaceInValue(self):
        headers = common.get_file_headers(os.path.join(DIRECTORY_TEST_DATA, "ONE_1_TWO_SOME THING_THREE_3"), normalize=False, profileFromPath=False)
        self.assertEqual(headers['TWO'], 'SOME THING')

    def test_file_headers_simple_dash(self):
        headers = common.get_file_headers(os.path.join(DIRECTORY_TEST_DATA, "ONE-1_TWO-2_THREE-3"), normalize=False, profileFromPath=False)
        self.assertEqual(headers['ONE'], '1')
        self.assertEqual(headers['TWO'], '2')
        self.assertEqual(headers['THREE'], '3')

    def test_file_headers(self):
        headers = common.get_file_headers(os.path.join(DIRECTORY_TEST_DATA, "masterFlat_DATE_2023-12-04_FILTER_B_SETTEMP_-10.00_INSTRUME_ZWO ASI2600MM Pro_GAIN_100_OFFSET_50.xisf"), normalize=False, profileFromPath=False)
        self.assertEqual(headers['INSTRUME'], 'ZWO ASI2600MM Pro')
        self.assertEqual(headers['GAIN'], '100')

    def test_file_headers_orderOfProperties(self):
        headers = common.get_file_headers("TEST_A_TEST_B_NOTEST_C_TESTING_D", normalize=False, profileFromPath=False)
        self.assertEqual(headers['TEST'], 'A')

        headers = common.get_file_headers("NOTEST_C_TEST_A_TEST_B_TESTING_D", normalize=False, profileFromPath=False)
        self.assertEqual(headers['TEST'], 'A')

        headers = common.get_file_headers("NOTEST_C_TESTING_D_TEST_A_TEST_B", normalize=False, profileFromPath=False)
        self.assertEqual(headers['TEST'], 'A')

    def test_file_headers_withAcceptDirectory(self):
        headers = common.get_file_headers(r"E:\STUFF\data\R135@f2.8+ASI2600MM Pro\My Target Name Panel 3\accept\DATE_2023-12-04\masterFlat_DATE_2023-12-04_FILTER_X_SETTEMP_-10.00_INSTRUME_ASI2600MM Pro_GAIN_100_OFFSET_50.xisf", normalize=False, profileFromPath=False)
        self.assertEqual(headers['INSTRUME'], 'ASI2600MM Pro')
        self.assertEqual(headers['GAIN'], '100')

    def test_file_headers_withAcceptDirectory_normalized(self):
        headers = common.get_file_headers(r"E:\STUFF\data\R135@f2.8+ASI2600MM Pro\My Target Name Panel 3\accept\DATE_2023-12-04\masterFlat_DATE_2023-12-04_FILTER_X_SETTEMP_-10.00_INSTRUME_ASI2600MM Pro_GAIN_100_OFFSET_50.xisf", normalize=True, profileFromPath=False)
        self.assertEqual(headers['camera'], 'ASI2600MM Pro')
        self.assertEqual(headers['gain'], '100')
        self.assertFalse('INSTRUME' in headers)

        
    def test_file_headers_withoutAcceptDirectory(self):
        headers = common.get_file_headers(os.path.join(DIRECTORY_TEST_DATA, r"E:\STUFF\data\R135@f2.8+ASI2600MM Pro\My Target Name Panel 3\DATE_2023-12-04\masterFlat_DATE_2023-12-04_FILTER_X_SETTEMP_-10.00_INSTRUME_ASI2600MM Pro_GAIN_100_OFFSET_50.xisf"), normalize=False, profileFromPath=False)
        self.assertEqual(headers['INSTRUME'], 'ASI2600MM Pro')
        self.assertEqual(headers['GAIN'], '100')
        
    def test_fits_headers(self):
        headers = common.get_fits_headers(os.path.join(DIRECTORY_TEST_DATA, "test_GAIN_999.fits"), normalize=False, profileFromPath=False)
        self.assertEqual(headers['OBJECT'], 'Cave Nebula LBN529')
        self.assertEqual(headers['FILTER'], 'H')
        self.assertEqual(headers['GAIN'], '100')
        self.assertEqual(headers['OFFSET'], '50')

    def test_fits_headers_withNamingOverride(self):
        headers = common.get_fits_headers(os.path.join(DIRECTORY_TEST_DATA, "test_GAIN_999.fits"), normalize=False, file_naming_override=True, profileFromPath=False)
        self.assertEqual(headers['OBJECT'], 'Cave Nebula LBN529')
        self.assertEqual(headers['FILTER'], 'H')
        self.assertEqual(headers['GAIN'], '999') # from filename
        self.assertEqual(headers['OFFSET'], '50')

    def test_xisf_headers(self):
        headers = common.get_xisf_headers(os.path.join(DIRECTORY_TEST_DATA, "masterFlat_DATE_2023-12-04_FILTER_X_SETTEMP_-10.00_INSTRUME_ASI2600MM Pro_GAIN_100_OFFSET_50.xisf"), normalize=False, profileFromPath=False)
        self.assertEqual(headers['INSTRUME'], 'ZWO ASI2600MM Pro')
        self.assertEqual(headers['TELESCOP'], 'C8')
        self.assertEqual(headers['IMAGETYP'], 'Master Flat')
        self.assertEqual(headers['OBSGEO-B'], '35.60527778')
        self.assertEqual(headers['FILTER'], 'B')
        

    def test_xisf_headers_withNamingOverride(self):
        headers = common.get_xisf_headers(os.path.join(DIRECTORY_TEST_DATA, "masterFlat_DATE_2023-12-04_FILTER_X_SETTEMP_-10.00_INSTRUME_ASI2600MM Pro_GAIN_100_OFFSET_50.xisf"), normalize=False, file_naming_override=True, profileFromPath=False)
        self.assertEqual(headers['INSTRUME'], 'ASI2600MM Pro') # from filename
        self.assertEqual(headers['TELESCOP'], 'C8')
        self.assertEqual(headers['IMAGETYP'], 'Master Flat')
        self.assertEqual(headers['OBSGEO-B'], '35.60527778')
        self.assertEqual(headers['FILTER'], 'X') # from filename

    def test_normalized(self):
        # assumes all values are strings given the get headers functions
        headers = {
            "DATE-OBS": "2023-12-04T23:09:59.893",
            "FILTER": "O3",
            "EXPTIME": "0.7",
            "CCD-TEMP": "-9",
            "SET-TEMP": "-10",
            "IMAGETYP": "Master Flat",
            "GAIN": None,
            "OFFSET": "50",
            "TELESCOP": "C8",
            "FOCRATIO": "2.8",
            "INSTRUME": "ZWO ASI2600MM Pro",
            "SITELAT": None,
            "OBSGEO-B": "35.60527778",
            "SITELONG": None,
            "OBSGEO-L": "-78.79361111",
            "OBJECT": "Some Awesome Nebula",
        }
        normalized_headers = common.normalize_headers(headers)
        self.assertEqual(normalized_headers['date'], '2023-12-04')
        self.assertEqual(normalized_headers['datetime'], '2023-12-04_23-09-59')
        self.assertEqual(normalized_headers['filter'], "O")
        self.assertEqual(normalized_headers['exposureseconds'], "0.70")
        self.assertEqual(normalized_headers['temp'], "-9.00")
        self.assertEqual(normalized_headers['settemp'], "-10.00")
        self.assertEqual(normalized_headers['type'], "MASTER FLAT")
        self.assertEqual(normalized_headers['gain'], None)
        self.assertEqual(normalized_headers['offset'], "50")
        self.assertEqual(normalized_headers['optic'], "C8")
        self.assertEqual(normalized_headers['focal_ratio'], "2.8")
        self.assertEqual(normalized_headers['camera'], 'ZWO ASI2600MM Pro')
        self.assertEqual(normalized_headers['latitude'], '35.6')
        self.assertEqual(normalized_headers['longitude'], '-78.8')
        self.assertEqual(normalized_headers['targetname'], "Some Awesome Nebula")

    def test_normalized_with_panel(self):
        # assumes all values are strings given the get headers functions
        headers = {
            "OBJECT": "Some Awesome Nebula Panel 2",
        }
        normalized_headers = common.normalize_headers(headers)
        self.assertEqual(normalized_headers['targetname'], "Some Awesome Nebula")
        self.assertEqual(normalized_headers['panel'], "2")

    def test_gain_at_end_of_filename_dash(self):
        headers=common.get_file_headers(r"E:\\temp\\PI_WBPP\\_calibration\\master\\masterFlat_BIN-1_6248x4176_FILTER-S_mono_INSTRUME-ZWO ASI2600MM Pro_DATE-2023-12-06_SETTEMP--10.00_OFFSET-50_GAIN-100.xisf", normalize=False, profileFromPath=False)
        self.assertEqual(headers['GAIN'], "100")

    def test_gain_at_end_of_filename_underscore(self):
        headers=common.get_file_headers(r"E:\\temp\\PI_WBPP\\_calibration\\master\\masterFlat_BIN-1_6248x4176_FILTER-S_mono_INSTRUME-ZWO ASI2600MM Pro_DATE-2023-12-06_SETTEMP--10.00_OFFSET-50_GAIN_100.xisf", normalize=False, profileFromPath=False)
        self.assertEqual(headers['GAIN'], "100")

class Test_schedulerdb(unittest.TestCase):
    def test_project_status_from_path_Unknown(self):
        filename=r"C:\Something\Unknown\My Target\accept\DATE_2023-12-12"
        status = common.project_status_from_path(filename)
        self.assertEqual(status, 0)

    def test_project_status_from_path_Blink(self):
        filename=r"C:\Something\10_Blink\My Target\accept\DATE_2023-12-12"
        status = common.project_status_from_path(filename)
        self.assertEqual(status, 1)

    def test_project_status_from_path_Data(self):
        filename=r"C:\Something\20_Data\My Target\accept\DATE_2023-12-12"
        status = common.project_status_from_path(filename)
        self.assertEqual(status, 1)

    def test_project_status_from_path_Master(self):
        filename=r"C:\Something\30_Master\My Target\accept\DATE_2023-12-12"
        status = common.project_status_from_path(filename)
        self.assertEqual(status, 2)

    def test_project_status_from_path_Process(self):
        filename=r"C:\Something\40_Process\My Target\accept\DATE_2023-12-12"
        status = common.project_status_from_path(filename)
        self.assertEqual(status, 2)

    def test_project_status_from_path_Bake(self):
        filename=r"C:\Something\50_Bake\My Target\accept\DATE_2023-12-12"
        status = common.project_status_from_path(filename)
        self.assertEqual(status, 2)

    def test_project_status_from_path_Done(self):
        filename=r"C:\Something\60_Done\My Target\accept\DATE_2023-12-12"
        status = common.project_status_from_path(filename)
        self.assertEqual(status, 3)

class Test_csv(unittest.TestCase):
    def test_simpleObject_to_csv_withHeader(self):
        data = [{"key1": "1value1", "key2": "1value2"}, {"key1": "2value1", "key2": "2value2"}]
        csv = common.simpleObject_to_csv(data=data, output_headers=True)
        self.assertEqual(csv, "key1,key2\n1value1,1value2\n2value1,2value2\n")

    def test_simpleObject_to_csv_withoutHeader(self):
        data = [{"key1": "1value1", "key2": "1value2"}, {"key1": "2value1", "key2": "2value2"}]
        csv = common.simpleObject_to_csv(data=data, output_headers=False)
        self.assertEqual(csv, "1value1,1value2\n2value1,2value2\n")

    def test_simpleObject_to_csv_notUniformKeys(self):
        data = [{"key1": "1value1", "key2": "1value2"}, {"key2": "2value2", "key3": "2value3"}]
        csv = common.simpleObject_to_csv(data=data, output_headers=True)
        self.assertEqual(csv, "key1,key2,key3\n1value1,1value2,\n,2value2,2value3\n")

class Test_get_metadata(unittest.TestCase):
    def test_enrich_metadata_cr2(self):
        filename="some.cr2"
        metadata = {
            filename: {
                "some": "value",
                "filename": filename,
                "targetname": "something",
            }
        }
        enriched = common.enrich_metadata(
            data=metadata,
            required_properties=["required"],
            debug=False,
            printStatus=False,
            profileFromPath=False,
        )
        self.assertIsNotNone(enriched)
        self.assertEqual(len(enriched.keys()), 1)
        self.assertTrue('longitude' in enriched[filename])
        self.assertTrue('latitude' in enriched[filename])

    def test_get_metadata_xisf_notRecursive(self):
        metadata = common.get_metadata(
            dirs=[DIRECTORY_TEST_DATA],
            patterns=[".*\.xisf$"],
            recursive=False,
            required_properties=[],
            profileFromPath=False,
        )
        self.assertIsNotNone(metadata)
        self.assertIsNotNone(metadata.keys())
        self.assertEqual(len(metadata.keys()), 2, "unexpected number of keys")
        self.assertEqual(list(metadata.keys())[0], os.path.join(DIRECTORY_TEST_DATA, "masterDark_EXPOSURE_30.00_SETTEMP_-10.00_INSTRUME_ASI2600MM Pro_GAIN_100_OFFSET_50.xisf"))
        self.assertEqual(list(metadata.keys())[1], os.path.join(DIRECTORY_TEST_DATA, "masterFlat_DATE_2023-12-04_FILTER_X_SETTEMP_-10.00_INSTRUME_ASI2600MM Pro_GAIN_100_OFFSET_50.xisf"))
        # expect 'filename' property to be added
        self.assertTrue('filename' in metadata[list(metadata.keys())[0]], "filename attribute missing")
        self.assertTrue('filename' in metadata[list(metadata.keys())[1]], "filename attribute missing")

    def test_get_metadata_xisf_notRecursive(self):
        metadata = common.get_metadata(
            dirs=[DIRECTORY_TEST_DATA],
            patterns=[".*\.xisf$"],
            recursive=False,
            required_properties=[],
            profileFromPath=False,
        )
        self.assertIsNotNone(metadata)
        self.assertIsNotNone(metadata.keys())
        self.assertEqual(len(metadata.keys()), 2, "unexpected number of keys")
        self.assertEqual(list(metadata.keys())[0], os.path.join(DIRECTORY_TEST_DATA, "masterDark_EXPOSURE_30.00_SETTEMP_-10.00_INSTRUME_ASI2600MM Pro_GAIN_100_OFFSET_50.xisf"))
        self.assertEqual(list(metadata.keys())[1], os.path.join(DIRECTORY_TEST_DATA, "masterFlat_DATE_2023-12-04_FILTER_X_SETTEMP_-10.00_INSTRUME_ASI2600MM Pro_GAIN_100_OFFSET_50.xisf"))
        # expect 'filename' property to be added
        self.assertTrue('filename' in metadata[list(metadata.keys())[0]], "filename attribute missing")
        self.assertTrue('filename' in metadata[list(metadata.keys())[1]], "filename attribute missing")

    def test_get_metadata_fits_notRecursive(self):
        metadata = common.get_metadata(
            dirs=[DIRECTORY_TEST_DATA],
            patterns=[".*\.fits$"],
            recursive=False,
            required_properties=[],
            profileFromPath=False,
        )
        self.assertIsNotNone(metadata)
        self.assertIsNotNone(metadata.keys())
        self.assertEqual(len(metadata.keys()), 1, "unexpected number of keys")
        self.assertEqual(list(metadata.keys())[0], os.path.join(DIRECTORY_TEST_DATA, "test_GAIN_999.fits"))
        # expect 'filename' property to be added
        self.assertTrue('filename' in metadata[list(metadata.keys())[0]], "filename attribute missing")

    def test_get_metadata_fits_recursive(self):
        metadata = common.get_metadata(
            dirs=[DIRECTORY_TEST_DATA],
            patterns=[".*\.fits$"],
            recursive=True,
            required_properties=[],
            profileFromPath=False,
        )
        self.assertIsNotNone(metadata)
        self.assertIsNotNone(metadata.keys())
        self.assertEqual(len(metadata.keys()), 3, "unexpected number of keys")
        self.assertEqual(list(metadata.keys())[0], os.path.join(DIRECTORY_TEST_DATA, "test_GAIN_999.fits"))
        self.assertEqual(list(metadata.keys())[1], os.path.join(DIRECTORY_TEST_DATA, "child1", "FILTER_UVIR_EXP_120.00_2023-12-07_20-27-45_HFR_2.51_STARS_718_RMSAC_0.85_TEMP_-9.90.fits"))
        self.assertEqual(list(metadata.keys())[2], os.path.join(DIRECTORY_TEST_DATA, "child2", "FILTER_UVIR_EXP_120.00_2023-12-07_20-56-01_HFR_2.52_STARS_836_RMSAC_0.62_TEMP_-9.90.fits"))
        # expect 'filename' property to be added
        self.assertTrue('filename' in metadata[list(metadata.keys())[0]], "filename attribute missing")
        self.assertTrue('filename' in metadata[list(metadata.keys())[1]], "filename attribute missing")
        self.assertTrue('filename' in metadata[list(metadata.keys())[2]], "filename attribute missing")

    def test_get_metadata_fits_recursive_enrich(self):
        metadata = common.get_metadata(
            dirs=[DIRECTORY_TEST_DATA],
            patterns=[".*\.fits$"],
            recursive=True,
            required_properties=['settemp'],
            profileFromPath=False,
        )
        self.assertIsNotNone(metadata)
        self.assertIsNotNone(metadata.keys())
        self.assertEqual(len(metadata.keys()), 3, "unexpected number of keys")
        self.assertEqual(list(metadata.keys())[0], os.path.join(DIRECTORY_TEST_DATA, "test_GAIN_999.fits"))
        self.assertEqual(list(metadata.keys())[1], os.path.join(DIRECTORY_TEST_DATA, "child1", "FILTER_UVIR_EXP_120.00_2023-12-07_20-27-45_HFR_2.51_STARS_718_RMSAC_0.85_TEMP_-9.90.fits"))
        self.assertEqual(list(metadata.keys())[2], os.path.join(DIRECTORY_TEST_DATA, "child2", "FILTER_UVIR_EXP_120.00_2023-12-07_20-56-01_HFR_2.52_STARS_836_RMSAC_0.62_TEMP_-9.90.fits"))
        self.assertEqual(metadata[list(metadata.keys())[0]]['settemp'], '-5.00')
        self.assertEqual(metadata[list(metadata.keys())[1]]['settemp'], '-10.00')
        self.assertEqual(metadata[list(metadata.keys())[2]]['settemp'], '-10.00')
        # and sanity check we got values from filename
        self.assertEqual(metadata[list(metadata.keys())[0]]['gain'], '999') # filename value overrides FITS header
        self.assertEqual(metadata[list(metadata.keys())[1]]['gain'], '100')
        self.assertEqual(metadata[list(metadata.keys())[2]]['gain'], '100')
        # expect 'filename' property to be added
        self.assertTrue('filename' in metadata[list(metadata.keys())[0]], "filename attribute missing")
        self.assertTrue('filename' in metadata[list(metadata.keys())[1]], "filename attribute missing")
        self.assertTrue('filename' in metadata[list(metadata.keys())[2]], "filename attribute missing")

    def test_get_metadata_fits_recursive_enrich_then_filterMatch(self):
        metadata = common.get_metadata(
            dirs=[DIRECTORY_TEST_DATA],
            patterns=[".*\.fits$"],
            recursive=True,
            required_properties=['settemp'],
            profileFromPath=False,
        )
        self.assertIsNotNone(metadata)
        self.assertIsNotNone(metadata.keys())
        self.assertEqual(len(metadata.keys()), 3, "unexpected number of keys")
        filtered = common.filter_metadata(
            data=metadata,
            filters={
                "filter": "UVIR",
            }
        )
        self.assertEqual(len(filtered.keys()), 2, "unexpected number of keys")
        self.assertEqual(list(filtered.keys())[0], os.path.join(DIRECTORY_TEST_DATA, "child1", "FILTER_UVIR_EXP_120.00_2023-12-07_20-27-45_HFR_2.51_STARS_718_RMSAC_0.85_TEMP_-9.90.fits"))
        self.assertEqual(list(filtered.keys())[1], os.path.join(DIRECTORY_TEST_DATA, "child2", "FILTER_UVIR_EXP_120.00_2023-12-07_20-56-01_HFR_2.52_STARS_836_RMSAC_0.62_TEMP_-9.90.fits"))

    def test_get_filtered_metadata_fits_recursive(self):
        filtered = common.get_filtered_metadata(
            dirs=[DIRECTORY_TEST_DATA],
            patterns=[".*\.fits$"],
            recursive=True,
            required_properties=['settemp'],
            filters={"filter": "UVIR",},
            profileFromPath=False,
        )
        self.assertIsNotNone(filtered)
        self.assertIsNotNone(filtered.keys())
        self.assertEqual(len(filtered.keys()), 2, "unexpected number of keys")
        self.assertEqual(list(filtered.keys())[0], os.path.join(DIRECTORY_TEST_DATA, "child1", "FILTER_UVIR_EXP_120.00_2023-12-07_20-27-45_HFR_2.51_STARS_718_RMSAC_0.85_TEMP_-9.90.fits"))
        self.assertEqual(list(filtered.keys())[1], os.path.join(DIRECTORY_TEST_DATA, "child2", "FILTER_UVIR_EXP_120.00_2023-12-07_20-56-01_HFR_2.52_STARS_836_RMSAC_0.62_TEMP_-9.90.fits"))

    def test_get_metadata_fits_recursive_enrich_then_filterNoMatch(self):
        metadata = common.get_metadata(
            dirs=[DIRECTORY_TEST_DATA],
            patterns=[".*\.fits$"],
            recursive=True,
            required_properties=['settemp'],
            profileFromPath=False,
        )
        self.assertIsNotNone(metadata)
        self.assertIsNotNone(metadata.keys())
        self.assertEqual(len(metadata.keys()), 3, "unexpected number of keys")
        filtered = common.filter_metadata(
            data=metadata,
            filters={
                "filter": "UVIR",
                "gain": "NOPE",
            }
        )
        self.assertEqual(len(filtered.keys()), 0, "unexpected number of keys")

class Test_filter_metadata(unittest.TestCase):
    metadata = {
        "filename1": {"a": "1", "b": "1", "c": "1"},
        "filename2": {"a": "2", "b": "2", "c": "2"},
        "filename3": {"a": "3", "b": "3", "c": "3"},
        "filename4": {"a": "4", "b": "3", "c": "3"},
    }

    def test_filter_metadata_invalidFilters(self):
        try: 
            common.filter_metadata(data=self.metadata, filters=None)
            self.fail("expected Exception for filters=None")
        except:
            pass

        try: 
            common.filter_metadata(data=self.metadata, filters={})
            self.fail("expected Exception for filters={}")
        except:
            pass

        try: 
            common.filter_metadata(data=self.metadata, filters={"a", None})
            self.fail("expected Exception for filters={\"a\": None}")
        except:
            pass

        try: 
            common.filter_metadata(data=self.metadata, filters={"a", ""})
            self.fail("expected Exception for filters={\"a\": \"\"}")
        except:
            pass

    def test_filter_metadata_oneFilter_matchOne(self):
        filters={
            "a": "1",
        }
        expected = {}
        expected['filename1'] = self.metadata['filename1']
        filtered = common.filter_metadata(data=self.metadata, filters=filters)
        self.assertEqual(filtered, expected)

    def test_filter_metadata_oneFilter_noMatch(self):
        filters={
            "a": "NOPE",
        }
        expected = {}
        filtered = common.filter_metadata(data=self.metadata, filters=filters)
        self.assertEqual(filtered, expected)

    def test_filter_metadata_twoFilters_noMatch(self):
        filters={
            "b": "NOPE",
            "c": "NOPE",
        }
        expected = {}
        filtered = common.filter_metadata(data=self.metadata, filters=filters)
        self.assertEqual(filtered, expected)

    def test_filter_metadata_twoFilters_matchOne(self):
        filters={
            "a": "1",
            "b": "1",
        }
        expected = {}
        expected['filename1'] = self.metadata['filename1']
        filtered = common.filter_metadata(data=self.metadata, filters=filters)
        self.assertEqual(filtered, expected)

    def test_filter_metadata_twoFilters_matchTwo(self):
        filters={
            "b": "3",
            "c": "3",
        }
        expected = {}
        expected['filename3'] = self.metadata['filename3']
        expected['filename4'] = self.metadata['filename4']
        filtered = common.filter_metadata(data=self.metadata, filters=filters)
        self.assertEqual(filtered, expected)
    
    def test_filter_metadata_with_lambda(self):
        filters={
            "a": (lambda x: x != "3"),
            "b": (lambda x: True), # allow any b
            "c": "3",
        }
        expected = {}
        expected['filename4'] = self.metadata['filename4']
        filtered = common.filter_metadata(data=self.metadata, filters=filters)
        self.assertEqual(filtered, expected)

class Test_copy_calibration(unittest.TestCase):
    data_calibration={
        "dark1.xisf": {
            "type": "MASTER DARK",
            "camera": "myCamera",
            "optic": "teleScope",
            "focal_ratio": "2.8",
            "filter": "F",
            "exposureseconds": "60.00",
            "settemp": "-10.00",
            "gain": "100",
            "offset": "50",
            "filename": "dark1.xisf",
        },
        "dark2.xisf": {
            "type": "MASTER DARK",
            "camera": "myCamera",
            "optic": "teleScope",
            "focal_ratio": "2.8",
            "filter": "F",
            "exposureseconds": "120.00",
            "settemp": "-10.00",
            "gain": "100",
            "offset": "50",
            "filename": "dark2.xisf",
        },
        "flat1.xisf": {
            "type": "MASTER FLAT",
            "camera": "myCamera",
            "optic": "teleScope",
            "focal_ratio": "2.8",
            "filter": "F",
            "exposureseconds": "1.00",
            "settemp": "-10.00",
            "gain": "100",
            "offset": "50",
            "filename": "flat1.xisf",
        },
        "flat2.xisf": {
            "type": "MASTER FLAT",
            "camera": "myCamera",
            "optic": "teleScope",
            "focal_ratio": "2.8",
            "filter": "Z",
            "exposureseconds": "2.00",
            "settemp": "-10.00",
            "gain": "100",
            "offset": "50",
            "filename": "flat2.xisf",
        },
    }

    def test_get_copy_list_basic(self):
        # (input_dir:str, output_dir:str, group_by:[], debug=False):
        # output_filename_only = {type}[_filterKey_{filterValue}]*.{extension}
        # to_file = {output_dir}/{camera}[/{optic}]/{output_filename_only}
        output = common.get_copy_list(
            data=self.data_calibration,
            output_dir="C:\output",
            filters={
                "type":"MASTER DARK", 
                "exposureseconds": "60.00",
            },
        )
        self.assertIsNotNone(output)
        self.assertEqual(len(output), 1)
        self.assertEqual(output[0][0], r"dark1.xisf")
        self.assertEqual(output[0][1], r"C:\output\myCamera\masterDark_EXPOSURE_60.00.xisf")

    def test_get_copy_list_darks(self):
        # (input_dir:str, output_dir:str, group_by:[], debug=False):
        # output_filename_only = {type}[_filterKey_{filterValue}]*.{extension}
        # to_file = {output_dir}/{camera}[/{optic}]/{output_filename_only}
        output = common.get_copy_list(
            data=self.data_calibration,
            output_dir="C:\output",
            filters={
                "type":"MASTER DARK", 
                "exposureseconds": "120.00",
                "settemp": "-10.00",
                "gain": "100",
                "offset": "50",
            },
        )
        self.assertIsNotNone(output)
        self.assertEqual(len(output), 1)
        self.assertEqual(output[0][0], r"dark2.xisf")
        self.assertEqual(output[0][1], r"C:\output\myCamera\masterDark_EXPOSURE_120.00_SETTEMP_-10.00_GAIN_100_OFFSET_50.xisf")

    def test_get_copy_list_darksAll(self):
        # (input_dir:str, output_dir:str, group_by:[], debug=False):
        # output_filename_only = {type}[_filterKey_{filterValue}]*.{extension}
        # to_file = {output_dir}/{camera}[/{optic}]/{output_filename_only}
        output = common.get_copy_list(
            data=self.data_calibration,
            output_dir="C:\output",
            filters={
                "type":"MASTER DARK", 
                "exposureseconds": (lambda x: True), # any!
                "settemp": (lambda x: True), # any!
                "camera": (lambda x: True), # any!
                "gain": (lambda x: True), # any!
                "offset": (lambda x: True), # any!
            },
        )
        self.assertIsNotNone(output)
        self.assertEqual(len(output), 2)
        self.assertEqual(output[0][0], r"dark1.xisf")
        self.assertEqual(output[0][1], r"C:\output\myCamera\masterDark_EXPOSURE_60.00_SETTEMP_-10.00_GAIN_100_OFFSET_50.xisf")
        self.assertEqual(output[1][0], r"dark2.xisf")
        self.assertEqual(output[1][1], r"C:\output\myCamera\masterDark_EXPOSURE_120.00_SETTEMP_-10.00_GAIN_100_OFFSET_50.xisf")

    def test_get_copy_list_flats(self):
        # (input_dir:str, output_dir:str, group_by:[], debug=False):
        # output_filename_only = {type}[_filterKey_{filterValue}]*.{extension}
        # to_file = {output_dir}/{camera}[/{optic}]/{output_filename_only}
        output = common.get_copy_list(
            data=self.data_calibration,
            output_dir="C:\output",
            filters={
                "type":"MASTER FLAT",
                "filter": "F", 
                "settemp": "-10.00",
                "gain": "100",
                "offset": "50",
            },
        )
        self.assertIsNotNone(output)
        self.assertEqual(len(output), 1)
        self.assertEqual(output[0][0], r"flat1.xisf")
        self.assertEqual(output[0][1], r"C:\output\myCamera\masterFlat_FILTER_F_SETTEMP_-10.00_GAIN_100_OFFSET_50.xisf")

    def test_get_copy_list_noMatch(self):
        # (input_dir:str, output_dir:str, group_by:[], debug=False):
        # output_filename_only = {type}[_filterKey_{filterValue}]*.{extension}
        # to_file = {output_dir}/{camera}[/{optic}]/{output_filename_only}
        output = common.get_copy_list(
            data=self.data_calibration,
            output_dir="C:\output",
            filters={
                "type":"MASTER FLAT",
                "filter": (lambda x: False), # never can match
            },
        )
        self.assertIsNotNone(output)
        self.assertEqual(len(output), 0)



if __name__ == '__main__':
    unittest.main()
