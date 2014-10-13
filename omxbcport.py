"""
Module Name: omxbcport.py
Python Version: 2.7.3

This module defines all known port indices of the OpenMAX components in
Broadcom VMCS-X release.
Reference: Raspberry Pi firmware/documentation/ilcomponents/index.html.

Copyright (c) 2014 Binh Bui

Redistribution and use in source and binary forms, with or without
modification, are permitted.
"""

#-------------------------------------------------------------------------------
# Audio Domain Components
#-------------------------------------------------------------------------------

PORT_AUDIO_CAPTURE_INPUT_CLOCK = 181
PORT_AUDIO_CAPTURE_OUTPUT      = 180

PORT_AUDIO_DECODE_INPUT  = 120
PORT_AUDIO_DECODE_OUTPUT = 121

PORT_AUDIO_ENCODE_INPUT  = 160
PORT_AUDIO_ENCODE_OUTPUT = 161

PORT_AUDIO_LOWPOWER_INPUT = 270

PORT_AUDIO_MIXER_INPUT_1     = 232
PORT_AUDIO_MIXER_INPUT_2     = 233
PORT_AUDIO_MIXER_INPUT_3     = 234
PORT_AUDIO_MIXER_INPUT_4     = 235
PORT_AUDIO_MIXER_INPUT_CLOCK = 230
PORT_AUDIO_MIXER_OUTPUT      = 231

PORT_AUDIO_PROCESSOR_INPUT  = 300
PORT_AUDIO_PROCESSOR_OUTPUT = 301

PORT_AUDIO_RENDER_INPUT       = 100
PORT_AUDIO_RENDER_INPUT_CLOCK = 101

PORT_AUDIO_SPLITTER_INPUT       = 261
PORT_AUDIO_SPLITTER_INPUT_CLOCK = 260
PORT_AUDIO_SPLITTER_OUTPUT_1    = 262
PORT_AUDIO_SPLITTER_OUTPUT_2    = 263
PORT_AUDIO_SPLITTER_OUTPUT_3    = 264
PORT_AUDIO_SPLITTER_OUTPUT_4    = 265

#-------------------------------------------------------------------------------
# Image Domain Components
#-------------------------------------------------------------------------------

PORT_IMAGE_DECODE_INPUT  = 320
PORT_IMAGE_DECODE_OUTPUT = 321

PORT_IMAGE_ENCODE_INPUT  = 340
PORT_IMAGE_ENCODE_OUTPUT = 341

PORT_IMAGE_FX_INPUT  = 190
PORT_IMAGE_FX_OUTPUT = 191

PORT_IMAGE_READ_OUTPUT = 310
PORT_IMAGE_WRITE_INPUT = 330

PORT_RESIZE_INPUT  = 60
PORT_RESIZE_OUTPUT = 61

PORT_SOURCE_OUTPUT = 20

PORT_TRANSITION_INPUT_1 = 210
PORT_TRANSITION_INPUT_2 = 211
PORT_TRANSITION_OUTPUT  = 212

PORT_WRITE_STILL_INPUT = 30

#-------------------------------------------------------------------------------
# Miscellaneous Components
#-------------------------------------------------------------------------------

PORT_CLOCK_OUTPUT_1 = 80
PORT_CLOCK_OUTPUT_2 = 81
PORT_CLOCK_OUTPUT_3 = 82
PORT_CLOCK_OUTPUT_4 = 83
PORT_CLOCK_OUTPUT_5 = 84
PORT_CLOCK_OUTPUT_6 = 85

PORT_NULL_SINK_INPUT_AUDIO = 242
PORT_NULL_SINK_INPUT_IMAGE = 241
PORT_NULL_SINK_INPUT_VIDEO = 240

PORT_TEXT_SCHEDULER_INPUT       = 150
PORT_TEXT_SCHEDULER_INPUT_CLOCK = 152
PORT_TEXT_SCHEDULER_OUTPUT      = 151

PORT_VISUALISATION_INPUT_AUDIO  = 140
PORT_VISUALISATION_INPUT_CLOCK  = 143
PORT_VISUALISATION_OUTPUT_AUDIO = 141 
PORT_VISUALISATION_OUTPUT_VIDEO = 142

#-------------------------------------------------------------------------------
# Mux/Demux Components
#-------------------------------------------------------------------------------

PORT_READ_MEDIA_INPUT_CLOCK  = 113
PORT_READ_MEDIA_OUTPUT_AUDIO = 110
PORT_READ_MEDIA_OUTPUT_TEXT  = 112
PORT_READ_MEDIA_OUTPUT_VIDEO = 111

PORT_WRITE_MEDIA_INPUT_AUDIO = 170
PORT_WRITE_MEDIA_INPUT_VIDEO = 171

#-------------------------------------------------------------------------------
# Video Domain Components
#-------------------------------------------------------------------------------

PORT_CAMERA_INPUT_CLOCK    = 73
PORT_CAMERA_OUTPUT_VIDEO_1 = 70
PORT_CAMERA_OUTPUT_VIDEO_2 = 71
PORT_CAMERA_OUTPUT_IMAGE   = 72

PORT_EGL_RENDER_INPUT  = 220
PORT_EGL_RENDER_OUTPUT = 221

PORT_VIDEO_DECODE_INPUT  = 130
PORT_VIDEO_DECODE_OUTPUT = 131

PORT_VIDEO_ENCODE_INPUT  = 200
PORT_VIDEO_ENCODE_OUTPUT = 201

PORT_VIDEO_RENDER_INPUT = 90

PORT_VIDEO_SCHEDULER_INPUT       = 10
PORT_VIDEO_SCHEDULER_INPUT_CLOCK = 12
PORT_VIDEO_SCHEDULER_OUTPUT      = 11

PORT_VIDEO_SPLITTER_INPUT       = 250
PORT_VIDEO_SPLITTER_OUTPUT_1    = 251
PORT_VIDEO_SPLITTER_OUTPUT_2    = 252
PORT_VIDEO_SPLITTER_OUTPUT_3    = 253
PORT_VIDEO_SPLITTER_OUTPUT_4    = 254

