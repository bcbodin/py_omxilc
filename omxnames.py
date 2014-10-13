"""
Module Name: omxnames.py
Python Version: 2.7.3

This module defines the names for component domains, commands, states, coding
formats, color formats and other-domain data types.

Copyright (c) 2014 Binh Bui

Redistribution and use in source and binary forms, with or without
modification, are permitted.
"""

from omx_index import *

#-------------------------------------------------------------------------------
# Component Domain Names

omx_component_domain_names = ('Audio', 'Image', 'Video', 'Other')

omx_component_domains = (OMX_IndexParamAudioInit,
                         OMX_IndexParamImageInit,
                         OMX_IndexParamVideoInit,
                         OMX_IndexParamOtherInit)

#-------------------------------------------------------------------------------
# Command Names

omx_cmd_names = (
        'command StateSet',
        'command Flush',
        'command PortDisable',
        'command PortEnable',
        'command MarkBuffer')

#-------------------------------------------------------------------------------
# State Names

omx_state_names = (
        'state Invalid',
        'state Loaded',
        'state Idle',
        'state Executing',
        'state Pause',
        'state WaitForResources')

#-------------------------------------------------------------------------------
# Audio Coding Format Names

omx_audio_coding_names = {
    0x00000000: 'Unused',
    0x00000001: 'AutoDetect',
    0x00000002: 'PCM',
    0x00000003: 'ADPCM',
    0x00000004: 'AMR',
    0x00000005: 'GSMFR',
    0x00000006: 'GSMEFR',
    0x00000007: 'GSMHR',
    0x00000008: 'PDCFR',
    0x00000009: 'PDCEFR',
    0x0000000a: 'PDCHR',
    0x0000000b: 'TDMAFR',
    0x0000000c: 'TDMAEFR',
    0x0000000d: 'QCELP8',
    0x0000000e: 'QCELP13',
    0x0000000f: 'EVRC',
    0x00000010: 'SMV',
    0x00000011: 'G711',
    0x00000012: 'G723',
    0x00000013: 'G726',
    0x00000014: 'G729',
    0x00000015: 'AAC',
    0x00000016: 'MP3',
    0x00000017: 'SBC',
    0x00000018: 'VORBIS',
    0x00000019: 'WMA',
    0x0000001a: 'RA',
    0x0000001b: 'MIDI',
    0x7f000001: 'FLAC',
    0x7f000002: 'DDP',
    0x7f000003: 'DTS',
    0x7f000004: 'WMAPRO',
    0x7f000005: 'ATRAC3',
    0x7f000006: 'ATRACX',
    0x7f000007: 'ATRACAAL'
}

#-------------------------------------------------------------------------------
# Image Coding Format Names

omx_image_coding_names = {
    0x00000000: 'Unused',
    0x00000001: 'AutoDetect',
    0x00000002: 'JPEG',
    0x00000003: 'JPEG2K',
    0x00000004: 'EXIF',
    0x00000005: 'TIFF',
    0x00000006: 'GIF',
    0x00000007: 'PNG',
    0x00000008: 'LZW',
    0x00000009: 'BMP',
    0x7f000001: 'CodingTGA',
    0x7f000002: 'PPM'
}

#-------------------------------------------------------------------------------
# Video Coding Format Names

omx_video_coding_names = {
    0x00000000: 'Unused',
    0x00000001: 'AutoDetect',
    0x00000002: 'MPEG2',
    0x00000003: 'H263',
    0x00000004: 'MPEG4',
    0x00000005: 'WMV',
    0x00000006: 'RV',
    0x00000007: 'AVC',
    0x00000008: 'MJPEG',
    0x7f000001: 'VP6',
    0x7f000002: 'VP7',
    0x7f000003: 'VP8',
    0x7f000004: 'YUV',
    0x7f000005: 'Sorenson',
    0x7f000006: 'Theora',
    0x7f000007: 'MVC'
}

#-------------------------------------------------------------------------------
# Color Format Names

omx_color_format_names = {
    0x00000000: 'Unused',
    0x00000001: 'Monochrome',
    0x00000002: '8bitRGB332',
    0x00000003: '12bitRGB444',
    0x00000004: '16bitARGB4444',
    0x00000005: '16bitARGB1555',
    0x00000006: '16bitRGB565',
    0x00000007: '16bitBGR565',
    0x00000008: '18bitRGB666',
    0x00000009: '18bitARGB1665',
    0x0000000a: '19bitARGB1666', 
    0x0000000b: '24bitRGB888',
    0x0000000c: '24bitBGR888',
    0x0000000d: '24bitARGB1887',
    0x0000000e: '25bitARGB1888',
    0x0000000f: '32bitBGRA8888',
    0x00000010: '32bitARGB8888',
    0x00000011: 'YUV411Planar',
    0x00000012: 'YUV411PackedPlanar',
    0x00000013: 'YUV420Planar',
    0x00000014: 'YUV420PackedPlanar',
    0x00000015: 'YUV420SemiPlanar',
    0x00000016: 'YUV422Planar',
    0x00000017: 'YUV422PackedPlanar',
    0x00000018: 'YUV422SemiPlanar',
    0x00000019: 'YCbYCr',
    0x0000001a: 'YCrYCb',
    0x0000001b: 'CbYCrY',
    0x0000001c: 'CrYCbY',
    0x0000001d: 'YUV444Interleaved',
    0x0000001e: 'RawBayer8bit',
    0x0000001f: 'RawBayer10bit',
    0x00000020: 'RawBayer8bitcompressed',
    0x00000021: 'L2', 
    0x00000022: 'L4', 
    0x00000023: 'L8', 
    0x00000024: 'L16', 
    0x00000025: 'L24', 
    0x00000026: 'L32',
    0x00000027: 'YUV420PackedSemiPlanar',
    0x00000028: 'YUV422PackedSemiPlanar',
    0x00000029: '18BitBGR666',
    0x0000002a: '24BitARGB6666',
    0x0000002b: '24BitABGR6666',
    0x7f000001: '32bitABGR8888',
    0x7f000002: '8bitPalette',
    0x7f000003: 'YUVUV128',
    0x7f000004: 'RawBayer12bit',
    0x7f000005: 'BRCMEGL',
    0x7f000006: 'BRCMOpaque',
    0x7f000007: 'YVU420PackedPlanar',
    0x7f000008: 'YVU420PackedSemiPlanar'
}

#-------------------------------------------------------------------------------
# Other-Domain Data Type Names

omx_other_data_type_names = {
    0x00000000: 'Time',
    0x00000001: 'Power',
    0x00000002: 'Stats',
    0x00000003: 'Binary',
    0x7f000001: 'Text',
    0x7f000002: 'TextSKM2',
    0x7f000003: 'Text3GP5'
}


