# -*- coding: ascii -*-
"""
lots of Excel Magic Numbers
"""

# Boundaries BIFF8+

MAX_ROW = 65536
MAX_COL = 256


biff_records = {
    0x0000: "DIMENSIONS",
    0x0001: "BLANK",
    0x0002: "INTEGER",
    0x0003: "NUMBER",
    0x0004: "LABEL",
    0x0005: "BOOLERR",
    0x0006: "FORMULA",
    0x0007: "STRING",
    0x0008: "ROW",
    0x0009: "BOF",
    0x000A: "EOF",
    0x000B: "INDEX",
    0x000C: "CALCCOUNT",
    0x000D: "CALCMODE",
    0x000E: "PRECISION",
    0x000F: "REFMODE",
    0x0010: "DELTA",
    0x0011: "ITERATION",
    0x0012: "PROTECT",
    0x0013: "PASSWORD",
    0x0014: "HEADER",
    0x0015: "FOOTER",
    0x0016: "EXTERNCOUNT",
    0x0017: "EXTERNSHEET",
    0x0018: "NAME",
    0x0019: "WINDOWPROTECT",
    0x001A: "VERTICALPAGEBREAKS",
    0x001B: "HORIZONTALPAGEBREAKS",
    0x001C: "NOTE",
    0x001D: "SELECTION",
    0x001E: "FORMAT",
    0x001F: "FORMATCOUNT",
    0x0020: "COLUMNDEFAULT",
    0x0021: "ARRAY",
    0x0022: "1904",
    0x0023: "EXTERNNAME",
    0x0024: "COLWIDTH",
    0x0025: "DEFAULTROWHEIGHT",
    0x0026: "LEFTMARGIN",
    0x0027: "RIGHTMARGIN",
    0x0028: "TOPMARGIN",
    0x0029: "BOTTOMMARGIN",
    0x002A: "PRINTHEADERS",
    0x002B: "PRINTGRIDLINES",
    0x002F: "FILEPASS",
    0x0031: "FONT",
    0x0036: "TABLE",
    0x003C: "CONTINUE",
    0x003D: "WINDOW1",
    0x003E: "WINDOW2",
    0x0040: "BACKUP",
    0x0041: "PANE",
    0x0042: "CODEPAGE",
    0x0043: "XF",
    0x0044: "IXFE",
    0x0045: "EFONT",
    0x004D: "PLS",
    0x0050: "DCON",
    0x0051: "DCONREF",
    0x0053: "DCONNAME",
    0x0055: "DEFCOLWIDTH",
    0x0056: "BUILTINFMTCNT",
    0x0059: "XCT",
    0x005A: "CRN",
    0x005B: "FILESHARING",
    0x005C: "WRITEACCESS",
    0x005D: "OBJ",
    0x005E: "UNCALCED",
    0x005F: "SAFERECALC",
    0x0060: "TEMPLATE",
    0x0063: "OBJPROTECT",
    0x007D: "COLINFO",
    0x007E: "RK",
    0x007F: "IMDATA",
    0x0080: "GUTS",
    0x0081: "WSBOOL",
    0x0082: "GRIDSET",
    0x0083: "HCENTER",
    0x0084: "VCENTER",
    0x0085: "BOUNDSHEET",
    0x0086: "WRITEPROT",
    0x0087: "ADDIN",
    0x0088: "EDG",
    0x0089: "PUB",
    0x008C: "COUNTRY",
    0x008D: "HIDEOBJ",
    0x008E: "BUNDLESOFFSET",
    0x008F: "BUNDLEHEADER",
    0x0090: "SORT",
    0x0091: "SUB",
    0x0092: "PALETTE",
    0x0093: "STYLE",
    0x0094: "LHRECORD",
    0x0095: "LHNGRAPH",
    0x0096: "SOUND",
    0x0098: "LPR",
    0x0099: "STANDARDWIDTH",
    0x009A: "FNGROUPNAME",
    0x009B: "FILTERMODE",
    0x009C: "FNGROUPCOUNT",
    0x009D: "AUTOFILTERINFO",
    0x009E: "AUTOFILTER",
    0x00A0: "SCL",
    0x00A1: "SETUP",
    0x00A9: "COORDLIST",
    0x00AB: "GCW",
    0x00AE: "SCENMAN",
    0x00AF: "SCENARIO",
    0x00B0: "SXVIEW",
    0x00B1: "SXVD",
    0x00B2: "SXVI",
    0x00B4: "SXIVD",
    0x00B5: "SXLI",
    0x00B6: "SXPI",
    0x00B8: "DOCROUTE",
    0x00B9: "RECIPNAME",
    0x00BC: "SHRFMLA",
    0x00BD: "MULRK",
    0x00BE: "MULBLANK",
    0x00C1: "MMS",
    0x00C2: "ADDMENU",
    0x00C3: "DELMENU",
    0x00C5: "SXDI",
    0x00C6: "SXDB",
    0x00C7: "SXFIELD",
    0x00C8: "SXINDEXLIST",
    0x00C9: "SXDOUBLE",
    0x00CD: "SXSTRING",
    0x00CE: "SXDATETIME",
    0x00D0: "SXTBL",
    0x00D1: "SXTBRGITEM",
    0x00D2: "SXTBPG",
    0x00D3: "OBPROJ",
    0x00D5: "SXIDSTM",
    0x00D6: "RSTRING",
    0x00D7: "DBCELL",
    0x00DA: "BOOKBOOL",
    0x00DC: "SXEXT|PARAMQRY",
    0x00DD: "SCENPROTECT",
    0x00DE: "OLESIZE",
    0x00DF: "UDDESC",
    0x00E0: "XF",
    0x00E1: "INTERFACEHDR",
    0x00E2: "INTERFACEEND",
    0x00E3: "SXVS",
    0x00E5: "MERGEDCELLS",
    0x00E9: "BITMAP",
    0x00EB: "MSODRAWINGGROUP",
    0x00EC: "MSODRAWING",
    0x00ED: "MSODRAWINGSELECTION",
    0x00F0: "SXRULE",
    0x00F1: "SXEX",
    0x00F2: "SXFILT",
    0x00F6: "SXNAME",
    0x00F7: "SXSELECT",
    0x00F8: "SXPAIR",
    0x00F9: "SXFMLA",
    0x00FB: "SXFORMAT",
    0x00FC: "SST",
    0x00FD: "LABELSST",
    0x00FF: "EXTSST",
    0x0100: "SXVDEX",
    0x0103: "SXFORMULA",
    0x0122: "SXDBEX",
    0x0137: "CHTRINSERT",
    0x0138: "CHTRINFO",
    0x013B: "CHTRCELLCONTENT",
    0x013D: "TABID",
    0x0140: "CHTRMOVERANGE",
    0x014D: "CHTRINSERTTAB",
    0x015F: "LABELRANGES",
    0x0160: "USESELFS",
    0x0161: "DSF",
    0x0162: "XL5MODIFY",
    0x0196: "CHTRHEADER",
    0x01A9: "USERBVIEW",
    0x01AA: "USERSVIEWBEGIN",
    0x01AB: "USERSVIEWEND",
    0x01AD: "QSI",
    0x01AE: "SUPBOOK",
    0x01AF: "PROT4REV",
    0x01B0: "CONDFMT",
    0x01B1: "CF",
    0x01B2: "DVAL",
    0x01B5: "DCONBIN",
    0x01B6: "TXO",
    0x01B7: "REFRESHALL",
    0x01B8: "HLINK",
    0x01BA: "CODENAME",
    0x01BB: "SXFDBTYPE",
    0x01BC: "PROT4REVPASS",
    0x01BE: "DV",
    0x01C0: "XL9FILE",
    0x01C1: "RECALCID",
    0x0200: "DIMENSIONS",
    0x0201: "BLANK",
    0x0203: "NUMBER",
    0x0204: "LABEL",
    0x0205: "BOOLERR",
    0x0206: "FORMULA",
    0x0207: "STRING",
    0x0208: "ROW",
    0x0209: "BOF",
    0x020B: "INDEX",
    0x0218: "NAME",
    0x0221: "ARRAY",
    0x0223: "EXTERNNAME",
    0x0225: "DEFAULTROWHEIGHT",
    0x0231: "FONT",
    0x0236: "TABLE",
    0x023E: "WINDOW2",
    0x0243: "XF",
    0x027E: "RK",
    0x0293: "STYLE",
    0x0406: "FORMULA",
    0x0409: "BOF",
    0x041E: "FORMAT",
    0x0443: "XF",
    0x04BC: "SHRFMLA",
    0x0800: "SCREENTIP",
    0x0803: "WEBQRYSETTINGS",
    0x0804: "WEBQRYTABLES",
    0x0809: "BOF",
    0x0862: "SHEETLAYOUT",
    0x0867: "SHEETPROTECTION",
    0x1001: "UNITS",
    0x1002: "ChartChart",
    0x1003: "ChartSeries",
    0x1006: "ChartDataformat",
    0x1007: "ChartLineformat",
    0x1009: "ChartMarkerformat",
    0x100A: "ChartAreaformat",
    0x100B: "ChartPieformat",
    0x100C: "ChartAttachedlabel",
    0x100D: "ChartSeriestext",
    0x1014: "ChartChartformat",
    0x1015: "ChartLegend",
    0x1016: "ChartSerieslist",
    0x1017: "ChartBar",
    0x1018: "ChartLine",
    0x1019: "ChartPie",
    0x101A: "ChartArea",
    0x101B: "ChartScatter",
    0x101C: "ChartChartline",
    0x101D: "ChartAxis",
    0x101E: "ChartTick",
    0x101F: "ChartValuerange",
    0x1020: "ChartCatserrange",
    0x1021: "ChartAxislineformat",
    0x1022: "ChartFormatlink",
    0x1024: "ChartDefaulttext",
    0x1025: "ChartText",
    0x1026: "ChartFontx",
    0x1027: "ChartObjectLink",
    0x1032: "ChartFrame",
    0x1033: "BEGIN",
    0x1034: "END",
    0x1035: "ChartPlotarea",
    0x103A: "Chart3D",
    0x103C: "ChartPicf",
    0x103D: "ChartDropbar",
    0x103E: "ChartRadar",
    0x103F: "ChartSurface",
    0x1040: "ChartRadararea",
    0x1041: "ChartAxisparent",
    0x1043: "ChartLegendxn",
    0x1044: "ChartShtprops",
    0x1045: "ChartSertocrt",
    0x1046: "ChartAxesused",
    0x1048: "ChartSbaseref",
    0x104A: "ChartSerparent",
    0x104B: "ChartSerauxtrend",
    0x104E: "ChartIfmt",
    0x104F: "ChartPos",
    0x1050: "ChartAlruns",
    0x1051: "ChartAI",
    0x105B: "ChartSerauxerrbar",
    0x105D: "ChartSerfmt",
    0x105F: "Chart3DDataFormat",
    0x1060: "ChartFbi",
    0x1061: "ChartBoppop",
    0x1062: "ChartAxcext",
    0x1063: "ChartDat",
    0x1064: "ChartPlotgrowth",
    0x1065: "ChartSiindex",
    0x1066: "ChartGelframe",
    0x1067: "ChartBoppcustom",
    0xFFFF: ""
}


