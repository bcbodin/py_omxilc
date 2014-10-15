"""
Module Name: omxjpgdec.py
Version: 1.1 (2014-10-14)
Python Version: 2.7.3
Platform: Raspberry Pi

An OpenMAX JPEG Decoder

This module pairs an image_decode with a resize component to decode a JPEG image
to a specified color format and resize it to a specified dimension for display.
Supported color formats are: 16bitRGB565, YUV420PackedPlanar and 32bitABGR8888.

Copyright (c) 2014 Binh Bui

Redistribution and use in source and binary forms, with or without
modification, are permitted.
"""

from omxilc import *
import os

ILC_TIMEOUT = 250   # default time-out in ms

#===============================================================================
# OpenMAX JPEG Decoder Class
#===============================================================================

class JPEGDecoder(object):
    """OpenMAX JPEG Decoder Class"""

    def __init__(self, out_width=1920, out_height=1080,
                 out_format=OMX_COLOR_Format32bitABGR8888,
                 in_width=1920, in_height=1080,
                 timeout=ILC_TIMEOUT, name='jpeg_decoder'):
        """
        Jpeg Decoder Class Constructor

        Parameters:
            out_width       <int>   Desired output image width (optional).
            out_height      <int>   Desired output image height (optional).
            out_format      <int>   Desired output color format (optional).
            in_width        <int>   Expected input image width (optional).
            in_height       <int>   Expected input image height (optional).
            timeout         <int>   Time-out in ms (optional).
            name            <str>   Name of JPEG decoder (optional).
        """

        # Save initialization parameters.
        self.out_width = out_width
        self.out_height = out_height
        self.out_format = out_format
        self.in_width = in_width
        self.in_height = in_height
        self.timeout = timeout
        self.name = name

        # Sizes of decoder input and resizer output buffers:
        w = ((in_width + 15)/16)*16     # Round up to multiples of 16.
        h = ((in_height + 15)/16)*16
        self.in_buf_size = (w*h)/30

        w = ((out_width + 15)/16)*16    # Round up to multiples of 16.
        h = ((out_height + 15)/16)*16
        sz = w*h
        if out_format == OMX_COLOR_FormatYUV420PackedPlanar:
            self.out_buf_size = sz
        elif out_format == OMX_COLOR_Format16bitRGB565:
            self.out_buf_size = sz*2
        elif out_format == OMX_COLOR_Format32bitABGR8888:
            self.out_buf_size = sz*4
        else:
            cons_print('%s__init__: Unsupported output color format.' %
                self.name)
            return

        self.ready = False

        # Create image_decode component.
        self.decoder = omxComponent(name='image_decode',
                flags=ILCLIENT_FLAGS_ALL,
                timeout=timeout)

        # Create resize component.
        self.resizer = omxComponent(name='resize',
                flags=ILCLIENT_FLAGS_ALL,
                timeout=timeout)

        # Ensure that both components are created.
        if not self.decoder.c_handle or not self.resizer.c_handle:
            cons_print('%s.__init__: Required component(s) not created.' %
                self.name)
            return

        # Get input and output port indices of components.
        num_ports = 0
        if 'Image1' in self.decoder.in_port_indices:
            self.decoder_in_port = self.decoder.in_port_indices['Image1']
            num_ports += 1
        if 'Image1' in self.decoder.out_port_indices:
            self.decoder_out_port = self.decoder.out_port_indices['Image1']
            num_ports += 1
        if 'Image1' in self.resizer.in_port_indices:
            self.resizer_in_port = self.resizer.in_port_indices['Image1']
            num_ports += 1
        if 'Image1' in self.resizer.out_port_indices:
            self.resizer_out_port = self.resizer.out_port_indices['Image1']
            num_ports += 1

        # Ensure that there are 4 ports.
        if num_ports != 4:
            cons_print('%s.__init__: Less than 4 ports found.' % self.name)
            return

        # Set up JPEG decoder.
        self.Setup()

    #---------------------------------------------------------------------------
    def Close(self):
        """
        Close the JPEG decoder.

        Return value:
            <int>       Error code: 0 for success, not 0 for failure.
        """

        # Get buffer supplier for decoder output port.
        e, bs = self.decoder.GetBufferSupplier(self.decoder_out_port)
        if e != OMX_ErrorNone:
            return e

        # Disable resizer input and decoder output.
        # Supplier port is disabled first and non-supplier port second.
        if bs == OMX_BufferSupplyInput: # Supplier is resizer input port.
            e |= self.resizer.DisablePort(self.resizer_in_port)
            e |= self.decoder.DisablePort(self.decoder_out_port, self.timeout)
            self.resizer.WaitForPortDisabled(self.resizer_in_port, self.timeout)
        else:
            e |= self.decoder.DisablePort(self.decoder_out_port)
            e |= self.resizer.DisablePort(self.resizer_in_port, self.timeout)
            self.decoder.WaitForPortDisabled(self.decoder_out_port, self.timeout)

        # Remove tunnel between decoder output and resizer input.
        e |= self.decoder.RemoveOutTunnel()

        # Disable resizer output port.
        e |= self.resizer.DisablePort(self.resizer_out_port)

        # Resizer should generate a FillBufferDone callback
        # for each output port buffer.

        # Free resizer output port buffers.
        for n in range(self.num_out_buf):
            cp_out_buf_hdr = self.resizer.c_app_data.pp_out_buf_hdr[n]
            e |= self.resizer.FreeBuffer(self.resizer_out_port, cp_out_buf_hdr)

        # Wait until resizer output port is disabled.
        self.resizer.WaitForPortDisabled(self.resizer_out_port, self.timeout)

        # Disable decoder input port.
        e |= self.decoder.DisablePort(self.decoder_in_port)

        # Free decoder input port buffers.
        for n in range(self.num_in_buf):
            cp_in_buf_hdr = self.decoder.c_app_data.pp_in_buf_hdr[n]
            e |= self.decoder.FreeBuffer(self.decoder_in_port, cp_in_buf_hdr)

        # Wait until decoder port is disabled.
        self.decoder.WaitForPortDisabled(self.decoder_in_port, self.timeout)

        # Request resizer and decoder to change state to Idle.
        e = self.resizer.ChangeState(OMX_StateIdle)
        e |= self.decoder.ChangeState(OMX_StateIdle)

        # Wait until resizer and decoder are in state Idle.
        self.resizer.WaitForState(OMX_StateIdle)
        self.decoder.WaitForState(OMX_StateIdle)

        # Request resizer and decoder to change state to Loaded.
        e |= self.resizer.ChangeState(OMX_StateLoaded)
        e |= self.decoder.ChangeState(OMX_StateLoaded)

        # Wait until resizer and decoder are in state Loaded.
        self.resizer.WaitForState(OMX_StateLoaded)
        self.decoder.WaitForState(OMX_StateLoaded)

        e |= self.decoder.Close()
        e |= self.resizer.Close()

        return e

    #---------------------------------------------------------------------------
    def Setup(self):
        """
        Set up the JPEG decoder.

        Return value:
            <int>       Error code: 0 for success, not 0 for failure.
        """

