"""
   omx_ivcommon.py
   Python Conversion of OMX_IVCommon.h - OpenMax IL version 1.1.2
   by Binh Bui - 2014-09-25

/**
 * Copyright (c) 2008 The Khronos Group Inc. 
 * 
 * Permission is hereby granted, free of charge, to any person obtaining
 * a copy of this software and associated documentation files (the
 * "Software"), to deal in the Software without restriction, including
 * without limitation the rights to use, copy, modify, merge, publish,
 * distribute, sublicense, and/or sell copies of the Software, and to
 * permit persons to whom the Software is furnished to do so, subject
 * to the following conditions: 
 * The above copyright notice and this permission notice shall be included
 * in all copies or substantial portions of the Software. 
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
 * OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
 * IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
 * CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
 * TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 * SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE. 
 *
 */

/** 
 * @file OMX_IVCommon.h - OpenMax IL version 1.1.2
 *  The structures needed by Video and Image components to exchange
 *  parameters and configuration data with the components.
 */
"""


#**
#* Each OMX header must include all required header files to allow the header
#* to compile without errors.  The includes below are required for this header
#* file to compile successfully 
#*/

#include "OMX_Core.h"

from omx_core import *


#** @defgroup iv OpenMAX IL Imaging and Video Domain
#* Common structures for OpenMAX IL Imaging and Video domains
#* @{
#*/


#** 
#* Enumeration defining possible uncompressed image/video formats. 
#*
#* ENUMS:
#*  Unused                 : Placeholder value when format is N/A
#*  Monochrome             : black and white
#*  8bitRGB332             : Red 7:5, Green 4:2, Blue 1:0
#*  12bitRGB444            : Red 11:8, Green 7:4, Blue 3:0
#*  16bitARGB4444          : Alpha 15:12, Red 11:8, Green 7:4, Blue 3:0
#*  16bitARGB1555          : Alpha 15, Red 14:10, Green 9:5, Blue 4:0
#*  16bitRGB565            : Red 15:11, Green 10:5, Blue 4:0
#*  16bitBGR565            : Blue 15:11, Green 10:5, Red 4:0
#*  18bitRGB666            : Red 17:12, Green 11:6, Blue 5:0
#*  18bitARGB1665          : Alpha 17, Red 16:11, Green 10:5, Blue 4:0
#*  19bitARGB1666          : Alpha 18, Red 17:12, Green 11:6, Blue 5:0
#*  24bitRGB888            : Red 24:16, Green 15:8, Blue 7:0
#*  24bitBGR888            : Blue 24:16, Green 15:8, Red 7:0
#*  24bitARGB1887          : Alpha 23, Red 22:15, Green 14:7, Blue 6:0
#*  25bitARGB1888          : Alpha 24, Red 23:16, Green 15:8, Blue 7:0
#*  32bitBGRA8888          : Blue 31:24, Green 23:16, Red 15:8, Alpha 7:0
#*  32bitARGB8888          : Alpha 31:24, Red 23:16, Green 15:8, Blue 7:0
#*  YUV411Planar           : U,Y are subsampled by a factor of 4 horizontally
#*  YUV411PackedPlanar     : packed per payload in planar slices
#*  YUV420Planar           : Three arrays Y,U,V.
#*  YUV420PackedPlanar     : packed per payload in planar slices
#*  YUV420SemiPlanar       : Two arrays, one is all Y, the other is U and V
#*  YUV422Planar           : Three arrays Y,U,V.
#*  YUV422PackedPlanar     : packed per payload in planar slices
#*  YUV422SemiPlanar       : Two arrays, one is all Y, the other is U and V
#*  YCbYCr                 : Organized as 16bit YUYV (i.e. YCbYCr)
#*  YCrYCb                 : Organized as 16bit YVYU (i.e. YCrYCb)
#*  CbYCrY                 : Organized as 16bit UYVY (i.e. CbYCrY)
#*  CrYCbY                 : Organized as 16bit VYUY (i.e. CrYCbY)
#*  YUV444Interleaved      : Each pixel contains equal parts YUV
#*  RawBayer8bit           : SMIA camera output format
#*  RawBayer10bit          : SMIA camera output format
#*  RawBayer8bitcompressed : SMIA camera output format
#*  Vendor extensions
#*  32bitABGR888           : Alpha 31:24, Blue 23:16, Green 15:8, Red 7:0
#*/
OMX_COLOR_FORMATTYPE = OMX_U32

(   OMX_COLOR_FormatUnused,
    OMX_COLOR_FormatMonochrome,
    OMX_COLOR_Format8bitRGB332,
    OMX_COLOR_Format12bitRGB444,
    OMX_COLOR_Format16bitARGB4444,
    OMX_COLOR_Format16bitARGB1555,
    OMX_COLOR_Format16bitRGB565,
    OMX_COLOR_Format16bitBGR565,
    OMX_COLOR_Format18bitRGB666,
    OMX_COLOR_Format18bitARGB1665,
    OMX_COLOR_Format19bitARGB1666, 
    OMX_COLOR_Format24bitRGB888,
    OMX_COLOR_Format24bitBGR888,
    OMX_COLOR_Format24bitARGB1887,
    OMX_COLOR_Format25bitARGB1888,
    OMX_COLOR_Format32bitBGRA8888,
    OMX_COLOR_Format32bitARGB8888,
    OMX_COLOR_FormatYUV411Planar,
    OMX_COLOR_FormatYUV411PackedPlanar,
    OMX_COLOR_FormatYUV420Planar,
    OMX_COLOR_FormatYUV420PackedPlanar,
    OMX_COLOR_FormatYUV420SemiPlanar,
    OMX_COLOR_FormatYUV422Planar,
    OMX_COLOR_FormatYUV422PackedPlanar,
    OMX_COLOR_FormatYUV422SemiPlanar,
    OMX_COLOR_FormatYCbYCr,
    OMX_COLOR_FormatYCrYCb,
    OMX_COLOR_FormatCbYCrY,
    OMX_COLOR_FormatCrYCbY,
    OMX_COLOR_FormatYUV444Interleaved,
    OMX_COLOR_FormatRawBayer8bit,
    OMX_COLOR_FormatRawBayer10bit,
    OMX_COLOR_FormatRawBayer8bitcompressed,
    OMX_COLOR_FormatL2, 
    OMX_COLOR_FormatL4, 
    OMX_COLOR_FormatL8, 
    OMX_COLOR_FormatL16, 
    OMX_COLOR_FormatL24, 
    OMX_COLOR_FormatL32,
    OMX_COLOR_FormatYUV420PackedSemiPlanar,
    OMX_COLOR_FormatYUV422PackedSemiPlanar,
    OMX_COLOR_Format18BitBGR666,
    OMX_COLOR_Format24BitARGB6666,
    OMX_COLOR_Format24BitABGR6666 
    ) = range(44)

