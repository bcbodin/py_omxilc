"""
Module Name: omxerr.py
Python Version: 2.7.6

Standard OMX Error Class

Copyright (c) 2014 Binh Bui

Redistribution and use in source and binary forms, with or without
modification, are permitted.
"""
#===============================================================================
#  Copyright (c) 2008 The Khronos Group Inc. 
#  
#  Permission is hereby granted, free of charge, to any person obtaining
#  a copy of this software and associated documentation files (the
#  "Software"), to deal in the Software without restriction, including
#  without limitation the rights to use, copy, modify, merge, publish,
#  distribute, sublicense, and/or sell copies of the Software, and to
#  permit persons to whom the Software is furnished to do so, subject
#  to the following conditions: 
#  The above copyright notice and this permission notice shall be included
#  in all copies or substantial portions of the Software. 
#  
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
#  OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
#  CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
#  TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#  SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE. 
#  
#===============================================================================

class OMXError(object):
    """
    Standard OMX Error Class
    """

    def __init__(self):
        """
        Initialize a dictionary of standard OMX errors indexed by codes.
        For the definition of these errors, see the OMX_ERRORTYPE enumeration
        in OMX_Core.h (or omx_core.py).
        """

        self.dict = {
            0x00000000: 'OMX_ErrorNone',

            0x80001000: 'OMX_ErrorInsufficientResources',
            0x80001001: 'OMX_ErrorUndefined',
            0x80001002: 'OMX_ErrorInvalidComponentName',
            0x80001003: 'OMX_ErrorComponentNotFound',
            0x80001004: 'OMX_ErrorInvalidComponent',
            0x80001005: 'OMX_ErrorBadParameter',
            0x80001006: 'OMX_ErrorNotImplemented',
            0x80001007: 'OMX_ErrorUnderflow',
            0x80001008: 'OMX_ErrorOverflow',
            0x80001009: 'OMX_ErrorHardware',
            0x8000100A: 'OMX_ErrorInvalidState',
            0x8000100B: 'OMX_ErrorStreamCorrupt',
            0x8000100C: 'OMX_ErrorPortsNotCompatible',
            0x8000100D: 'OMX_ErrorResourcesLost',
            0x8000100E: 'OMX_ErrorNoMore',
            0x8000100F: 'OMX_ErrorVersionMismatch',
            0x80001010: 'OMX_ErrorNotReady',
            0x80001011: 'OMX_ErrorTimeout',
            0x80001012: 'OMX_ErrorSameState',
            0x80001013: 'OMX_ErrorResourcesPreempted',
            0x80001014: 'OMX_ErrorPortUnresponsiveDuringAllocation',
            0x80001015: 'OMX_ErrorPortUnresponsiveDuringDeallocation',
            0x80001016: 'OMX_ErrorPortUnresponsiveDuringStop',
            0x80001017: 'OMX_ErrorIncorrectStateTransition',
            0x80001018: 'OMX_ErrorIncorrectStateOperation',
            0x80001019: 'OMX_ErrorUnsupportedSetting',
            0x8000101A: 'OMX_ErrorUnsupportedIndex',
            0x8000101B: 'OMX_ErrorBadPortIndex',
            0x8000101C: 'OMX_ErrorPortUnpopulated',
            0x8000101D: 'OMX_ErrorComponentSuspended',
            0x8000101E: 'OMX_ErrorDynamicResourcesUnavailable',
            0x8000101F: 'OMX_ErrorMbErrorsInFrame',
            0x80001020: 'OMX_ErrorFormatNotDetected',
            0x80001021: 'OMX_ErrorContentPipeOpenFailed',
            0x80001022: 'OMX_ErrorContentPipeCreationFailed',
            0x80001023: 'OMX_ErrorSeperateTablesUsed',
            0x80001024: 'OMX_ErrorTunnelingUnsupported',

            0x8F000000: 'OMX_ErrorKhronosExtensions',

            0x90000000: 'OMX_ErrorVendorStartUnused',
            0x90000001: 'OMX_ErrorDiskFull',
            0x90000002: 'OMX_ErrorMaxFileSize',
            0x90000003: 'OMX_ErrorDrmUnauthorised',
            0x90000004: 'OMX_ErrorDrmExpired',
            0x90000005: 'OMX_ErrorDrmGeneral'
        }

    #---------------------------------------------------------------------------

    def Print(self, error, comp_name='', method=''):
        """
        Method to print the name of an error detected by a component, or
        resulted from the unsuccessful execution of a method or function.

        Parameters:
            error       <int>       error code from OMX_ERRORTYPE enumeration
            comp_name   <str>       name of component (optional)
            method      <str>       name of method or function (optional)

        Return values:
            None
        """

        if error:
            e = error & 0xffffffff

            s = ''
            if comp_name:
                s += comp_name + '.'
            if method:
                s += method + ' failed:'
            l = len(s)
            if l > 0:
                s = s[:-1] + ':'
            else:
                s = '%s:' % hex(e)


            if e in self.dict:
                error_name = self.dict[e]
            else:
                error_name = 'Undefined Error Code'
                if l > 0:
                    error_name += ' (%s)' % hex(e)

            print s, error_name