#        cons_print('%s.Setup' % self.name)
        self.alt_setup = False

        # Ensure that both components are in state Loaded.
        if self.decoder.c_app_data.current_state != OMX_StateLoaded:
            cons_print('%s.Setup: Decoder not in state Loaded.' % self.name)
            return
        if self.resizer.c_app_data.current_state != OMX_StateLoaded:
            cons_print('%s.Setup: Resizer not in state Loaded.' % self.name)
            return

        # Set format of decoder input port.
        e = self.decoder.SetImagePortFormat(
                self.decoder_in_port,
                OMX_IMAGE_CodingJPEG,
                OMX_COLOR_FormatUnused)

        # Modify settings of resizer output port.
        e |= self.resizerSetOutputDefinition(
                coding=OMX_IMAGE_CodingUnused,
                color=self.out_format,
                width=self.out_width,
                height=self.out_height)

        # Set up tunnel between decoder output and resizer input.
        e |= self.decoder.PlaceOutTunnel(self.decoder_out_port,
                self.resizer, self.resizer_in_port)

        # Enable all ports.
        e |= self.decoder.EnablePort(self.decoder_in_port, self.timeout)
        e |= self.decoder.EnablePort(self.decoder_out_port, self.timeout)
        e |= self.resizer.EnablePort(self.resizer_in_port, self.timeout)
        e |= self.resizer.EnablePort(self.resizer_out_port, self.timeout)

        # Request resizer and decoder to change state to Idle.
        e |= self.resizer.ChangeState(OMX_StateIdle)
        e |= self.decoder.ChangeState(OMX_StateIdle)

        # Resizer output port should generate a settings change event.
        self.resizer.WaitForPortSettingsChanged(self.resizer_out_port)

        # Allocate buffers to resizer output port.
        ec, self.cpp_out_buf = self.resizer.AllocateAllBuffers(
                self.resizer_out_port,
                self.out_buf_size)
        e |= ec
        self.num_out_buf = len(self.cpp_out_buf)