OMX_COLOR_FormatKhronosExtensions = 0x6F000000  #**< Reserved region for introducing Khronos Standard Extensions */ 
OMX_COLOR_FormatVendorStartUnused = 0x7F000000  #**< Reserved region for introducing Vendor Extensions */

(   OMX_COLOR_Format32bitABGR8888,
    OMX_COLOR_Format8bitPalette,
    OMX_COLOR_FormatYUVUV128,
    OMX_COLOR_FormatRawBayer12bit,
    OMX_COLOR_FormatBRCMEGL,
    OMX_COLOR_FormatBRCMOpaque,
    OMX_COLOR_FormatYVU420PackedPlanar,
    OMX_COLOR_FormatYVU420PackedSemiPlanar 
    ) = (0x7F000001 + i for i in range(8))

OMX_COLOR_FormatMax = 0x7FFFFFFF

#} OMX_COLOR_FORMATTYPE;

#** 
#* Defines the matrix for conversion from RGB to YUV or vice versa.
#* iColorMatrix should be initialized with the fixed point values 
#* used in converting between formats.
#*/
class OMX_CONFIG_COLORCONVERSIONTYPE(ctypes.Structure):
    _fields_ = [('nSize', OMX_U32),             #**< Size of the structure in bytes */
                ('nVersion', OMX_VERSIONTYPE),  #**< OMX specification version info */ 
                ('nPortIndex', OMX_U32),        #**< Port that this struct applies to */
                ('xColorMatrix', (OMX_S32 * 3) * 3), #**< Stored in signed Q16 format */
                ('xColorOffset', OMX_S32 * 4)]  #**< Stored in signed Q16 format */

#}OMX_CONFIG_COLORCONVERSIONTYPE;

#** 
#* Structure defining percent to scale each frame dimension.  For example:  
#* To make the width 50% larger, use fWidth = 1.5 and to make the width
#* 1/2 the original size, use fWidth = 0.5
#*/
class OMX_CONFIG_SCALEFACTORTYPE(ctypes.Structure):
    _fields_ = [('nSize', OMX_U32),             #**< Size of the structure in bytes */
                ('nVersion', OMX_VERSIONTYPE),  #**< OMX specification version info */ 
                ('nPortIndex', OMX_U32),        #**< Port that this struct applies to */
                ('xWidth', OMX_S32),            #**< Fixed point value stored as Q16 */
                ('xHeight', OMX_S32)]           #**< Fixed point value stored as Q16 */

#}OMX_CONFIG_SCALEFACTORTYPE;

#** 
#* Enumeration of possible image filter types 
#*/
OMX_IMAGEFILTERTYPE = OMX_U32

(   OMX_ImageFilterNone,
    OMX_ImageFilterNoise,
    OMX_ImageFilterEmboss,
    OMX_ImageFilterNegative,
    OMX_ImageFilterSketch,
    OMX_ImageFilterOilPaint,
    OMX_ImageFilterHatch,
    OMX_ImageFilterGpen,
    OMX_ImageFilterAntialias, 
    OMX_ImageFilterDeRing,       
    OMX_ImageFilterSolarize 
    ) = range(11)

OMX_ImageFilterKhronosExtensions = 0x6F000000  #**< Reserved region for introducing Khronos Standard Extensions */ 
OMX_ImageFilterVendorStartUnused = 0x7F000000  #**< Reserved region for introducing Vendor Extensions */
      
    #* Broadcom specific image filters */
(   OMX_ImageFilterWatercolor,
    OMX_ImageFilterPastel,
    OMX_ImageFilterSharpen,
    OMX_ImageFilterFilm,
    OMX_ImageFilterBlur,
    OMX_ImageFilterSaturation,

    OMX_ImageFilterDeInterlaceLineDouble,
    OMX_ImageFilterDeInterlaceAdvanced,
    
    OMX_ImageFilterColourSwap,
    OMX_ImageFilterWashedOut,
    OMX_ImageFilterColourPoint,
    OMX_ImageFilterPosterise,
    OMX_ImageFilterColourBalance,
    OMX_ImageFilterCartoon,

    OMX_ImageFilterAnaglyph,
    OMX_ImageFilterDeInterlaceFast 
    ) = (0x7F000001 + i for i in range(16))

OMX_ImageFilterMax = 0x7FFFFFFF

#} OMX_IMAGEFILTERTYPE;

OMX_IMAGEFILTERANAGLYPHTYPE = OMX_U32

(   OMX_ImageFilterAnaglyphNone,
    OMX_ImageFilterAnaglyphSBStoRedCyan,
    OMX_ImageFilterAnaglyphSBStoCyanRed,
    OMX_ImageFilterAnaglyphSBStoGreenMagenta,
    OMX_ImageFilterAnaglyphSBStoMagentaGreen,
    OMX_ImageFilterAnaglyphTABtoRedCyan,
    OMX_ImageFilterAnaglyphTABtoCyanRed,
    OMX_ImageFilterAnaglyphTABtoGreenMagenta,
    OMX_ImageFilterAnaglyphTABtoMagentaGreen 
    ) = range(9)

#} OMX_IMAGEFILTERANAGLYPHTYPE;

#** 
#* Image filter configuration 
#*
#* STRUCT MEMBERS:
#*  nSize        : Size of the structure in bytes       
#*  nVersion     : OMX specification version information
#*  nPortIndex   : Port that this structure applies to 
#*  eImageFilter : Image filter type enumeration      
#*/
class OMX_CONFIG_IMAGEFILTERTYPE(ctypes.Structure):
    _fields_ = [('nSize', OMX_U32),
                ('nVersion', OMX_VERSIONTYPE),
                ('nPortIndex', OMX_U32),
                ('eImageFilter', OMX_IMAGEFILTERTYPE)]