all_funcs_by_name = {
    # Includes Analysis ToolPak aka ATP aka add-in aka xcall functions,
    # distinguished by -ve opcode.
    # name: (opcode, min # args, max # args, func return type, func arg types)
    # + in func arg types means more of the same.
    'ABS'         : ( 24, 1,  1, 'V', 'V'),
    'ACCRINT'     : ( -1, 6,  7, 'V', 'VVVVVVV'),
    'ACCRINTM'    : ( -1, 3,  5, 'V', 'VVVVV'),
    'ACOS'        : ( 99, 1,  1, 'V', 'V'),
    'ACOSH'       : (233, 1,  1, 'V', 'V'),
    'ADDRESS'     : (219, 2,  5, 'V', 'VVVVV'),
    'AMORDEGRC'   : ( -1, 7,  7, 'V', 'VVVVVVV'),
    'AMORLINC'    : ( -1, 7,  7, 'V', 'VVVVVVV'),
    'AND'         : ( 36, 1, 30, 'V', 'R+'),
    'AREAS'       : ( 75, 1,  1, 'V', 'R'),
    'ASC'         : (214, 1,  1, 'V', 'V'),
    'ASIN'        : ( 98, 1,  1, 'V', 'V'),
    'ASINH'       : (232, 1,  1, 'V', 'V'),
    'ATAN'        : ( 18, 1,  1, 'V', 'V'),
    'ATAN2'       : ( 97, 2,  2, 'V', 'VV'),
    'ATANH'       : (234, 1,  1, 'V', 'V'),
    'AVEDEV'      : (269, 1, 30, 'V', 'R+'),
    'AVERAGE'     : (  5, 1, 30, 'V', 'R+'),
    'AVERAGEA'    : (361, 1, 30, 'V', 'R+'),
    'BAHTTEXT'    : (368, 1,  1, 'V', 'V'),
    'BESSELI'     : ( -1, 2,  2, 'V', 'VV'),
    'BESSELJ'     : ( -1, 2,  2, 'V', 'VV'),
    'BESSELK'     : ( -1, 2,  2, 'V', 'VV'),
    'BESSELY'     : ( -1, 2,  2, 'V', 'VV'),
    'BETADIST'    : (270, 3,  5, 'V', 'VVVVV'),
    'BETAINV'     : (272, 3,  5, 'V', 'VVVVV'),
    'BIN2DEC'     : ( -1, 1,  1, 'V', 'V'),
    'BIN2HEX'     : ( -1, 1,  2, 'V', 'VV'),
    'BIN2OCT'     : ( -1, 1,  2, 'V', 'VV'),
    'BINOMDIST'   : (273, 4,  4, 'V', 'VVVV'),
    'CEILING'     : (288, 2,  2, 'V', 'VV'),
    'CELL'        : (125, 1,  2, 'V', 'VR'),
    'CHAR'        : (111, 1,  1, 'V', 'V'),
    'CHIDIST'     : (274, 2,  2, 'V', 'VV'),
    'CHIINV'      : (275, 2,  2, 'V', 'VV'),
    'CHITEST'     : (306, 2,  2, 'V', 'AA'),
    'CHOOSE'      : (100, 2, 30, 'R', 'VR+'),
    'CLEAN'       : (162, 1,  1, 'V', 'V'),
    'CODE'        : (121, 1,  1, 'V', 'V'),
    'COLUMN'      : (  9, 0,  1, 'V', 'R'),
    'COLUMNS'     : ( 77, 1,  1, 'V', 'R'),
    'COMBIN'      : (276, 2,  2, 'V', 'VV'),
    'COMPLEX'     : ( -1, 2,  3, 'V', 'VVV'),
    'CONCATENATE' : (336, 1, 30, 'V', 'V+'),
    'CONFIDENCE'  : (277, 3,  3, 'V', 'VVV'),
    'CONVERT'     : ( -1, 3,  3, 'V', 'VVV'),
    'CORREL'      : (307, 2,  2, 'V', 'AA'),
    'COS'         : ( 16, 1,  1, 'V', 'V'),
    'COSH'        : (230, 1,  1, 'V', 'V'),
    'COUNT'       : (  0, 1, 30, 'V', 'R+'),
    'COUNTA'      : (169, 1, 30, 'V', 'R+'),
    'COUNTBLANK'  : (347, 1,  1, 'V', 'R'),
    'COUNTIF'     : (346, 2,  2, 'V', 'RV'),
    'COUPDAYBS'   : ( -1, 3,  5, 'V', 'VVVVV'),
    'COUPDAYS'    : ( -1, 3,  5, 'V', 'VVVVV'),
    'COUPDAYSNC'  : ( -1, 3,  5, 'V', 'VVVVV'),
    'COUPNCD'     : ( -1, 3,  5, 'V', 'VVVVV'),
    'COUPNUM'     : ( -1, 3,  5, 'V', 'VVVVV'),
    'COUPPCD'     : ( -1, 3,  5, 'V', 'VVVVV'),
    'COVAR'       : (308, 2,  2, 'V', 'AA'),
    'CRITBINOM'   : (278, 3,  3, 'V', 'VVV'),
    'CUMIPMT'     : ( -1, 6,  6, 'V', 'VVVVVV'),
    'CUMPRINC'    : ( -1, 6,  6, 'V', 'VVVVVV'),
    'DATE'        : ( 65, 3,  3, 'V', 'VVV'),
    'DATEDIF'     : (351, 3,  3, 'V', 'VVV'),
    'DATEVALUE'   : (140, 1,  1, 'V', 'V'),
    'DAVERAGE'    : ( 42, 3,  3, 'V', 'RRR'),
    'DAY'         : ( 67, 1,  1, 'V', 'V'),
    'DAYS360'     : (220, 2,  3, 'V', 'VVV'),
    'DB'          : (247, 4,  5, 'V', 'VVVVV'),
    'DBCS'        : (215, 1,  1, 'V', 'V'),
    'DCOUNT'      : ( 40, 3,  3, 'V', 'RRR'),
    'DCOUNTA'     : (199, 3,  3, 'V', 'RRR'),
    'DDB'         : (144, 4,  5, 'V', 'VVVVV'),
    'DEC2BIN'     : ( -1, 1,  2, 'V', 'VV'),
    'DEC2HEX'     : ( -1, 1,  2, 'V', 'VV'),
    'DEC2OCT'     : ( -1, 1,  2, 'V', 'VV'),
    'DEGREES'     : (343, 1,  1, 'V', 'V'),
    'DELTA'       : ( -1, 1,  2, 'V', 'VV'),
    'DEVSQ'       : (318, 1, 30, 'V', 'R+'),
    'DGET'        : (235, 3,  3, 'V', 'RRR'),
    'DISC'        : ( -1, 4,  5, 'V', 'VVVVV'),
    'DMAX'        : ( 44, 3,  3, 'V', 'RRR'),
    'DMIN'        : ( 43, 3,  3, 'V', 'RRR'),
    'DOLLAR'      : ( 13, 1,  2, 'V', 'VV'),
    'DOLLARDE'    : ( -1, 2,  2, 'V', 'VV'),
    'DOLLARFR'    : ( -1, 2,  2, 'V', 'VV'),
    'DPRODUCT'    : (189, 3,  3, 'V', 'RRR'),
    'DSTDEV'      : ( 45, 3,  3, 'V', 'RRR'),
    'DSTDEVP'     : (195, 3,  3, 'V', 'RRR'),
    'DSUM'        : ( 41, 3,  3, 'V', 'RRR'),
    'DURATION'    : ( -1, 5,  6, 'V', 'VVVVVV'),
    'DVAR'        : ( 47, 3,  3, 'V', 'RRR'),
    'DVARP'       : (196, 3,  3, 'V', 'RRR'),
    'EDATE'       : ( -1, 2,  2, 'V', 'VV'),
    'EFFECT'      : ( -1, 2,  2, 'V', 'VV'),
    'EOMONTH'     : ( -1, 1,  2, 'V', 'VV'),
    'ERF'         : ( -1, 1,  2, 'V', 'VV'),
    'ERFC'        : ( -1, 1,  1, 'V', 'V'),
    'ERROR.TYPE'  : (261, 1,  1, 'V', 'V'),
    'EVEN'        : (279, 1,  1, 'V', 'V'),
    'EXACT'       : (117, 2,  2, 'V', 'VV'),
    'EXP'         : ( 21, 1,  1, 'V', 'V'),
    'EXPONDIST'   : (280, 3,  3, 'V', 'VVV'),
    'FACT'        : (184, 1,  1, 'V', 'V'),
    'FACTDOUBLE'  : ( -1, 1,  1, 'V', 'V'),
    'FALSE'       : ( 35, 0,  0, 'V', '-'),
    'FDIST'       : (281, 3,  3, 'V', 'VVV'),
    'FIND'        : (124, 2,  3, 'V', 'VVV'),
    'FINDB'       : (205, 2,  3, 'V', 'VVV'),
    'FINV'        : (282, 3,  3, 'V', 'VVV'),
    'FISHER'      : (283, 1,  1, 'V', 'V'),
    'FISHERINV'   : (284, 1,  1, 'V', 'V'),
    'FIXED'       : ( 14, 2,  3, 'V', 'VVV'),
    'FLOOR'       : (285, 2,  2, 'V', 'VV'),
    'FORECAST'    : (309, 3,  3, 'V', 'VAA'),
    'FREQUENCY'   : (252, 2,  2, 'A', 'RR'),
    'FTEST'       : (310, 2,  2, 'V', 'AA'),
    'FV'          : ( 57, 3,  5, 'V', 'VVVVV'),
    'FVSCHEDULE'  : ( -1, 2,  2, 'V', 'VA'),
    'GAMMADIST'   : (286, 4,  4, 'V', 'VVVV'),
    'GAMMAINV'    : (287, 3,  3, 'V', 'VVV'),
    'GAMMALN'     : (271, 1,  1, 'V', 'V'),
    'GCD'         : ( -1, 1, 29, 'V', 'V+'),
    'GEOMEAN'     : (319, 1, 30, 'V', 'R+'),
    'GESTEP'      : ( -1, 1,  2, 'V', 'VV'),
    'GETPIVOTDATA': (358, 2, 30, 'A', 'VAV+'),
    'GROWTH'      : ( 52, 1,  4, 'A', 'RRRV'),
    'HARMEAN'     : (320, 1, 30, 'V', 'R+'),
    'HEX2BIN'     : ( -1, 1,  2, 'V', 'VV'),
    'HEX2DEC'     : ( -1, 1,  1, 'V', 'V'),
    'HEX2OCT'     : ( -1, 1,  2, 'V', 'VV'),
    'HLOOKUP'     : (101, 3,  4, 'V', 'VRRV'),
    'HOUR'        : ( 71, 1,  1, 'V', 'V'),
    'HYPERLINK'   : (359, 1,  2, 'V', 'VV'),
    'HYPGEOMDIST' : (289, 4,  4, 'V', 'VVVV'),
    'IF'          : (  1, 2,  3, 'R', 'VRR'),
    'IMABS'       : ( -1, 1,  1, 'V', 'V'),
    'IMAGINARY'   : ( -1, 1,  1, 'V', 'V'),
    'IMARGUMENT'  : ( -1, 1,  1, 'V', 'V'),
    'IMCONJUGATE' : ( -1, 1,  1, 'V', 'V'),
    'IMCOS'       : ( -1, 1,  1, 'V', 'V'),
    'IMDIV'       : ( -1, 2,  2, 'V', 'VV'),
    'IMEXP'       : ( -1, 1,  1, 'V', 'V'),
    'IMLN'        : ( -1, 1,  1, 'V', 'V'),
    'IMLOG10'     : ( -1, 1,  1, 'V', 'V'),
    'IMLOG2'      : ( -1, 1,  1, 'V', 'V'),
    'IMPOWER'     : ( -1, 2,  2, 'V', 'VV'),
    'IMPRODUCT'   : ( -1, 2,  2, 'V', 'VV'),
    'IMREAL'      : ( -1, 1,  1, 'V', 'V'),
    'IMSIN'       : ( -1, 1,  1, 'V', 'V'),
    'IMSQRT'      : ( -1, 1,  1, 'V', 'V'),
    'IMSUB'       : ( -1, 2,  2, 'V', 'VV'),
    'IMSUM'       : ( -1, 1, 29, 'V', 'V+'),
    'INDEX'       : ( 29, 2,  4, 'R', 'RVVV'),
    'INDIRECT'    : (148, 1,  2, 'R', 'VV'),
    'INFO'        : (244, 1,  1, 'V', 'V'),
    'INT'         : ( 25, 1,  1, 'V', 'V'),
    'INTERCEPT'   : (311, 2,  2, 'V', 'AA'),
    'INTRATE'     : ( -1, 4,  5, 'V', 'VVVVV'),
    'IPMT'        : (167, 4,  6, 'V', 'VVVVVV'),
    'IRR'         : ( 62, 1,  2, 'V', 'RV'),
    'ISBLANK'     : (129, 1,  1, 'V', 'V'),
    'ISERR'       : (126, 1,  1, 'V', 'V'),
    'ISERROR'     : (  3, 1,  1, 'V', 'V'),
    'ISEVEN'      : ( -1, 1,  1, 'V', 'V'),
    'ISLOGICAL'   : (198, 1,  1, 'V', 'V'),
    'ISNA'        : (  2, 1,  1, 'V', 'V'),
    'ISNONTEXT'   : (190, 1,  1, 'V', 'V'),
    'ISNUMBER'    : (128, 1,  1, 'V', 'V'),
    'ISODD'       : ( -1, 1,  1, 'V', 'V'),
    'ISPMT'       : (350, 4,  4, 'V', 'VVVV'),
    'ISREF'       : (105, 1,  1, 'V', 'R'),
    'ISTEXT'      : (127, 1,  1, 'V', 'V'),
    'KURT'        : (322, 1, 30, 'V', 'R+'),
    'LARGE'       : (325, 2,  2, 'V', 'RV'),
    'LCM'         : ( -1, 1, 29, 'V', 'V+'),
    'LEFT'        : (115, 1,  2, 'V', 'VV'),
    'LEFTB'       : (208, 1,  2, 'V', 'VV'),
    'LEN'         : ( 32, 1,  1, 'V', 'V'),
    'LENB'        : (211, 1,  1, 'V', 'V'),
    'LINEST'      : ( 49, 1,  4, 'A', 'RRVV'),
    'LN'          : ( 22, 1,  1, 'V', 'V'),
    'LOG'         : (109, 1,  2, 'V', 'VV'),
    'LOG10'       : ( 23, 1,  1, 'V', 'V'),
    'LOGEST'      : ( 51, 1,  4, 'A', 'RRVV'),
    'LOGINV'      : (291, 3,  3, 'V', 'VVV'),
    'LOGNORMDIST' : (290, 3,  3, 'V', 'VVV'),
    'LOOKUP'      : ( 28, 2,  3, 'V', 'VRR'),
    'LOWER'       : (112, 1,  1, 'V', 'V'),
    'MATCH'       : ( 64, 2,  3, 'V', 'VRR'),
    'MAX'         : (  7, 1, 30, 'V', 'R+'),
    'MAXA'        : (362, 1, 30, 'V', 'R+'),
    'MDETERM'     : (163, 1,  1, 'V', 'A'),
    'MDURATION'   : ( -1, 5,  6, 'V', 'VVVVVV'),
    'MEDIAN'      : (227, 1, 30, 'V', 'R+'),
    'MID'         : ( 31, 3,  3, 'V', 'VVV'),
    'MIDB'        : (210, 3,  3, 'V', 'VVV'),
    'MIN'         : (  6, 1, 30, 'V', 'R+'),
    'MINA'        : (363, 1, 30, 'V', 'R+'),
    'MINUTE'      : ( 72, 1,  1, 'V', 'V'),
    'MINVERSE'    : (164, 1,  1, 'A', 'A'),
    'MIRR'        : ( 61, 3,  3, 'V', 'RVV'),
    'MMULT'       : (165, 2,  2, 'A', 'AA'),
    'MOD'         : ( 39, 2,  2, 'V', 'VV'),
    'MODE'        : (330, 1, 30, 'V', 'A+'),
    'MONTH'       : ( 68, 1,  1, 'V', 'V'),
    'MROUND'      : ( -1, 2,  2, 'V', 'VV'),
    'MULTINOMIAL' : ( -1, 1, 29, 'V', 'V+'),
    'N'           : (131, 1,  1, 'V', 'R'),
    'NA'          : ( 10, 0,  0, 'V', '-'),
    'NEGBINOMDIST': (292, 3,  3, 'V', 'VVV'),
    'NETWORKDAYS' : ( -1, 2,  3, 'V', 'VVR'),
    'NOMINAL'     : ( -1, 2,  2, 'V', 'VV'),
    'NORMDIST'    : (293, 4,  4, 'V', 'VVVV'),
    'NORMINV'     : (295, 3,  3, 'V', 'VVV'),
    'NORMSDIST'   : (294, 1,  1, 'V', 'V'),
    'NORMSINV'    : (296, 1,  1, 'V', 'V'),
    'NOT'         : ( 38, 1,  1, 'V', 'V'),
    'NOW'         : ( 74, 0,  0, 'V', '-'),
    'NPER'        : ( 58, 3,  5, 'V', 'VVVVV'),
    'NPV'         : ( 11, 2, 30, 'V', 'VR+'),
    'OCT2BIN'     : ( -1, 1,  2, 'V', 'VV'),
    'OCT2DEC'     : ( -1, 1,  1, 'V', 'V'),
    'OCT2HEX'     : ( -1, 1,  2, 'V', 'VV'),
    'ODD'         : (298, 1,  1, 'V', 'V'),
    'ODDFPRICE'   : ( -1, 9,  9, 'V', 'VVVVVVVVV'),
    'ODDFYIELD'   : ( -1, 9,  9, 'V', 'VVVVVVVVV'),
    'ODDLPRICE'   : ( -1, 8,  8, 'V', 'VVVVVVVV'),
    'ODDLYIELD'   : ( -1, 8,  8, 'V', 'VVVVVVVV'),
    'OFFSET'      : ( 78, 3,  5, 'R', 'RVVVV'),
    'OR'          : ( 37, 1, 30, 'V', 'R+'),
    'PEARSON'     : (312, 2,  2, 'V', 'AA'),
    'PERCENTILE'  : (328, 2,  2, 'V', 'RV'),
    'PERCENTRANK' : (329, 2,  3, 'V', 'RVV'),
    'PERMUT'      : (299, 2,  2, 'V', 'VV'),
    'PHONETIC'    : (360, 1,  1, 'V', 'R'),
    'PI'          : ( 19, 0,  0, 'V', '-'),
    'PMT'         : ( 59, 3,  5, 'V', 'VVVVV'),
    'POISSON'     : (300, 3,  3, 'V', 'VVV'),
    'POWER'       : (337, 2,  2, 'V', 'VV'),
    'PPMT'        : (168, 4,  6, 'V', 'VVVVVV'),
    'PRICE'       : ( -1, 6,  7, 'V', 'VVVVVVV'),
    'PRICEDISC'   : ( -1, 4,  5, 'V', 'VVVVV'),
    'PRICEMAT'    : ( -1, 5,  6, 'V', 'VVVVVV'),
    'PROB'        : (317, 3,  4, 'V', 'AAVV'),
    'PRODUCT'     : (183, 1, 30, 'V', 'R+'),
    'PROPER'      : (114, 1,  1, 'V', 'V'),
    'PV'          : ( 56, 3,  5, 'V', 'VVVVV'),
    'QUARTILE'    : (327, 2,  2, 'V', 'RV'),
    'QUOTIENT'    : ( -1, 2,  2, 'V', 'VV'),
    'RADIANS'     : (342, 1,  1, 'V', 'V'),
    'RAND'        : ( 63, 0,  0, 'V', '-'),
    'RANDBETWEEN' : ( -1, 2,  2, 'V', 'VV'),
    'RANK'        : (216, 2,  3, 'V', 'VRV'),
    'RATE'        : ( 60, 3,  6, 'V', 'VVVVVV'),
    'RECEIVED'    : ( -1, 4,  5, 'V', 'VVVVV'),
    'REPLACE'     : (119, 4,  4, 'V', 'VVVV'),
    'REPLACEB'    : (207, 4,  4, 'V', 'VVVV'),
    'REPT'        : ( 30, 2,  2, 'V', 'VV'),
    'RIGHT'       : (116, 1,  2, 'V', 'VV'),
    'RIGHTB'      : (209, 1,  2, 'V', 'VV'),
    'ROMAN'       : (354, 1,  2, 'V', 'VV'),
    'ROUND'       : ( 27, 2,  2, 'V', 'VV'),
    'ROUNDDOWN'   : (213, 2,  2, 'V', 'VV'),
    'ROUNDUP'     : (212, 2,  2, 'V', 'VV'),
    'ROW'         : (  8, 0,  1, 'V', 'R'),
    'ROWS'        : ( 76, 1,  1, 'V', 'R'),
    'RSQ'         : (313, 2,  2, 'V', 'AA'),
    'RTD'         : (379, 3, 30, 'A', 'VVV+'),
    'SEARCH'      : ( 82, 2,  3, 'V', 'VVV'),
    'SEARCHB'     : (206, 2,  3, 'V', 'VVV'),
    'SECOND'      : ( 73, 1,  1, 'V', 'V'),
    'SERIESSUM'   : ( -1, 4,  4, 'V', 'VVVA'),
    'SIGN'        : ( 26, 1,  1, 'V', 'V'),
    'SIN'         : ( 15, 1,  1, 'V', 'V'),
    'SINH'        : (229, 1,  1, 'V', 'V'),
    'SKEW'        : (323, 1, 30, 'V', 'R+'),
    'SLN'         : (142, 3,  3, 'V', 'VVV'),
    'SLOPE'       : (315, 2,  2, 'V', 'AA'),
    'SMALL'       : (326, 2,  2, 'V', 'RV'),
    'SQRT'        : ( 20, 1,  1, 'V', 'V'),
    'SQRTPI'      : ( -1, 1,  1, 'V', 'V'),
    'STANDARDIZE' : (297, 3,  3, 'V', 'VVV'),
    'STDEV'       : ( 12, 1, 30, 'V', 'R+'),
    'STDEVA'      : (366, 1, 30, 'V', 'R+'),
    'STDEVP'      : (193, 1, 30, 'V', 'R+'),
    'STDEVPA'     : (364, 1, 30, 'V', 'R+'),
    'STEYX'       : (314, 2,  2, 'V', 'AA'),
    'SUBSTITUTE'  : (120, 3,  4, 'V', 'VVVV'),
    'SUBTOTAL'    : (344, 2, 30, 'V', 'VR+'),
    'SUM'         : (  4, 1, 30, 'V', 'R+'),
    'SUMIF'       : (345, 2,  3, 'V', 'RVR'),
    'SUMPRODUCT'  : (228, 1, 30, 'V', 'A+'),
    'SUMSQ'       : (321, 1, 30, 'V', 'R+'),
    'SUMX2MY2'    : (304, 2,  2, 'V', 'AA'),
    'SUMX2PY2'    : (305, 2,  2, 'V', 'AA'),
    'SUMXMY2'     : (303, 2,  2, 'V', 'AA'),
    'SYD'         : (143, 4,  4, 'V', 'VVVV'),
    'T'           : (130, 1,  1, 'V', 'R'),
    'TAN'         : ( 17, 1,  1, 'V', 'V'),
    'TANH'        : (231, 1,  1, 'V', 'V'),
    'TBILLEQ'     : ( -1, 3,  3, 'V', 'VVV'),
    'TBILLPRICE'  : ( -1, 3,  3, 'V', 'VVV'),
    'TBILLYIELD'  : ( -1, 3,  3, 'V', 'VVV'),
    'TDIST'       : (301, 3,  3, 'V', 'VVV'),
    'TEXT'        : ( 48, 2,  2, 'V', 'VV'),
    'TIME'        : ( 66, 3,  3, 'V', 'VVV'),
    'TIMEVALUE'   : (141, 1,  1, 'V', 'V'),
    'TINV'        : (332, 2,  2, 'V', 'VV'),
    'TODAY'       : (221, 0,  0, 'V', '-'),
    'TRANSPOSE'   : ( 83, 1,  1, 'A', 'A'),
    'TREND'       : ( 50, 1,  4, 'A', 'RRRV'),
    'TRIM'        : (118, 1,  1, 'V', 'V'),
    'TRIMMEAN'    : (331, 2,  2, 'V', 'RV'),
    'TRUE'        : ( 34, 0,  0, 'V', '-'),
    'TRUNC'       : (197, 1,  2, 'V', 'VV'),
    'TTEST'       : (316, 4,  4, 'V', 'AAVV'),
    'TYPE'        : ( 86, 1,  1, 'V', 'V'),
    'UPPER'       : (113, 1,  1, 'V', 'V'),
    'USDOLLAR'    : (204, 1,  2, 'V', 'VV'),
    'VALUE'       : ( 33, 1,  1, 'V', 'V'),
    'VAR'         : ( 46, 1, 30, 'V', 'R+'),
    'VARA'        : (367, 1, 30, 'V', 'R+'),
    'VARP'        : (194, 1, 30, 'V', 'R+'),
    'VARPA'       : (365, 1, 30, 'V', 'R+'),
    'VDB'         : (222, 5,  7, 'V', 'VVVVVVV'),
    'VLOOKUP'     : (102, 3,  4, 'V', 'VRRV'),
    'WEEKDAY'     : ( 70, 1,  2, 'V', 'VV'),
    'WEEKNUM'     : ( -1, 1,  2, 'V', 'VV'),
    'WEIBULL'     : (302, 4,  4, 'V', 'VVVV'),
    'WORKDAY'     : ( -1, 2,  3, 'V', 'VVR'),
    'XIRR'        : ( -1, 2,  3, 'V', 'AAV'),
    'XNPV'        : ( -1, 3,  3, 'V', 'VAA'),
    'YEAR'        : ( 69, 1,  1, 'V', 'V'),
    'YEARFRAC'    : ( -1, 2,  3, 'V', 'VVV'),
    'YIELD'       : ( -1, 6,  7, 'V', 'VVVVVVV'),
    'YIELDDISC'   : ( -1, 4,  5, 'V', 'VVVVV'),
    'YIELDMAT'    : ( -1, 5,  6, 'V', 'VVVVVV'),
    'ZTEST'       : (324, 2,  3, 'V', 'RVV'),
    }