#        self.out_buf_free = [1] * self.num_out_buf
        if ec == OMX_ErrorNone:
            sz = len(self.cpp_out_buf[0][0])
            if sz != self.out_buf_size:
                self.out_buf_size = sz

        # Allocate buffers to decoder input port.
        ec, self.cpp_in_buf = self.decoder.AllocateAllBuffers(
                self.decoder_in_port,
                self.in_buf_size)
        e |= ec
        self.num_in_buf = len(self.cpp_in_buf)
#        self.in_buf_free = [1] * self.num_in_buf
        if ec == OMX_ErrorNone:
            sz = len(self.cpp_in_buf[0][0])
            if sz != self.in_buf_size:
                self.in_buf_size = sz

        # Wait until resizer and decoder are in state Idle.
        self.resizer.WaitForState(OMX_StateIdle)
        self.decoder.WaitForState(OMX_StateIdle)

        # Request resizer and decoder to change state to Executing.
        e |= self.resizer.ChangeState(OMX_StateExecuting)
        e |= self.decoder.ChangeState(OMX_StateExecuting)

        # Wait until resizer decoder are in state Executing.
        self.resizer.WaitForState(OMX_StateExecuting)
        self.decoder.WaitForState(OMX_StateExecuting)

        # Set ready flag.
        if e == OMX_ErrorNone:
            self.ready = True
            cons_print('%s: Ready.' % self.name)

        return e

    #---------------------------------------------------------------------------
    def AltSetup(self):
        """
        Alternate Set Up for the JPEG Decoder

        This set up sequence is used by Matt Ownby and Anthong Sale in the
        hello_jpeg demo program.

        Return value:
            <int>       Error code: 0 for success, not 0 for failure.
        """

        cons_print('%s.AltSetup' % self.name)
        self.alt_setup = True

        # Ensure that both components are in state Loaded.
        if self.decoder.c_app_data.current_state != OMX_StateLoaded:
            cons_print('%s.Setup: Decoder not in state Loaded.' % self.name)
            return
        if self.resizer.c_app_data.current_state != OMX_StateLoaded:
            cons_print('%s.Setup: Resizer not in state Loaded.' % self.name)
            return

        # Set format of decoder input port.
        e = self.decoder.SetImagePortFormat(
                self.decoder_in_port,
                OMX_IMAGE_CodingJPEG,
                OMX_COLOR_FormatUnused)

        # Enable decoder input port.
        e |= self.decoder.EnablePort(self.decoder_in_port, self.timeout)

        # Request decoder to change state to Idle.
        e |= self.decoder.ChangeState(OMX_StateIdle)

        # Allocate buffers to decoder input port.
        ec, self.cpp_in_buf = self.decoder.AllocateAllBuffers(
                self.decoder_in_port,
                self.in_buf_size)
        e |= ec
        self.num_in_buf = len(self.cpp_in_buf)