#} OMX_CONFIG_IMAGEFILTERTYPE;

#** 
#* Customized U and V for color enhancement 
#*
#* STRUCT MEMBERS:
#*  nSize             : Size of the structure in bytes
#*  nVersion          : OMX specification version information 
#*  nPortIndex        : Port that this structure applies to
#*  bColorEnhancement : Enable/disable color enhancement
#*  nCustomizedU      : Practical values: 16-240, range: 0-255, value set for 
#*                      U component
#*  nCustomizedV      : Practical values: 16-240, range: 0-255, value set for 
#*                      V component
#*/
class OMX_CONFIG_COLORENHANCEMENTTYPE(ctypes.Structure):
    _fields_ = [('nSize', OMX_U32),
                ('nVersion', OMX_VERSIONTYPE), 
                ('nPortIndex', OMX_U32),
                ('bColorEnhancement', OMX_BOOL),
                ('nCustomizedU', OMX_U8),
                ('nCustomizedV', OMX_U8)]

#} OMX_CONFIG_COLORENHANCEMENTTYPE;

#** 
#* Define color key and color key mask 
#*
#* STRUCT MEMBERS:
#*  nSize      : Size of the structure in bytes
#*  nVersion   : OMX specification version information 
#*  nPortIndex : Port that this structure applies to
#*  nARGBColor : 32bit Alpha, Red, Green, Blue Color
#*  nARGBMask  : 32bit Mask for Alpha, Red, Green, Blue channels
#*/
class OMX_CONFIG_COLORKEYTYPE(ctypes.Structure):
    _fields_ = [('nSize', OMX_U32),
                ('nVersion', OMX_VERSIONTYPE),
                ('nPortIndex', OMX_U32),
                ('nARGBColor', OMX_U32),
                ('nARGBMask', OMX_U32)]

#} OMX_CONFIG_COLORKEYTYPE;

#** 
#* List of color blend types for pre/post processing 
#*
#* ENUMS:
#*  None          : No color blending present
#*  AlphaConstant : Function is (alpha_constant * src) + 
#*                  (1 - alpha_constant) * dst)
#*  AlphaPerPixel : Function is (alpha * src) + (1 - alpha) * dst)
#*  Alternate     : Function is alternating pixels from src and dst
#*  And           : Function is (src & dst)
#*  Or            : Function is (src | dst)
#*  Invert        : Function is ~src
#*/
OMX_COLORBLENDTYPE = OMX_U32

(   OMX_ColorBlendNone,
    OMX_ColorBlendAlphaConstant,
    OMX_ColorBlendAlphaPerPixel,
    OMX_ColorBlendAlternate,
    OMX_ColorBlendAnd,
    OMX_ColorBlendOr,
    OMX_ColorBlendInvert 
    ) = range(7)

OMX_ColorBlendKhronosExtensions = 0x6F000000  #**< Reserved region for introducing Khronos Standard Extensions */ 
OMX_ColorBlendVendorStartUnused = 0x7F000000  #**< Reserved region for introducing Vendor Extensions */

OMX_ColorBlendMax = 0x7FFFFFFF

#} OMX_COLORBLENDTYPE;

#** 
#* Color blend configuration 
#*
#* STRUCT MEMBERS:
#*  nSize             : Size of the structure in bytes                        
#*  nVersion          : OMX specification version information                
#*  nPortIndex        : Port that this structure applies to                   
#*  nRGBAlphaConstant : Constant global alpha values when global alpha is used
#*  eColorBlend       : Color blend type enumeration                         
#*/
class OMX_CONFIG_COLORBLENDTYPE(ctypes.Structure):
    _fields_ = [('nSize', OMX_U32),
                ('nVersion', OMX_VERSIONTYPE),
                ('nPortIndex', OMX_U32),
                ('nRGBAlphaConstant', OMX_U32),
                ('eColorBlend', OMX_COLORBLENDTYPE)]

#} OMX_CONFIG_COLORBLENDTYPE;

#** 
#* Hold frame dimension
#*
#* STRUCT MEMBERS:
#*  nSize      : Size of the structure in bytes      
#*  nVersion   : OMX specification version information
#*  nPortIndex : Port that this structure applies to     
#*  nWidth     : Frame width in pixels                 
#*  nHeight    : Frame height in pixels                
#*/
class OMX_FRAMESIZETYPE(ctypes.Structure):
    _fields_ = [('nSize', OMX_U32),
                ('nVersion', OMX_VERSIONTYPE),
                ('nPortIndex', OMX_U32),
                ('nWidth', OMX_U32),
                ('nHeight', OMX_U32)]

#} OMX_FRAMESIZETYPE;

#**
#* Rotation configuration 
#*
#* STRUCT MEMBERS:
#*  nSize      : Size of the structure in bytes             
#*  nVersion   : OMX specification version information
#*  nPortIndex : Port that this structure applies to
#*  nRotation  : +/- integer rotation value               
#*/
class OMX_CONFIG_ROTATIONTYPE(ctypes.Structure):
    _fields_ = [('nSize', OMX_U32),
                ('nVersion', OMX_VERSIONTYPE),
                ('nPortIndex', OMX_U32),
                ('nRotation', OMX_S32)] 

#} OMX_CONFIG_ROTATIONTYPE;

#** 
#* Possible mirroring directions for pre/post processing 
#*
#* ENUMS:
#*  None       : No mirroring                         
#*  Vertical   : Vertical mirroring, flip on X axis   
#*  Horizontal : Horizontal mirroring, flip on Y axis  
#*  Both       : Both vertical and horizontal mirroring
#*/
OMX_MIRRORTYPE = OMX_U32

(   OMX_MirrorNone,         # = 0,
    OMX_MirrorVertical,
    OMX_MirrorHorizontal,
    OMX_MirrorBoth  
    ) = range(4)

OMX_MirrorKhronosExtensions = 0x6F000000  #**< Reserved region for introducing Khronos Standard Extensions */ 
OMX_MirrorVendorStartUnused = 0x7F000000  #**< Reserved region for introducing Vendor Extensions */

OMX_MirrorMax = 0x7FFFFFFF   

#} OMX_MIRRORTYPE;