# Formulas Parse things

ptgExp          = 0x01
ptgTbl          = 0x02
ptgAdd          = 0x03
ptgSub          = 0x04
ptgMul          = 0x05
ptgDiv          = 0x06
ptgPower        = 0x07
ptgConcat       = 0x08
ptgLT           = 0x09
ptgLE           = 0x0a
ptgEQ           = 0x0b
ptgGE           = 0x0c
ptgGT           = 0x0d
ptgNE           = 0x0e
ptgIsect        = 0x0f
ptgUnion        = 0x10
ptgRange        = 0x11
ptgUplus        = 0x12
ptgUminus       = 0x13
ptgPercent      = 0x14
ptgParen        = 0x15
ptgMissArg      = 0x16
ptgStr          = 0x17
ptgExtend       = 0x18
ptgAttr         = 0x19
ptgSheet        = 0x1a
ptgEndSheet     = 0x1b
ptgErr          = 0x1c
ptgBool         = 0x1d
ptgInt          = 0x1e
ptgNum          = 0x1f

ptgArrayR       = 0x20
ptgFuncR        = 0x21
ptgFuncVarR     = 0x22
ptgNameR        = 0x23
ptgRefR         = 0x24
ptgAreaR        = 0x25
ptgMemAreaR     = 0x26
ptgMemErrR      = 0x27
ptgMemNoMemR    = 0x28
ptgMemFuncR     = 0x29
ptgRefErrR      = 0x2a
ptgAreaErrR     = 0x2b
ptgRefNR        = 0x2c
ptgAreaNR       = 0x2d
ptgMemAreaNR    = 0x2e
ptgMemNoMemNR   = 0x2f
ptgNameXR       = 0x39
ptgRef3dR       = 0x3a
ptgArea3dR      = 0x3b
ptgRefErr3dR    = 0x3c
ptgAreaErr3dR   = 0x3d