#        self.in_buf_free = [1] * self.num_in_buf
        if ec == OMX_ErrorNone:
            sz = len(self.cpp_in_buf[0][0])
            if sz != self.in_buf_size:
                self.in_buf_size = sz

        # Wait until decoder is in state Idle.
        self.decoder.WaitForState(OMX_StateIdle)

        # Request decoder to change state to Executing.
        e |= self.decoder.ChangeState(OMX_StateExecuting)

        # Wait until decoder is in state Executing.
        self.decoder.WaitForState(OMX_StateExecuting)

        # Set ready flag.
        if e == OMX_ErrorNone:
            self.ready = True
            cons_print('%s: Ready.' % self.name)

        self.num_out_buf = 0

        return e

    #---------------------------------------------------------------------------
    def SetupPipe(self):
        """
        Once the settings of the decoder output port change after the first
        input buffer load is converted, set the color format of the decoder
        output port, configure the resizer, place a tunnel from the decoder
        output port to the resizer input port, and allocate and supply buffer(s)
        to the resizer output port.

        This first-time handler is adapted from the hello_jpeg demo program by
        Matt Ownby and Anthong Sale.

        Return value:
            <int>       Error code: 0 for success, not 0 for failure.
        """

        cons_print('%s.SetupPipe' % self.name)

        # Set color format of decoder output port.
        # This will crash the system.
#        e = self.decoder.SetImagePortFormat(
#                self.decoder_out_port,
#                OMX_IMAGE_CodingUnused,
#                self.out_format)

        # Copy decoder output port settings to resizer input port.
        e = self.CopyPortDefinition(
                self.decoder,
                self.decoder_out_port,
                self.resizer,
                self.resizer_in_port)

        # Set up tunnel between decoder output and resizer input.
        e |= self.decoder.PlaceOutTunnel(self.decoder_out_port,
                self.resizer, self.resizer_in_port)

        # Enable decoder output and resizer input.
        e |= self.decoder.EnablePort(self.decoder_out_port)
        e |= self.resizer.EnablePort(self.resizer_in_port, self.timeout)

        # Request resizer to change state to Idle.
        e |= self.resizer.ChangeState(OMX_StateIdle)

        # Resizer output port should generate a settings change event.
        self.resizer.WaitForPortSettingsChanged(self.resizer_out_port)

        # Decoder output port should be enabled.
        self.decoder.WaitForPortEnabled(self.decoder_out_port, self.timeout)

        # Wait until resizer is in state Idle.
        self.resizer.WaitForState(OMX_StateIdle)

        # Modify settings of resizer output port.
        e |= self.resizerSetOutputDefinition(
                coding=OMX_IMAGE_CodingUnused,
                color=self.out_format,
                width=self.out_width,
                height=self.out_height)

        # Request resizer to change state to Executing.
        e |= self.resizer.ChangeState(OMX_StateExecuting)

        # Wait until resizer is in state Executing.
        self.resizer.WaitForState(OMX_StateExecuting)

        # Enable resizer output port.
        e |= self.resizer.EnablePort(self.resizer_out_port)

        # Allocate buffers to resizer output port.
        ec, self.cpp_out_buf = self.resizer.AllocateAllBuffers(
                self.resizer_out_port,
                self.out_buf_size)
        e |= ec
        self.num_out_buf = len(self.cpp_out_buf)