#** 
#* Mirroring configuration 
#*
#* STRUCT MEMBERS:
#*  nSize      : Size of the structure in bytes      
#*  nVersion   : OMX specification version information
#*  nPortIndex : Port that this structure applies to  
#*  eMirror    : Mirror type enumeration              
#*/
class OMX_CONFIG_MIRRORTYPE(ctypes.Structure):
    _fields_ = [('nSize', OMX_U32),
                ('nVersion', OMX_VERSIONTYPE), 
                ('nPortIndex', OMX_U32),
                ('eMirror', OMX_MIRRORTYPE)]

#} OMX_CONFIG_MIRRORTYPE;

#** 
#* Position information only 
#*
#* STRUCT MEMBERS:
#*  nSize      : Size of the structure in bytes               
#*  nVersion   : OMX specification version information
#*  nPortIndex : Port that this structure applies to
#*  nX         : X coordinate for the point                     
#*  nY         : Y coordinate for the point 
#*/                      
class OMX_CONFIG_POINTTYPE(ctypes.Structure):
    _fields_ = [('nSize', OMX_U32),
                ('nVersion', OMX_VERSIONTYPE),
                ('nPortIndex', OMX_U32),
                ('nX', OMX_S32),
                ('nY', OMX_S32)]

#} OMX_CONFIG_POINTTYPE;

#** 
#* Frame size plus position 
#*
#* STRUCT MEMBERS:
#*  nSize      : Size of the structure in bytes                    
#*  nVersion   : OMX specification version information      
#*  nPortIndex : Port that this structure applies to    
#*  nLeft      : X Coordinate of the top left corner of the rectangle
#*  nTop       : Y Coordinate of the top left corner of the rectangle
#*  nWidth     : Width of the rectangle                              
#*  nHeight    : Height of the rectangle                             
#*/
class OMX_CONFIG_RECTTYPE(ctypes.Structure):
    _fields_ = [('nSize', OMX_U32),
                ('nVersion', OMX_VERSIONTYPE),  
                ('nPortIndex', OMX_U32), 
                ('nLeft', OMX_S32), 
                ('nTop', OMX_S32),
                ('nWidth', OMX_U32),
                ('nHeight', OMX_U32)]

#} OMX_CONFIG_RECTTYPE;

#** 
#* Deblocking state; it is required to be set up before starting the codec 
#*
#* STRUCT MEMBERS:
#*  nSize       : Size of the structure in bytes      
#*  nVersion    : OMX specification version information 
#*  nPortIndex  : Port that this structure applies to
#*  bDeblocking : Enable/disable deblocking mode    
#*/
class OMX_PARAM_DEBLOCKINGTYPE(ctypes.Structure):
    _fields_ = [('nSize', OMX_U32),
                ('nVersion', OMX_VERSIONTYPE),
                ('nPortIndex', OMX_U32),
                ('bDeblocking', OMX_BOOL)]

#} OMX_PARAM_DEBLOCKINGTYPE;

#** 
#* Stabilization state 
#*
#* STRUCT MEMBERS:
#*  nSize      : Size of the structure in bytes          
#*  nVersion   : OMX specification version information    
#*  nPortIndex : Port that this structure applies to   
#*  bStab      : Enable/disable frame stabilization state
#*/
class OMX_CONFIG_FRAMESTABTYPE(ctypes.Structure):
    _fields_ = [('nSize', OMX_U32),
                ('nVersion', OMX_VERSIONTYPE),
                ('nPortIndex', OMX_U32),
                ('bStab', OMX_BOOL)]

#} OMX_CONFIG_FRAMESTABTYPE;

#** 
#* White Balance control type 
#*
#* STRUCT MEMBERS:
#*  SunLight : Referenced in JSR-234
#*  Flash    : Optimal for device's integrated flash
#*/
OMX_WHITEBALCONTROLTYPE = OMX_U32

(   OMX_WhiteBalControlOff,                 # = 0,
    OMX_WhiteBalControlAuto,
    OMX_WhiteBalControlSunLight,
    OMX_WhiteBalControlCloudy,
    OMX_WhiteBalControlShade,
    OMX_WhiteBalControlTungsten,
    OMX_WhiteBalControlFluorescent,
    OMX_WhiteBalControlIncandescent,
    OMX_WhiteBalControlFlash,
    OMX_WhiteBalControlHorizon 
    ) = range(10)

OMX_WhiteBalControlKhronosExtensions = 0x6F000000  #**< Reserved region for introducing Khronos Standard Extensions */ 
OMX_WhiteBalControlVendorStartUnused = 0x7F000000  #**< Reserved region for introducing Vendor Extensions */

OMX_WhiteBalControlMax = 0x7FFFFFFF

#} OMX_WHITEBALCONTROLTYPE;

#** 
#* White Balance control configuration 
#*
#* STRUCT MEMBERS:
#*  nSize            : Size of the structure in bytes       
#*  nVersion         : OMX specification version information
#*  nPortIndex       : Port that this structure applies to                 
#*  eWhiteBalControl : White balance enumeration            
#*/
class OMX_CONFIG_WHITEBALCONTROLTYPE(ctypes.Structure):
    _fields_ = [('nSize', OMX_U32),
                ('nVersion', OMX_VERSIONTYPE),
                ('nPortIndex', OMX_U32),
                ('eWhiteBalControl', OMX_WHITEBALCONTROLTYPE)]

#} OMX_CONFIG_WHITEBALCONTROLTYPE;

#** 
#* Exposure control type 
#*/
OMX_EXPOSURECONTROLTYPE = OMX_U32

(   OMX_ExposureControlOff,                 # = 0,
    OMX_ExposureControlAuto,
    OMX_ExposureControlNight,
    OMX_ExposureControlBackLight,
    OMX_ExposureControlSpotLight,
    OMX_ExposureControlSports,
    OMX_ExposureControlSnow,
    OMX_ExposureControlBeach,
    OMX_ExposureControlLargeAperture,
    OMX_ExposureControlSmallAperture 
    ) = range(10)

OMX_ExposureControlKhronosExtensions = 0x6F000000  #**< Reserved region for introducing Khronos Standard Extensions */ 
OMX_ExposureControlVendorStartUnused = 0x7F000000  #**< Reserved region for introducing Vendor Extensions */

