import unittest

from bs4 import BeautifulSoup

from pycaption import (
    DFXPReader, DFXPWriter, SRTWriter, SAMIWriter, WebVTTWriter)

from pycaption.dfxp import (
    DFXP_DEFAULT_STYLE, DFXP_DEFAULT_STYLE_ID, 
    DFXP_DEFAULT_REGION, DFXP_DEFAULT_REGION_ID)
from .samples import (
    SAMPLE_SAMI, SAMPLE_SRT, SAMPLE_DFXP,
    SAMPLE_SAMI_UTF8, SAMPLE_SRT_UTF8, SAMPLE_DFXP_UTF8,
    SAMPLE_SAMI_UNICODE, SAMPLE_DFXP_UNICODE, SAMPLE_WEBVTT,
    SAMPLE_SRT_UNICODE)
from .mixins import SRTTestingMixIn, SAMITestingMixIn, DFXPTestingMixIn, WebVTTTestingMixIn


class DFXPConversionTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.captions = DFXPReader().read(SAMPLE_DFXP.decode(u'utf-8'))
        cls.captions_utf8 = DFXPReader().read(SAMPLE_DFXP_UTF8.decode(u'utf-8'))
        cls.captions_unicode = DFXPReader().read(SAMPLE_DFXP_UNICODE)


class DFXPtoDFXPTestCase(DFXPConversionTestCase, DFXPTestingMixIn):

    def test_dfxp_to_dfxp_conversion(self):
        results = DFXPWriter().write(self.captions)
        self.assertTrue(isinstance(results, unicode))
        self.assertDFXPEquals(SAMPLE_DFXP.decode(u'utf-8'), results)

    def test_dfxp_to_dfxp_utf8_conversion(self):
        results = DFXPWriter().write(self.captions_utf8)
        self.assertTrue(isinstance(results, unicode))
        self.assertDFXPEquals(SAMPLE_DFXP_UNICODE, results)

    def test_dfxp_to_dfxp_unicode_conversion(self):
        results = DFXPWriter().write(self.captions_unicode)
        self.assertTrue(isinstance(results, unicode))
        self.assertDFXPEquals(SAMPLE_DFXP_UNICODE, results)

    def test_default_styling_tag(self):
        w = DFXPWriter()
        w.default_settings = True
        result = w.write(self.captions)

        default_style = w._recreate_style(DFXP_DEFAULT_STYLE, None)
        default_style[u'xml:id'] = DFXP_DEFAULT_STYLE_ID

        soup = BeautifulSoup(result, u'xml')
        style = soup.find(u'style', {u'xml:id': DFXP_DEFAULT_STYLE_ID})
        
        self.assertTrue(style)
        self.assertEquals(style.attrs, default_style)

    def test_default_styling_p_tags(self):
        w = DFXPWriter()
        w.default_settings = True
        result = w.write(self.captions)

        soup = BeautifulSoup(result, u'xml')
        for p in soup.find_all(u'p'):
            self.assertEquals(p.attrs.get(u'style'), DFXP_DEFAULT_STYLE_ID)

    def test_default_region_tag(self):
        w = DFXPWriter()
        w.default_settings = True
        result = w.write(self.captions)

        default_region = w._recreate_style(DFXP_DEFAULT_REGION, None)
        default_region[u'xml:id'] = DFXP_DEFAULT_REGION_ID

        soup = BeautifulSoup(result, u'xml')
        region = soup.find(u'region', {u'xml:id': DFXP_DEFAULT_REGION_ID})
        
        self.assertTrue(region)
        self.assertEquals(region.attrs, default_region)

    def test_default_region_p_tags(self):
        w = DFXPWriter()
        w.default_settings = True
        result = w.write(self.captions)

        soup = BeautifulSoup(result, u'xml')
        for p in soup.find_all(u'p'):
            self.assertEquals(p.attrs.get(u'region'), DFXP_DEFAULT_REGION_ID)


class DFXPtoSRTTestCase(DFXPConversionTestCase, SRTTestingMixIn):

    def test_dfxp_to_srt_conversion(self):
        results = SRTWriter().write(self.captions)
        self.assertTrue(isinstance(results, unicode))
        self.assertSRTEquals(SAMPLE_SRT.decode(u'utf-8'), results)

    def test_dfxp_to_srt_utf8_conversion(self):
        results = SRTWriter().write(self.captions_utf8)
        self.assertTrue(isinstance(results, unicode))
        self.assertSRTEquals(SAMPLE_SRT_UNICODE, results)

    def test_dfxp_to_srt_unicode_conversion(self):
        results = SRTWriter().write(self.captions_unicode)
        self.assertTrue(isinstance(results, unicode))
        self.assertSRTEquals(SAMPLE_SRT_UNICODE, results)


class DFXPtoSAMITestCase(DFXPConversionTestCase, SAMITestingMixIn):

    def test_dfxp_to_sami_conversion(self):
        results = SAMIWriter().write(self.captions)
        self.assertTrue(isinstance(results, unicode))
        self.assertSAMIEquals(SAMPLE_SAMI.decode(u'utf-8'), results)

    def test_dfxp_to_sami_utf8_conversion(self):
        results = SAMIWriter().write(self.captions_utf8)
        self.assertTrue(isinstance(results, unicode))
        self.assertSAMIEquals(SAMPLE_SAMI_UNICODE, results)

    def test_dfxp_to_sami_unicode_conversion(self):
        results = SAMIWriter().write(self.captions_unicode)
        self.assertTrue(isinstance(results, unicode))
        self.assertSAMIEquals(SAMPLE_SAMI_UNICODE, results)


class DFXPtoWebVTTTestCase(DFXPConversionTestCase, WebVTTTestingMixIn):

    def test_dfxp_to_webvtt_conversion(self):
        results = WebVTTWriter().write(self.captions_utf8)
        self.assertTrue(isinstance(results, unicode))
        self.assertWebVTTEquals(SAMPLE_WEBVTT.decode(u'utf-8'), results)

    def test_dfxp_to_webvtt_unicode_conversion(self):
        results = WebVTTWriter().write(self.captions_unicode)
        self.assertTrue(isinstance(results, unicode))
        self.assertWebVTTEquals(SAMPLE_WEBVTT.decode(u'utf-8'), results)