#        self.out_buf_free = [1] * self.num_out_buf
        if ec == OMX_ErrorNone:
            sz = len(self.cpp_out_buf[0][0])
            if sz != self.out_buf_size:
                self.out_buf_size = sz

        # Wait until the resizer output port is enabled.
        self.resizer.WaitForPortEnabled(self.resizer_out_port, self.timeout)

        return e

    #---------------------------------------------------------------------------
    def CopyPortDefinition(self, src_comp, src_port, dst_comp, dst_port):
        """
        Copy settings of a port of a component to a port of another component.

        Parameters:
            src_comp        <object>    Source component.
            src_port        <int>       Source port index.
            dst_comp        <object>    Destination component.
            dst_port        <int>       Destination port index.

        Return value:
            <int>       Error code.
        """

        e, c_port_def = src_comp.GetPortDefinition(src_port)
        if e != OMX_ErrorNone:
            return e

        e = dst_comp.SetPortDefinition(dst_port, ctypes.pointer(c_port_def))

        return e

    #---------------------------------------------------------------------------
    def resizerSetOutputDefinition(self, coding=-1, color=-1, width=-1, height=-1,
                                   num_buffers=0):
        """
        Modify the settings of the output port of the image resizer.

        Parameters:
            See SetImagePortDefinition.

        Return value:
            See SetImagePortDefinition.
        """

        return self.SetImagePortDefinition(1, 1, coding, color, width, height,
                                           num_buffers)

    #---------------------------------------------------------------------------
    def SetImagePortDefinition(self, component_index, port_dir,
                      coding=-1, color=-1, width=-1, height=-1,
                      num_buffers=0):
        """
        Modify the settings of an image port of a component.

        Parameters:
            component_index <int>       Component index:
                                            0: decoder.
                                            1: resizer.
            port_dir        <int>       Port direction:
                                            0: input.
                                            1: output.
            coding          <int>       Coding format (optional):
                                            -1: no change.
            color           <int>       Color format (optional):
                                            -1: no change.
            width           <int>       Frame width (optional):
                                            -1: no change.
            height          <int>       Frame height (optional):
                                            -1: no change.
            num_buffers     <int>       Number of buffers (optional):
                                            < min.: no change.

        Return value:
            <int>       Error code: 0 for success, not 0 for failure.
        """

        name = self.name + '.SetImagePortDefinition:'
        
        if component_index == 0:
            comp = self.decoder
            if port_dir == 0:
                port_index = self.decoder_in_port
            else:
                port_index = self.decoder_out_port
        elif component_index == 1:
            comp = self.resizer
            if port_dir == 0:
                port_index = self.resizer_in_port
            else:
                port_index = self.resizer_out_port
        else:
            cons_print(name, 'Undefined component.')
            return 1

        e, c_port_def = comp.GetPortDefinition(port_index)
        if e != OMX_ErrorNone:
            return e

        if c_port_def.eDomain != 2:
            cons_print(name, 'Port %d is not an image port.' % port_index)
            return 1

        n = 0
        m = 0
        if coding >= 0:
            if coding not in omx_image_coding_names:
                cons_print(name, 'Unsupported image coding.')
                return 1
            c_port_def.format.image.eCompressionFormat = coding
            n += 1
            m += 1
        else:
            coding = c_port_def.format.image.eCompressionFormat
        if color >= 0:
            if color not in omx_color_format_names:
                cons_print(name, 'Unsupported color format.')
                return 1
            c_port_def.format.image.eColorFormat = color
            n += 1
            m += 1
        else:
            color = c_port_def.format.image.eColorFormat
        if width >= 0:
            c_port_def.format.image.nFrameWidth = width
            n += 1
        else:
            width = c_port_def.format.image.nFrameWidth
        if height >= 0:
            c_port_def.format.image.nFrameHeight = height
            n += 1
        else:
            height = c_port_def.format.image.nFrameHeight
        if num_buffers > c_port_def.nBufferCountMin:
            c_port_def.nBufferCountActual = num_buffers

        if n <= 0:
            return 0

        if n > m:
            c_port_def.format.image.nSliceHeight = ((height + 15)/16)*16
            w = ((width + 15)/16)*16
            if color == OMX_COLOR_FormatYUV420PackedPlanar:
                c_port_def.format.image.nStride = w
            elif color == OMX_COLOR_Format16bitRGB565:
                c_port_def.format.image.nStride = w*2
            elif color == OMX_COLOR_Format32bitABGR8888:
                c_port_def.format.image.nStride = w*4
            else:
                cons_print(name, 'Unsupported color format.')
                return 1
            e = comp.SetPortDefinition(port_index, ctypes.pointer(c_port_def))
        else:
            e = comp.SetImagePortFormat(port_index, coding, color)

        return e

    #---------------------------------------------------------------------------
    def decoderHandleOutSettingsChanged(self):
        """
        When an event occurs due to changes in settings of the decoder output
        port, set the color format of the port again, and copy the settings to
        the resizer input port (sink port of the tunnel).

        Return value:
            <int>       Error code: 0 for success, not 0 for failure.
        """

        # Check port index with settings changed returned by event handler.
        if self.decoder.c_app_data.port_changed != self.decoder_out_port:
            return 0
        self.decoder.c_app_data.port_changed = 0

        # Get buffer supplier for decoder output port.
        # With the printout disabled in the port settings changed event handler,
        # calling this method generates a PortUnpopulated error event even
        # though it does not return any error. This error is fatal after an
        # unpredictable number of continuous conversions. The solution seems
        # to be to put sufficient delay in the port settings changed handler
        # before returning from it.
        e, bs = self.decoder.GetBufferSupplier(self.decoder_out_port)
        if e != OMX_ErrorNone:
            print '%s: Failed to get buffer supplier for decoder output.'
            bs = OMX_BufferSupplyInput

        # Disable resizer input and decoder output.
        # Supplier port is disabled first and non-supplier port second.
        if bs == OMX_BufferSupplyInput: # Supplier is resizer input port.
            e |= self.resizer.DisablePort(self.resizer_in_port)
            e |= self.decoder.DisablePort(self.decoder_out_port, self.timeout)
            self.resizer.WaitForPortDisabled(self.resizer_in_port, self.timeout)
        else:
            e |= self.decoder.DisablePort(self.decoder_out_port)
            e |= self.resizer.DisablePort(self.resizer_in_port, self.timeout)
            self.decoder.WaitForPortDisabled(self.decoder_out_port, self.timeout)

        # Set color format of decoder output port again.
        e |= self.decoder.SetImagePortFormat(
                self.decoder_out_port,
                OMX_IMAGE_CodingUnused,
                self.out_format)

        # Copy decoder output port settings to resizer input port.
        e |= self.CopyPortDefinition(
                self.decoder,
                self.decoder_out_port,
                self.resizer,
                self.resizer_in_port)

        # Re-nable non-supplier port first and supplier port second.
        # decoder output and resizer input ports.
        if bs == OMX_BufferSupplyInput: # Supplier is resizer input port.
            e |= self.decoder.EnablePort(self.decoder_out_port)
            e |= self.resizer.EnablePort(self.resizer_in_port, self.timeout)
            self.decoder.WaitForPortEnabled(self.decoder_out_port, self.timeout)
        else:
            e |= self.resizer.EnablePort(self.resizer_in_port)
            e |= self.decoder.EnablePort(self.decoder_out_port, self.timeout)
            self.resizer.WaitForPortEnabled(self.resizer_in_port, self.timeout)

        # Resizer output port should generate a settings change event.
        self.resizer.WaitForPortSettingsChanged(self.resizer_out_port)

        return e

    #---------------------------------------------------------------------------
    def FreeIOBuffers(self):
        """
        Make all input and output buffers available.
        """

        for n in range(self.num_in_buf):
            c_in_buf_hdr = self.decoder.c_app_data.pp_in_buf_hdr[n][0]
            c_in_buf_prv = ctypes.cast(c_in_buf_hdr.pAppPrivate, pBUFHDR_APPT)[0]
            c_in_buf_prv.buffer_free = 1

        for n in range(self.num_out_buf):
            c_out_buf_hdr = self.resizer.c_app_data.pp_out_buf_hdr[n][0]
            c_out_buf_prv = ctypes.cast(c_out_buf_hdr.pAppPrivate, pBUFHDR_APPT)[0]
            c_out_buf_prv.buffer_free = 1

    #---------------------------------------------------------------------------
    def ConvertFromFile(self, file_name):
        """
        Convert a JPEG image file to the specified color format and resize the
        converted image to the specified dimensions.
        
        Return value:
            <int>       Error code: 0 for failure, file size for success.
        """
        
        e = 0

        if self.alt_setup:
            cons_print('%s.%s: This cannot run with the alternate setup.' %
                (self.name, 'ConvertFromFile'))
            return e

        if not self.ready:
            cons_print('%s: Not ready.' % self.name)
            return e

        try:
            f = open(file_name)
        except IOError:
            cons_print('File %s not found.' % file_name)
            return e
            
        f_size = os.path.getsize(file_name)
        if f_size <= 0:
            f.close()
            return e

        with f:
            cons_print('%s: Converting file %s (%d bytes) to %s...' %
                (self.name, file_name, f_size, omx_color_format_names[self.out_format]))

            self.FreeIOBuffers()
            self.decoder.ResetCallbackPortFlags()
            self.resizer.ResetCallbackPortFlags()
            
            c_dec_dat = self.decoder.c_app_data
            c_rsz_dat = self.resizer.c_app_data

            to_read = f_size
            timer = 0
            first_load = True
            while ((c_dec_dat.port_eos != self.decoder_out_port) and
                   (timer < 1000)):
                while to_read > 0:
                    n_ibuf_used = 0
                    for n in range(self.num_in_buf):
                        cp_in_buf_hdr = c_dec_dat.pp_in_buf_hdr[n]
                        c_in_buf_prv = ctypes.cast(cp_in_buf_hdr[0].pAppPrivate, pBUFHDR_APPT)[0]

                        if not c_in_buf_prv.buffer_free:
                            continue
                        c_in_buf_prv.buffer_free = 0
                        n_ibuf_used += 1

                        c_in_buf = self.cpp_in_buf[n][0]
                        n_read = f.readinto(c_in_buf)
                        if n_read <= 0:
                            break
                        to_read -= n_read

                        cp_in_buf_hdr[0].nFilledLen = n_read
                        cp_in_buf_hdr[0].nOffset = 0
                        if to_read > 0:
                            cp_in_buf_hdr[0].nFlags = 0
                        else:
                            cp_in_buf_hdr[0].nFlags = OMX_BUFFERFLAG_EOS
                        self.decoder.EmptyThisBuffer(cp_in_buf_hdr)

                        # If first buffer load, wait for decoder output settings changed event.
                        if first_load:
                            first_load = False
                            self.decoder.WaitForPortSettingsChanged(self.decoder_out_port)
                        self.decoderHandleOutSettingsChanged()

                        if self.num_out_buf > 0:
                            cp_out_buf_hdr = c_rsz_dat.pp_out_buf_hdr[0]