(   OMX_ExposureControlVeryLong,
    OMX_ExposureControlFixedFps,
    OMX_ExposureControlNightWithPreview,
    OMX_ExposureControlAntishake,
    OMX_ExposureControlFireworks 
    ) = (0x7F000001 + i for i in range(5))

OMX_ExposureControlMax = 0x7FFFFFFF

#} OMX_EXPOSURECONTROLTYPE;

#** 
#* White Balance control configuration 
#*
#* STRUCT MEMBERS:
#*  nSize            : Size of the structure in bytes      
#*  nVersion         : OMX specification version information
#*  nPortIndex       : Port that this structure applies to                
#*  eExposureControl : Exposure control enumeration         
#*/
class OMX_CONFIG_EXPOSURECONTROLTYPE(ctypes.Structure):
    _fields_ = [('nSize', OMX_U32),
                ('nVersion', OMX_VERSIONTYPE),
                ('nPortIndex', OMX_U32),
                ('eExposureControl', OMX_EXPOSURECONTROLTYPE)]

#} OMX_CONFIG_EXPOSURECONTROLTYPE;

#** 
#* Defines sensor supported mode. 
#*
#* STRUCT MEMBERS:
#*  nSize      : Size of the structure in bytes           
#*  nVersion   : OMX specification version information
#*  nPortIndex : Port that this structure applies to 
#*  nFrameRate : Single shot mode is indicated by a 0     
#*  bOneShot   : Enable for single shot, disable for streaming
#*  sFrameSize : Framesize                                          
#*/
class OMX_PARAM_SENSORMODETYPE(ctypes.Structure):
    _fields_ = [('nSize', OMX_U32),
                ('nVersion', OMX_VERSIONTYPE),
                ('nPortIndex', OMX_U32),
                ('nFrameRate', OMX_U32),
                ('bOneShot', OMX_BOOL),
                ('sFrameSize', OMX_FRAMESIZETYPE)]

#} OMX_PARAM_SENSORMODETYPE;

#** 
#* Defines contrast level 
#*
#* STRUCT MEMBERS:
#*  nSize      : Size of the structure in bytes                              
#*  nVersion   : OMX specification version information                
#*  nPortIndex : Port that this structure applies to                 
#*  nContrast  : Values allowed for contrast -100 to 100, zero means no change
#*/
class OMX_CONFIG_CONTRASTTYPE(ctypes.Structure):
    _fields_ = [('nSize', OMX_U32),
                ('nVersion', OMX_VERSIONTYPE),
                ('nPortIndex', OMX_U32),
                ('nContrast', OMX_S32)]

#} OMX_CONFIG_CONTRASTTYPE;

#** 
#* Defines brightness level 
#*
#* STRUCT MEMBERS:
#*  nSize       : Size of the structure in bytes          
#*  nVersion    : OMX specification version information 
#*  nPortIndex  : Port that this structure applies to 
#*  nBrightness : 0-100%        
#*/
class OMX_CONFIG_BRIGHTNESSTYPE(ctypes.Structure):
    _fields_ = [('nSize', OMX_U32),
                ('nVersion', OMX_VERSIONTYPE),
                ('nPortIndex', OMX_U32),
                ('nBrightness', OMX_U32)]

#} OMX_CONFIG_BRIGHTNESSTYPE;

#** 
#* Defines backlight level configuration for a video sink, e.g. LCD panel 
#*
#* STRUCT MEMBERS:
#*  nSize      : Size of the structure in bytes
#*  nVersion   : OMX specification version information 
#*  nPortIndex : Port that this structure applies to
#*  nBacklight : Values allowed for backlight 0-100%
#*  nTimeout   : Number of milliseconds before backlight automatically turns 
#*               off.  A value of 0x0 disables backight timeout 
#*/
class OMX_CONFIG_BACKLIGHTTYPE(ctypes.Structure):
    _fields_ = [('nSize', OMX_U32),
                ('nVersion', OMX_VERSIONTYPE),
                ('nPortIndex', OMX_U32),
                ('nBacklight', OMX_U32),
                ('nTimeout', OMX_U32)]

#} OMX_CONFIG_BACKLIGHTTYPE;

#** 
#* Defines setting for Gamma 
#*
#* STRUCT MEMBERS:
#*  nSize      : Size of the structure in bytes
#*  nVersion   : OMX specification version information 
#*  nPortIndex : Port that this structure applies to
#*  nGamma     : Values allowed for gamma -100 to 100, zero means no change
#*/
class OMX_CONFIG_GAMMATYPE(ctypes.Structure):
    _fields_ = [('nSize', OMX_U32),
                ('nVersion', OMX_VERSIONTYPE),
                ('nPortIndex', OMX_U32),
                ('nGamma', OMX_S32)]

#} OMX_CONFIG_GAMMATYPE;

#** 
#* Define for setting saturation 
#* 
#* STRUCT MEMBERS:
#*  nSize       : Size of the structure in bytes
#*  nVersion    : OMX specification version information
#*  nPortIndex  : Port that this structure applies to
#*  nSaturation : Values allowed for saturation -100 to 100, zero means 
#*                no change
#*/
class OMX_CONFIG_SATURATIONTYPE(ctypes.Structure):
    _fields_ = [('nSize', OMX_U32),
                ('nVersion', OMX_VERSIONTYPE),
                ('nPortIndex', OMX_U32),
                ('nSaturation', OMX_S32)]

#} OMX_CONFIG_SATURATIONTYPE;

#** 
#* Define for setting Lightness 
#*
#* STRUCT MEMBERS:
#*  nSize      : Size of the structure in bytes
#*  nVersion   : OMX specification version information
#*  nPortIndex : Port that this structure applies to
#*  nLightness : Values allowed for lightness -100 to 100, zero means no 
#*               change
#*/
class OMX_CONFIG_LIGHTNESSTYPE(ctypes.Structure):
    _fields_ = [('nSize', OMX_U32),
                ('nVersion', OMX_VERSIONTYPE),
                ('nPortIndex', OMX_U32),
                ('nLightness', OMX_S32)]

#} OMX_CONFIG_LIGHTNESSTYPE;