ptgArrayV       = 0x40
ptgFuncV        = 0x41
ptgFuncVarV     = 0x42
ptgNameV        = 0x43
ptgRefV         = 0x44
ptgAreaV        = 0x45
ptgMemAreaV     = 0x46
ptgMemErrV      = 0x47
ptgMemNoMemV    = 0x48
ptgMemFuncV     = 0x49
ptgRefErrV      = 0x4a
ptgAreaErrV     = 0x4b
ptgRefNV        = 0x4c
ptgAreaNV       = 0x4d
ptgMemAreaNV    = 0x4e
ptgMemNoMemNV   = 0x4f
ptgFuncCEV      = 0x58
ptgNameXV       = 0x59
ptgRef3dV       = 0x5a
ptgArea3dV      = 0x5b
ptgRefErr3dV    = 0x5c
ptgAreaErr3dV   = 0x5d

ptgArrayA       = 0x60
ptgFuncA        = 0x61
ptgFuncVarA     = 0x62
ptgNameA        = 0x63
ptgRefA         = 0x64
ptgAreaA        = 0x65
ptgMemAreaA     = 0x66
ptgMemErrA      = 0x67
ptgMemNoMemA    = 0x68
ptgMemFuncA     = 0x69
ptgRefErrA      = 0x6a
ptgAreaErrA     = 0x6b
ptgRefNA        = 0x6c
ptgAreaNA       = 0x6d
ptgMemAreaNA    = 0x6e
ptgMemNoMemNA   = 0x6f
ptgFuncCEA      = 0x78
ptgNameXA       = 0x79
ptgRef3dA       = 0x7a
ptgArea3dA      = 0x7b
ptgRefErr3dA    = 0x7c
ptgAreaErr3dA   = 0x7d