#                            c_out_buf_prv = ctypes.cast(cp_out_buf_hdr[0].pAppPrivate, pBUFHDR_APPT)[0]
                            self.resizer.FillThisBuffer(cp_out_buf_hdr)

                        if to_read <= 0:
                            break

                    self.decoderHandleOutSettingsChanged()
                    
                    if n_ibuf_used <= 0:
                        time.sleep(0.001)

                self.decoderHandleOutSettingsChanged()

                time.sleep(0.001)
                timer += 1

            if c_dec_dat.port_eos == self.decoder_out_port:
                timer = 0
                while ((c_rsz_dat.port_filled != self.resizer_out_port) and
                       (timer < self.timeout)):
                    time.sleep(0.001)
                    timer += 1

                if c_rsz_dat.port_filled == self.resizer_out_port:
                    e = f_size
                    cons_print('%s: Conversion successful.' % self.name)

        return e

    #---------------------------------------------------------------------------
    def AltConvertFromFile(self, file_name):
        """
        Alternate Version
        Convert a JPEG image file to the specified color format and resize the
        converted image to the specified dimensions.
        
        Return value:
            <int>       Error code: 0 for failure, file size for success.
        """
        
        e = 0

        if not self.alt_setup:
            cons_print('%s.%s: This cannot run without the alternate setup.' %
                (self.name, 'AltConvertFromFile'))
            return e

        if not self.ready:
            cons_print('%s: Not ready.' % self.name)
            return e

        try:
            f = open(file_name)
        except IOError:
            cons_print('File %s not found.' % file_name)
            return e
        
        f_size = os.path.getsize(file_name)
        if f_size <= 0:
            f.close()
            return e

        with f:
            cons_print('%s: Converting file %s (%d bytes) to %s...' %
                (self.name, file_name, f_size, omx_color_format_names[self.out_format]))

            self.FreeIOBuffers()
            self.decoder.ResetCallbackPortFlags()
            self.resizer.ResetCallbackPortFlags()
            
            c_dec_dat = self.decoder.c_app_data
            c_rsz_dat = self.resizer.c_app_data

            to_read = f_size
            timer = 0
            while ((c_dec_dat.port_eos != self.decoder_out_port) and
                   (timer < 1000)):
                while to_read > 0:
                    n_ibuf_used = 0
                    for n in range(self.num_in_buf):
                        cp_in_buf_hdr = c_dec_dat.pp_in_buf_hdr[n]
                        c_in_buf_prv = ctypes.cast(cp_in_buf_hdr[0].pAppPrivate, pBUFHDR_APPT)[0]

                        if not c_in_buf_prv.buffer_free:
                            continue
                        c_in_buf_prv.buffer_free = 0
                        n_ibuf_used += 1

                        c_in_buf = self.cpp_in_buf[n][0]
                        n_read = f.readinto(c_in_buf)
                        if n_read <= 0:
                            break
                        to_read -= n_read

                        cp_in_buf_hdr[0].nFilledLen = n_read
                        cp_in_buf_hdr[0].nOffset = 0
                        if to_read > 0:
                            cp_in_buf_hdr[0].nFlags = 0
                        else:
                            cp_in_buf_hdr[0].nFlags = OMX_BUFFERFLAG_EOS
                        self.decoder.EmptyThisBuffer(cp_in_buf_hdr)

                        if self.num_out_buf == 0:
                            self.decoder.WaitForPortSettingsChanged(self.decoder_out_port)
                            if c_dec_dat.port_changed == self.decoder_out_port:
                                c_dec_dat.port_changed = 0
                                self.SetupPipe()

                        if self.num_out_buf > 0:
                            self.decoderHandleOutSettingsChanged()
                            
                            cp_out_buf_hdr = c_rsz_dat.pp_out_buf_hdr[0]