#** 
#* Plane blend configuration 
#*
#* STRUCT MEMBERS:
#*  nSize      : Size of the structure in bytes 
#*  nVersion   : OMX specification version information
#*  nPortIndex : Index of input port associated with the plane.
#*  nDepth     : Depth of the plane in relation to the screen. Higher 
#*               numbered depths are "behind" lower number depths.  
#*               This number defaults to the Port Index number.
#*  nAlpha     : Transparency blending component for the entire plane.  
#*               See blending modes for more detail.
#*/
class OMX_CONFIG_PLANEBLENDTYPE(ctypes.Structure):
    _fields_ = [('nSize', OMX_U32),
                ('nVersion', OMX_VERSIONTYPE),
                ('nPortIndex', OMX_U32),
                ('nDepth', OMX_U32),
                ('nAlpha', OMX_U32)]

#} OMX_CONFIG_PLANEBLENDTYPE;

#** 
#* Define interlace type
#*
#* STRUCT MEMBERS:
#*  nSize                 : Size of the structure in bytes 
#*  nVersion              : OMX specification version information 
#*  nPortIndex            : Port that this structure applies to
#*  bEnable               : Enable control variable for this functionality 
#*                          (see below)
#*  nInterleavePortIndex  : Index of input or output port associated with  
#*                          the interleaved plane. 
#*  pPlanarPortIndexes[4] : Index of input or output planar ports.
#*/
class OMX_PARAM_INTERLEAVETYPE(ctypes.Structure):
    _fields_ = [('nSize', OMX_U32),
                ('nVersion', OMX_VERSIONTYPE),
                ('nPortIndex', OMX_U32),
                ('bEnable', OMX_BOOL),
                ('nInterleavePortIndex', OMX_U32)]

#} OMX_PARAM_INTERLEAVETYPE;

#** 
#* Defines the picture effect used for an input picture 
#*/
OMX_TRANSITIONEFFECTTYPE = OMX_U32

(   OMX_EffectNone,
    OMX_EffectFadeFromBlack,
    OMX_EffectFadeToBlack,
    OMX_EffectUnspecifiedThroughConstantColor,
    OMX_EffectDissolve,
    OMX_EffectWipe,
    OMX_EffectUnspecifiedMixOfTwoScenes 
    ) = range(7)

OMX_EffectKhronosExtensions = 0x6F000000  #**< Reserved region for introducing Khronos Standard Extensions */ 
OMX_EffectVendorStartUnused = 0x7F000000  #**< Reserved region for introducing Vendor Extensions */

(   OMX_EffectReverseUnspecifiedMixOfTwoScenes,
    
#ifndef __VIDEOCORE4__
    OMX_EffectDiagonalWipe,
    OMX_EffectDiagonalWipeRotate,
    OMX_EffectEllipticalWipe,
    OMX_EffectEllipticalWipeRotate,
    OMX_EffectInverseEllipticalWipe,
    OMX_EffectInverseEllipticalWipeRotate,
    OMX_EffectGlassWipe,
    OMX_EffectGlassWipeRotate,
    OMX_EffectWavyWipe,
    OMX_EffectWavyWipeRotate,
    OMX_EffectMunchingSquares,
    OMX_EffectStripeWipe,
    OMX_EffectStripeWipeRotate,
    
    OMX_EffectRotozoomUnmatched,
    OMX_EffectRotozoomMatched,
    OMX_EffectRotozoomGentle,
#endif

    OMX_EffectMunchRandom,
    OMX_EffectMunchVRandom,
    OMX_EffectMunchHRandom,
    OMX_EffectMunchWipe,
    OMX_EffectMunchMunch,
    OMX_EffectMunchStripe,
    OMX_EffectFadeRandom,
    OMX_EffectFadeVRandom,
    OMX_EffectFadeHRandom,
    OMX_EffectFadeWipe,
    OMX_EffectFadeMunch,
    OMX_EffectFadeStripe,
    OMX_EffectColourBlockRandom,
    OMX_EffectColourBlockVRandom,
    OMX_EffectColourBlockHRandom,
    OMX_EffectColourBlockWipe,
    OMX_EffectColourBlockMunch,
    OMX_EffectColourBlockStripe,
    OMX_EffectColourBlock2Random,
    OMX_EffectColourBlock2VRandom,
    OMX_EffectColourBlock2HRandom,
    OMX_EffectColourBlock2Wipe,
    OMX_EffectColourBlock2Munch,
    OMX_EffectColourBlock2Stripe,
    OMX_EffectShadeRandom,
    OMX_EffectShadeVRandom,
    OMX_EffectShadeHRandom,
    OMX_EffectShadeWipe,
    OMX_EffectShadeMunch,
    OMX_EffectShadeStripe,
    OMX_EffectBitmaskRandom,
    OMX_EffectBitmaskVRandom,
    OMX_EffectBitmaskHRandom,
    OMX_EffectBitmaskWipe,
    OMX_EffectBitmaskMunch,
    OMX_EffectBitmaskStripe,
    OMX_EffectBitmask2Random,
    OMX_EffectBitmask2VRandom,
    OMX_EffectBitmask2HRandom,
    OMX_EffectBitmask2Wipe,
    OMX_EffectBitmask2Munch,
    OMX_EffectBitmask2Stripe,
    OMX_EffectBitmask2ColourRandom,
    OMX_EffectBitmask2ColourVRandom,
    OMX_EffectBitmask2ColourHRandom,
    OMX_EffectBitmask2ColourWipe,
    OMX_EffectBitmask2ColourMunch,
    OMX_EffectBitmask2ColourStripe,

    OMX_EffectPushRight,
    OMX_EffectPushLeft,
    OMX_EffectPushDown,
    OMX_EffectPushUp,
    OMX_EffectCoverRight,
    OMX_EffectCoverLeft,
    OMX_EffectCoverDown,
    OMX_EffectCoverUp,
    OMX_EffectRevealRight,
    OMX_EffectRevealLeft,
    OMX_EffectRevealDown,
    OMX_EffectRevealUp,
    OMX_EffectWipeRight,
    OMX_EffectWipeLeft,
    OMX_EffectWipeDown,
    OMX_EffectWipeUp,
    OMX_EffectSpeckle,
    OMX_EffectCircle,
    OMX_EffectSpiral,
    OMX_EffectDiamond,
    OMX_EffectVert,
    OMX_EffectPlus,
    OMX_EffectClock,
    OMX_EffectPlasma,
    OMX_EffectDisplace,
    OMX_EffectGenie,
    OMX_EffectSide,
    OMX_EffectMaze,
    OMX_EffectRipple,
    OMX_EffectStar,
    OMX_EffectAlpha,
    OMX_EffectIntense,
    OMX_EffectIntenseU,
    OMX_EffectIntenseV,
    OMX_EffectInverseIntense,
    OMX_EffectInverseIntenseU,
    OMX_EffectInverseIntenseV,

    OMX_EffectPageTurn,

    OMX_EffectFlipPlaneDown,
    OMX_EffectFlipPlaneDownMid,
    OMX_EffectFlipPlaneDownHigh,
    OMX_EffectFlipPlaneLeft,
    OMX_EffectFlipPlaneLeftMid,
    OMX_EffectFlipPlaneLeftHigh,
    OMX_EffectFlipCubeDown,
    OMX_EffectFlipCubeDownMid,
    OMX_EffectFlipCubeDownHigh,
    OMX_EffectFlipCubeLeft,
    OMX_EffectFlipCubeLeftMid,
    OMX_EffectFlipCubeLeftHigh 
    ) = (0x7F000001 + i for i in range(115))