PtgNames = {
    ptgExp         : "ptgExp",
    ptgTbl         : "ptgTbl",
    ptgAdd         : "ptgAdd",
    ptgSub         : "ptgSub",
    ptgMul         : "ptgMul",
    ptgDiv         : "ptgDiv",
    ptgPower       : "ptgPower",
    ptgConcat      : "ptgConcat",
    ptgLT          : "ptgLT",
    ptgLE          : "ptgLE",
    ptgEQ          : "ptgEQ",
    ptgGE          : "ptgGE",
    ptgGT          : "ptgGT",
    ptgNE          : "ptgNE",
    ptgIsect       : "ptgIsect",
    ptgUnion       : "ptgUnion",
    ptgRange       : "ptgRange",
    ptgUplus       : "ptgUplus",
    ptgUminus      : "ptgUminus",
    ptgPercent     : "ptgPercent",
    ptgParen       : "ptgParen",
    ptgMissArg     : "ptgMissArg",
    ptgStr         : "ptgStr",
    ptgExtend      : "ptgExtend",
    ptgAttr        : "ptgAttr",
    ptgSheet       : "ptgSheet",
    ptgEndSheet    : "ptgEndSheet",
    ptgErr         : "ptgErr",
    ptgBool        : "ptgBool",
    ptgInt         : "ptgInt",
    ptgNum         : "ptgNum",
    ptgArrayR      : "ptgArrayR",
    ptgFuncR       : "ptgFuncR",
    ptgFuncVarR    : "ptgFuncVarR",
    ptgNameR       : "ptgNameR",
    ptgRefR        : "ptgRefR",
    ptgAreaR       : "ptgAreaR",
    ptgMemAreaR    : "ptgMemAreaR",
    ptgMemErrR     : "ptgMemErrR",
    ptgMemNoMemR   : "ptgMemNoMemR",
    ptgMemFuncR    : "ptgMemFuncR",
    ptgRefErrR     : "ptgRefErrR",
    ptgAreaErrR    : "ptgAreaErrR",
    ptgRefNR       : "ptgRefNR",
    ptgAreaNR      : "ptgAreaNR",
    ptgMemAreaNR   : "ptgMemAreaNR",
    ptgMemNoMemNR  : "ptgMemNoMemNR",
    ptgNameXR      : "ptgNameXR",
    ptgRef3dR      : "ptgRef3dR",
    ptgArea3dR     : "ptgArea3dR",
    ptgRefErr3dR   : "ptgRefErr3dR",
    ptgAreaErr3dR  : "ptgAreaErr3dR",
    ptgArrayV      : "ptgArrayV",
    ptgFuncV       : "ptgFuncV",
    ptgFuncVarV    : "ptgFuncVarV",
    ptgNameV       : "ptgNameV",
    ptgRefV        : "ptgRefV",
    ptgAreaV       : "ptgAreaV",
    ptgMemAreaV    : "ptgMemAreaV",
    ptgMemErrV     : "ptgMemErrV",
    ptgMemNoMemV   : "ptgMemNoMemV",
    ptgMemFuncV    : "ptgMemFuncV",
    ptgRefErrV     : "ptgRefErrV",
    ptgAreaErrV    : "ptgAreaErrV",
    ptgRefNV       : "ptgRefNV",
    ptgAreaNV      : "ptgAreaNV",
    ptgMemAreaNV   : "ptgMemAreaNV",
    ptgMemNoMemNV  : "ptgMemNoMemNV",
    ptgFuncCEV     : "ptgFuncCEV",
    ptgNameXV      : "ptgNameXV",
    ptgRef3dV      : "ptgRef3dV",
    ptgArea3dV     : "ptgArea3dV",
    ptgRefErr3dV   : "ptgRefErr3dV",
    ptgAreaErr3dV  : "ptgAreaErr3dV",
    ptgArrayA      : "ptgArrayA",
    ptgFuncA       : "ptgFuncA",
    ptgFuncVarA    : "ptgFuncVarA",
    ptgNameA       : "ptgNameA",
    ptgRefA        : "ptgRefA",
    ptgAreaA       : "ptgAreaA",
    ptgMemAreaA    : "ptgMemAreaA",
    ptgMemErrA     : "ptgMemErrA",
    ptgMemNoMemA   : "ptgMemNoMemA",
    ptgMemFuncA    : "ptgMemFuncA",
    ptgRefErrA     : "ptgRefErrA",
    ptgAreaErrA    : "ptgAreaErrA",
    ptgRefNA       : "ptgRefNA",
    ptgAreaNA      : "ptgAreaNA",
    ptgMemAreaNA   : "ptgMemAreaNA",
    ptgMemNoMemNA  : "ptgMemNoMemNA",
    ptgFuncCEA     : "ptgFuncCEA",
    ptgNameXA      : "ptgNameXA",
    ptgRef3dA      : "ptgRef3dA",
    ptgArea3dA     : "ptgArea3dA",
    ptgRefErr3dA   : "ptgRefErr3dA",
    ptgAreaErr3dA  : "ptgAreaErr3dA"
}


error_msg_by_code = {
    0x00: u"#NULL!",  # intersection of two cell ranges is empty
    0x07: u"#DIV/0!", # division by zero
    0x0F: u"#VALUE!", # wrong type of operand
    0x17: u"#REF!",   # illegal or deleted cell reference
    0x1D: u"#NAME?",  # wrong function or range name
    0x24: u"#NUM!",   # value range overflow
    0x2A: u"#N/A!"    # argument or function not available
}
