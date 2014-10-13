py_omxilc
=========

This package defines a component class for writing OpenMAX IL client applications in Python 2.7.3
for the Raspberry Pi B/B+ board. It is mainly based on the file ilclient.c developed by Broadcom
which defines an IL client side library. It is also based on the python module pyopenmax.py
developed by Peter de Rivaz.

The component class omxComponent is defined in the main module omxilc.py. ctypes is used to call
the core and component methods provided by the Broadcom C library libopenmaxil.so.

There are several other modules in the package. The majority of them are simply python converion of
the OpenMAX IL standard C header files. omxerr.py and omxnames.py are supporting modules for omxilc.py.
The converted headers are: omx_audio.py, omx_component.py, omx_core.py, omx_image.py, omx_index.py,
omx_ivcommon.py, omx_other.py, omx_types.py, and omx_video.py. The module omxbcport.py defines all
known port indices of the OpenMAX components in Broadcom VMCS-X release. The last module is included
for reference and is not required for writing applications.

The module omxjpgdec.py is an application module. This module pairs an image_decode with a resize
component to decode a JPEG image from a file to a specified color format and resize it to a specified
dimension for display. Supported color formats are: 16bitRGB565, YUV420PackedPlanar and 32bitABGR8888.

There are two methods in the JPEG decoder module for setting up the components and converting a file.
The first method sets up a complete pipe before the components go into state Executing. The alternate
set up method is developed by Matt Ownby and Anthong Sale and used in their hello_jpeg demo program
for the Raspberry Pi board. The conversion method ConvertFromFile must be used with Setup. Likewise,
the conversion metho AltConvertFromFile must be used with AltSetup.

There is a local variable _verbose in omxilc.py which enables the console printouts of statuses when
it is set to True.

The JPEG decoder was run from the console with verbose on and 2000 continuous conversions of a single
1920x1080 JPEG file. The 32-bit ABGR output size is 1104x621. The total run time was 5m23s which amounts
to 162 ms/frame or 6.2 frames/sec.

With the verbose off, the JPEG decoder causes the system to hang after some number of iterations.
I think that there are some sort of synchronisation/timing issues.

Copyright (c) 2014 Binh Bui

Redistribution and use in source and binary forms, with or without
modification, are permitted.