OMX_EffectMax = 0x7FFFFFFF

#} OMX_TRANSITIONEFFECTTYPE;

#** 
#* Structure used to configure current transition effect 
#*
#* STRUCT MEMBERS:
#* nSize      : Size of the structure in bytes
#* nVersion   : OMX specification version information 
#* nPortIndex : Port that this structure applies to
#* eEffect    : Effect to enable
#*/
class OMX_CONFIG_TRANSITIONEFFECTTYPE(ctypes.Structure):
    _fields_ = [('nSize', OMX_U32),
                ('nVersion', OMX_VERSIONTYPE),
                ('nPortIndex', OMX_U32),
                ('eEffect', OMX_TRANSITIONEFFECTTYPE)]

#} OMX_CONFIG_TRANSITIONEFFECTTYPE;

#** 
#* Defines possible data unit types for encoded video data. The data unit 
#* types are used both for encoded video input for playback as well as
#* encoded video output from recording. 
#*/
OMX_DATAUNITTYPE = OMX_U32

(   OMX_DataUnitCodedPicture,
    OMX_DataUnitVideoSegment,
    OMX_DataUnitSeveralSegments,
    OMX_DataUnitArbitraryStreamSection 
    ) = range(4)

OMX_DataUnitKhronosExtensions = 0x6F000000  #**< Reserved region for introducing Khronos Standard Extensions */ 
OMX_DataUnitVendorStartUnused = 0x7F000000  #**< Reserved region for introducing Vendor Extensions */

OMX_DataUnitMax = 0x7FFFFFFF

#} OMX_DATAUNITTYPE;

#** 
#* Defines possible encapsulation types for coded video data unit. The 
#* encapsulation information is used both for encoded video input for 
#* playback as well as encoded video output from recording. 
#*/
OMX_DATAUNITENCAPSULATIONTYPE = OMX_U32

(   OMX_DataEncapsulationElementaryStream,
    OMX_DataEncapsulationGenericPayload,
    OMX_DataEncapsulationRtpPayload 
    ) = range(3)

OMX_DataEncapsulationKhronosExtensions = 0x6F000000  #**< Reserved region for introducing Khronos Standard Extensions */ 
OMX_DataEncapsulationVendorStartUnused = 0x7F000000  #**< Reserved region for introducing Vendor Extensions */

OMX_DataEncapsulationMax = 0x7FFFFFFF

#} OMX_DATAUNITENCAPSULATIONTYPE;

#** 
#* Structure used to configure the type of being decoded/encoded 
#*/
class OMX_PARAM_DATAUNITTYPE(ctypes.Structure):
    _fields_ = [('nSize', OMX_U32),             #**< Size of the structure in bytes */
                ('nVersion', OMX_VERSIONTYPE),  #**< OMX specification version information */ 
                ('nPortIndex', OMX_U32),        #**< Port that this structure applies to */
                ('eUnitType', OMX_DATAUNITTYPE),
                ('eEncapsulationType', OMX_DATAUNITENCAPSULATIONTYPE)]

#} OMX_PARAM_DATAUNITTYPE;

#**
#* Defines dither types 
#*/
OMX_DITHERTYPE = OMX_U32

(   OMX_DitherNone,
    OMX_DitherOrdered,
    OMX_DitherErrorDiffusion,
    OMX_DitherOther 
    ) = range(4)

OMX_DitherKhronosExtensions = 0x6F000000  #**< Reserved region for introducing Khronos Standard Extensions */ 
OMX_DitherVendorStartUnused = 0x7F000000  #**< Reserved region for introducing Vendor Extensions */

OMX_DitherMax = 0x7FFFFFFF

#} OMX_DITHERTYPE;

#** 
#* Structure used to configure current type of dithering 
#*/
class OMX_CONFIG_DITHERTYPE(ctypes.Structure):
    _fields_ = [('nSize', OMX_U32),             #**< Size of the structure in bytes */
                ('nVersion', OMX_VERSIONTYPE),  #**< OMX specification version information */ 
                ('nPortIndex', OMX_U32),        #**< Port that this structure applies to */
                ('eDither', OMX_DITHERTYPE)]    #**< Type of dithering to use */

#} OMX_CONFIG_DITHERTYPE;

class OMX_CONFIG_CAPTUREMODETYPE(ctypes.Structure):
    _fields_ = [('nSize', OMX_U32),
                ('nVersion', OMX_VERSIONTYPE),
                ('nPortIndex', OMX_U32),        #**< Port that this structure applies to */
                ('bContinuous', OMX_BOOL),      #**< If true then ignore frame rate and emit capture 
                                                #*   data as fast as possible (otherwise obey port's frame rate). */
                ('bFrameLimited', OMX_BOOL),    #**< If true then terminate capture after the port emits the 
                                                #*   specified number of frames (otherwise the port does not 
                                                #*   terminate the capture until instructed to do so by the client). 
                                                #*   Even if set, the client may manually terminate the capture prior 
                                                #*   to reaching the limit. */
                ('nFrameLimit', OMX_U32)]       #**< Limit on number of frames emitted during a capture (only
                                                #*   valid if bFrameLimited is set). */