#                            c_out_buf_prv = ctypes.cast(cp_out_buf_hdr[0].pAppPrivate, pBUFHDR_APPT)[0]
                            self.resizer.FillThisBuffer(cp_out_buf_hdr)

                        if to_read <= 0:
                            break

                    if self.num_out_buf > 0:
                        self.decoderHandleOutSettingsChanged()
                        
                    if n_ibuf_used <= 0:
                        time.sleep(0.001)

                if self.num_out_buf > 0:
                    self.decoderHandleOutSettingsChanged()

                time.sleep(0.001)
                timer += 1

            if c_dec_dat.port_eos == self.decoder_out_port:
                timer = 0
                while ((c_rsz_dat.port_filled != self.resizer_out_port) and
                       (timer < self.timeout)):
                    time.sleep(0.001)
                    timer += 1

                if c_rsz_dat.port_filled == self.resizer_out_port:
                    e = f_size
                    cons_print('%s: Conversion successful.' % self.name)

        return e

#===============================================================================

if __name__ == '__main__':

    jpg_dec = JPEGDecoder(out_width=1104, out_height=621)

    fn = '101.jpg'
    num_frames = 1000
    t1 = time.time()
    if not jpg_dec.alt_setup:
        for n in range(num_frames):
            jpg_dec.ConvertFromFile(fn)
            print n+1
    else:
        for n in range(num_frames):
            jpg_dec.AltConvertFromFile(fn)
            print n+1
    t2 = time.time()
    dt = t2 - t1
    print 'Elapsed time: %.3f s' % dt
    print 'Frames/sec: %.3f' % (num_frames/dt)
    
    jpg_dec.Close()

    # Wait a little to allow JPEG decoder to really close before
    # de-initializing OpenMAX IL core.
    time.sleep(.25)
    e = OMX_Deinit()
    assert (e == OMX_ErrorNone)