#} OMX_CONFIG_CAPTUREMODETYPE;

OMX_METERINGTYPE = OMX_U32
 
(   OMX_MeteringModeAverage,     #**< Center-weighted average metering. */
    OMX_MeteringModeSpot,  	      #**< Spot (partial) metering. */
    OMX_MeteringModeMatrix       #**< Matrix or evaluative metering. */
    ) = range(3)
 
OMX_MeteringKhronosExtensions = 0x6F000000  #**< Reserved region for introducing Khronos Standard Extensions */ 
OMX_MeteringVendorStartUnused = 0x7F000000  #**< Reserved region for introducing Vendor Extensions */

OMX_MeteringModeBacklit = 0x7F000001

OMX_EVModeMax = 0x7fffffff

#} OMX_METERINGTYPE;
 
class OMX_CONFIG_EXPOSUREVALUETYPE(ctypes.Structure):
    _fields_ = [('nSize', OMX_U32),
                ('nVersion', OMX_VERSIONTYPE),
                ('nPortIndex', OMX_U32),
                ('eMetering', OMX_METERINGTYPE),
                ('xEVCompensation', OMX_S32),       #**< Fixed point value stored as Q16 */
                ('nApertureFNumber', OMX_U32),      #**< e.g. nApertureFNumber = 2 implies "f/2" - Q16 format */
                ('bAutoAperture', OMX_BOOL),		#**< Whether aperture number is defined automatically */
                ('nShutterSpeedMsec', OMX_U32),     #**< Shutterspeed in milliseconds */ 
                ('bAutoShutterSpeed', OMX_BOOL),	#**< Whether shutter speed is defined automatically */ 
                ('nSensitivity', OMX_U32),          #**< e.g. nSensitivity = 100 implies "ISO 100" */
                ('bAutoSensitivity', OMX_BOOL)]	    #**< Whether sensitivity is defined automatically */

#} OMX_CONFIG_EXPOSUREVALUETYPE;

#** 
#* Focus region configuration 
#*
#* STRUCT MEMBERS:
#*  nSize           : Size of the structure in bytes
#*  nVersion        : OMX specification version information
#*  nPortIndex      : Port that this structure applies to
#*  bCenter         : Use center region as focus region of interest
#*  bLeft           : Use left region as focus region of interest
#*  bRight          : Use right region as focus region of interest
#*  bTop            : Use top region as focus region of interest
#*  bBottom         : Use bottom region as focus region of interest
#*  bTopLeft        : Use top left region as focus region of interest
#*  bTopRight       : Use top right region as focus region of interest
#*  bBottomLeft     : Use bottom left region as focus region of interest
#*  bBottomRight    : Use bottom right region as focus region of interest
#*/
class OMX_CONFIG_FOCUSREGIONTYPE(ctypes.Structure):
    _fields_ = [('nSize', OMX_U32),
                ('nVersion', OMX_VERSIONTYPE),
                ('nPortIndex', OMX_U32),
                ('bCenter', OMX_BOOL),
                ('bLeft', OMX_BOOL),
                ('bRight', OMX_BOOL),
                ('bTop', OMX_BOOL),
                ('bBottom', OMX_BOOL),
                ('bTopLeft', OMX_BOOL),
                ('bTopRight', OMX_BOOL),
                ('bBottomLeft', OMX_BOOL),
                ('bBottomRight', OMX_BOOL)]

#} OMX_CONFIG_FOCUSREGIONTYPE;

#** 
#* Focus Status type 
#*/
OMX_FOCUSSTATUSTYPE = OMX_U32

(   OMX_FocusStatusOff,                     # = 0,
    OMX_FocusStatusRequest,
    OMX_FocusStatusReached,
    OMX_FocusStatusUnableToReach,
    OMX_FocusStatusLost 
    ) = range(5)

OMX_FocusStatusKhronosExtensions = 0x6F000000  #**< Reserved region for introducing Khronos Standard Extensions */ 
OMX_FocusStatusVendorStartUnused = 0x7F000000  #**< Reserved region for introducing Vendor Extensions */

(   OMX_FocusStatusCafWatching,
    OMX_FocusStatusCafSceneChanged 
    ) = (0x7F000001 + i for i in range(2))

OMX_FocusStatusMax = 0x7FFFFFFF

#} OMX_FOCUSSTATUSTYPE;

#** 
#* Focus status configuration 
#*
#* STRUCT MEMBERS:
#*  nSize               : Size of the structure in bytes
#*  nVersion            : OMX specification version information
#*  nPortIndex          : Port that this structure applies to
#*  eFocusStatus        : Specifies the focus status
#*  bCenterStatus       : Use center region as focus region of interest
#*  bLeftStatus         : Use left region as focus region of interest
#*  bRightStatus        : Use right region as focus region of interest
#*  bTopStatus          : Use top region as focus region of interest
#*  bBottomStatus       : Use bottom region as focus region of interest
#*  bTopLeftStatus      : Use top left region as focus region of interest
#*  bTopRightStatus     : Use top right region as focus region of interest
#*  bBottomLeftStatus   : Use bottom left region as focus region of interest
#*  bBottomRightStatus  : Use bottom right region as focus region of interest
#*/
class OMX_PARAM_FOCUSSTATUSTYPE(ctypes.Structure):
    _fields_ = [('nSize', OMX_U32),
                ('nVersion', OMX_VERSIONTYPE),
                ('nPortIndex', OMX_U32),
                ('eFocusStatus', OMX_FOCUSSTATUSTYPE),
                ('bCenterStatus', OMX_BOOL),
                ('bLeftStatus', OMX_BOOL),
                ('bRightStatus', OMX_BOOL),
                ('bTopStatus', OMX_BOOL),
                ('bBottomStatus', OMX_BOOL),
                ('bTopLeftStatus', OMX_BOOL),
                ('bTopRightStatus', OMX_BOOL),
                ('bBottomLeftStatus', OMX_BOOL),
                ('bBottomRightStatus', OMX_BOOL)]

#} OMX_PARAM_FOCUSSTATUSTYPE;


#** @} */
#* File EOF */

