"""
Module Name: omxilc.py
Version: 1.1 (2014-10-17)
Python Version: 2.7.3

This module defines classes for writing OMX IL client applications.
It is based on the file ilclient.c developed by Broadcom which defines an IL
client side library. It is also based on the python module pyopenmax.py
developed by Peter de Rivaz.

Copyright (c) 2014 Binh Bui

Redistribution and use in source and binary forms, with or without
modification, are permitted.
"""
#===============================================================================
#  ilclient.c
#
#  Copyright (c) 2012, Broadcom Europe Ltd
#  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are met:
#      * Redistributions of source code must retain the above copyright
#        notice, this list of conditions and the following disclaimer.
#      * Redistributions in binary form must reproduce the above copyright
#        notice, this list of conditions and the following disclaimer in the
#        documentation and/or other materials provided with the distribution.
#      * Neither the name of the copyright holder nor the
#        names of its contributors may be used to endorse or promote products
#        derived from this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
#  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
#  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
#  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
#  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
#  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
#  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
#  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#  POSSIBILITY OF SUCH DAMAGE.
#
#===============================================================================
#  pyopenmax.py
#
#  Copyright (c) 2012 Peter de Rivaz
# 
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted.
#
#  Raspberry Pi Video Decode Demo using OpenMAX IL via Python
#
#  Version 0.1 Now playback is at real time
#  Version 0.2 Added abiility to pause/resume/seek
#
#===============================================================================

from omx_component import *     # This also imports all other OMX IL modules.
from omxnames import *
import time

import omxerr       # Import this module to enable error printouts.
_verbose = False     # Set this variable to True to enable console printouts.

#-------------------------------------------------------------------------------
# Flags for controlling the creation of a component.
# These are taken from Broadcom ilclient.h.

ILCLIENT_FLAGS_NONE            = 0x00   # Used if no flags are set.

ILCLIENT_ENABLE_INPUT_BUFFERS  = 0x01   # If set, input ports are allowed to
                                        # communicate with a client via buffer
                                        # communication rather than tunneling
                                        # with another component.

ILCLIENT_ENABLE_OUTPUT_BUFFERS = 0x02   # If set, output ports are allowed to
                                        # communicate with a client via buffer
                                        # communication rather than tunneling
                                        # with another component.

ILCLIENT_DISABLE_ALL_PORTS     = 0x04   # If set, all ports are disabled on
                                        # creation.

ILCLIENT_HOST_COMPONENT        = 0x08   # Create a host component.
                                        # The default host ilcore only can
                                        # create host components by being
                                        # locally hosted. So this should only
                                        # be used for testing purposes.

ILCLIENT_OUTPUT_ZERO_BUFFERS   = 0x10   # All output ports will have
                                        # nBufferCountActual set to zero if
                                        # supported by the component.

ILCLIENT_FLAGS_ALL             = 0x07   # All options except creation of host
                                        # component creation and zeroing of
                                        # actual output buffer counts.

#-------------------------------------------------------------------------------
# C structure of component data returned by callbacks for identifying source
# and updating its data.

class COMPONENT_CBDT(ctypes.Structure):
    pass

pCOMPONENT_CBDT = ctypes.POINTER(COMPONENT_CBDT)

COMPONENT_CBDT._fields_ = [
        ('name', ctypes.c_char*32),         # Name of component.
        ('handle', OMX_HANDLETYPE),         # Handle of component.
        ('in_tunnel_port', ctypes.c_int),   # Input tunnel port index.
        ('out_tunnel_port', ctypes.c_int),  # Output tunnel port index.
        ('source', pCOMPONENT_CBDT),        # Source component of input tunnel.
        ('sink', pCOMPONENT_CBDT),          # Sink component of output tunnel.
        ('num_in_buf_hdr', ctypes.c_int),   # Number of input buffer headers.
        ('num_out_buf_hdr', ctypes.c_int),  # Number of output buffer headers.
        ('pp_in_buf_hdr', ppOMX_BUFFERHEADERTYPE),  # Input buffer header
                                                    # pointer array.
        ('pp_out_buf_hdr', ppOMX_BUFFERHEADERTYPE), # Output buffer header
                                                    # pointer array.
        ('method', ctypes.c_char*32),       # Name of method/function.
        ('cmd_complete', ctypes.c_int),     # Last command has completed.
        ('current_state', ctypes.c_int),    # Current state of component.
        ('port_flushed', ctypes.c_int),     # Flushed port index.
        ('port_disabled', ctypes.c_int),    # Disabled port index.
        ('port_enabled', ctypes.c_int),     # Enabled port index.
        ('port_buf_marked', ctypes.c_int),  # Port index that marked a buffer.
        ('port_changed', ctypes.c_int),     # Port index with settings changed.
        ('port_eos', ctypes.c_int),         # Port index that detected end of stream.
        ('port_emptied', ctypes.c_int),     # Port index with buffer emptied.
        ('port_filled', ctypes.c_int),      # Port index with buffer filled.
        ('event_error', ctypes.c_uint)]     # Error code from event handler.

#-------------------------------------------------------------------------------
# C structure of private data for a buffer header.

class BUFHDR_APPT(ctypes.Structure):
    pass

pBUFHDR_APPT = ctypes.POINTER(BUFHDR_APPT)

BUFHDR_APPT._fields_ = [
        ('buffer_index', ctypes.c_int),     # Buffer index (0, 1, ...).
        ('port_index', ctypes.c_int),       # Port index that uses buffer.
        ('buffer_free', ctypes.c_int)]      # 0 = filled; 1 = free.

#-------------------------------------------------------------------------------
# cons_print
# Function to print variable-length arguments to the console.
# Set _verbose to True to enable console printouts.

if '_verbose' not in dir():
    _verbose = False

if _verbose:
    _cons_print_locked = 0
    def cons_print(*args):
        global _cons_print_locked
        while _cons_print_locked:
            time.sleep(0.001)
        _cons_print_locked = 1
        for arg in args:
            print arg,
        print ''
        _cons_print_locked = 0
else:
    def cons_print(*args):
        pass

#-------------------------------------------------------------------------------
# print_error
# Function to print the name of an error detected by a component, or resulted
# from the unsuccessful execution of a method or function.
# Import omxerr to enable error printouts.

if 'omxerr' in dir():
    if 'OMXError' in dir(omxerr):
        omx_error = omxerr.OMXError()
elif 'OMXError' in dir():
    omx_error = OMXError()

if 'omx_error' in dir():
    if 'Print' in dir(omx_error):
	    print_error = omx_error.Print

if 'print_error' not in dir():
    def print_error(error, comp_name='', method=''):
        pass

if _verbose:
    cons_print_error = print_error
else:
    def cons_print_error(error, comp_name='', method=''):
        pass

#-------------------------------------------------------------------------------
# Default EventHandler callback for components.
def _defEventHandler(cv_handle, cp_app_data, event, data1, data2, cp_event_data):

    cp_comp = ctypes.cast(cp_app_data, pCOMPONENT_CBDT)
    c_comp = cp_comp[0]

    if event == OMX_EventCmdComplete:
        c_comp.cmd_complete = 1
#        cons_print('%s event: %s complete.' %
#            (c_comp.name, omx_cmd_names[data1]))

        if data1 == OMX_CommandStateSet:
            c_comp.current_state = data2    # state reached
            cons_print('%s event: Now in %s.' %
                (c_comp.name, omx_state_names[data2]))

        elif data1 == OMX_CommandFlush:
            c_comp.port_flushed = data2
            cons_print('%s event: Port %d flushed.' % (c_comp.name, data2))

        elif data1 == OMX_CommandPortDisable:
            c_comp.port_disabled = data2
            if data2 == c_comp.port_enabled:
                c_comp.port_enabled = 0
            cons_print('%s event: Port %d disabled.' % (c_comp.name, data2))

        elif data1 == OMX_CommandPortEnable:
            c_comp.port_enabled = data2
            if data2 == c_comp.port_disabled:
                c_comp.port_disabled = 0
            cons_print('%s event: Port %d enabled.' % (c_comp.name, data2))

        elif data1 == OMX_CommandMarkBuffer:
            c_comp.port_buf_marked = data2
            cons_print('%s event: Buffer marked by port %d.' %
                (c_comp.name, data2))

    elif event == OMX_EventError:
        c_comp.event_error = data1
        if data1 == OMX_ErrorSameState:
            cons_print_error(data1, c_comp.name + ' event', ' ' + c_comp.method)
        else:
            print_error(data1, c_comp.name + ' event', ' ' + c_comp.method)

    elif event == OMX_EventMark:
        cons_print('%s event: Marked buffer received.' % c_comp.name)

    elif event == OMX_EventPortSettingsChanged:
        c_comp.port_changed = data1
        cons_print('%s event: Port %d settings changed.' % (c_comp.name, data1))

    elif event == OMX_EventBufferFlag:
        c_comp.port_eos = data1
        cons_print('%s event: EOS detected by port %d.' % (c_comp.name, data1))

    else:
        cons_print('%s event:' % c_comp.name, event, data1, data2)

    return OMX_ErrorNone

#-------------------------------------------------------------------------------
# Default EmptyBufferDone callback for components.

def _defEmptyBufferDone(cv_handle, cp_app_data, cp_buffer):

    cp_comp = ctypes.cast(cp_app_data, pCOMPONENT_CBDT)
    cp_app = ctypes.cast(cp_buffer[0].pAppPrivate, pBUFHDR_APPT)
    if cp_buffer[0].nFilledLen == 0:
        cp_app[0].buffer_free = 1
    cp_comp[0].port_emptied = cp_app[0].port_index

    cons_print('%s callback: Port %d buffer %d emptied (%d bytes left).' %
        (cp_comp[0].name, cp_app[0].port_index, cp_app[0].buffer_index,
         cp_buffer[0].nFilledLen))

    return OMX_ErrorNone

def _defEmptyBufferDoneError(cv_handle, cp_app_data, cp_buffer):

    cp_comp = ctypes.cast(cp_app_data, pCOMPONENT_CBDT)

    cons_print('%s callback: EmptyBuffer done error.' % cp_comp[0].name)

    return OMX_ErrorNone

#-------------------------------------------------------------------------------
# Default FillBufferDone callback for components.

def _defFillBufferDone(cv_handle, cp_app_data, cp_buffer):

    cp_comp = ctypes.cast(cp_app_data, pCOMPONENT_CBDT)
    cp_app = ctypes.cast(cp_buffer[0].pAppPrivate, pBUFHDR_APPT)
    if cp_buffer[0].nFilledLen > 0:
        cp_app[0].buffer_free = 0
    cp_comp[0].port_filled = cp_app[0].port_index

    cons_print('%s callback: Port %d buffer %d filled (%d bytes).' %
        (cp_comp[0].name, cp_app[0].port_index, cp_app[0].buffer_index,
         cp_buffer[0].nFilledLen))

    return OMX_ErrorNone

def _defFillBufferDoneError(cv_handle, cp_app_data, cp_buffer):

    cp_comp = ctypes.cast(cp_app_data, pCOMPONENT_CBDT)

    cons_print('%s callback: FillBuffer done error.' % cp_comp[0].name)

    return OMX_ErrorNone

#===============================================================================
# OMX IL Component Class
#===============================================================================

class omxComponent(object):
    """OpenMAX Integration Layer Component Class"""

    def __init__(self, name, flags=ILCLIENT_FLAGS_NONE, timeout=0):
        """
        Parameters:
            name        <str>       Name of component to create.
            flags       <int>       Option flags (optional).
            timeout     <int>       Time-out in ms (optional).
        """

        self.name = name
        self.flags = flags
        self.timeout = timeout

        # Initialize component handle to null.
        self.cv_handle = OMX_HANDLETYPE()   # void pointer
        self.c_handle = ctypes.cast(self.cv_handle, pOMX_COMPONENTTYPE)

        # Create a C structure of component data that will be returned by
        # callbacks for identifying source and updating its data.
        self.c_app_data = COMPONENT_CBDT()
        self.c_app_data.name = self.name[:31]

        # Create a C structure of default callback functions.
        self.c_callbacks = OMX_CALLBACKTYPE()

        cfp = CFP_EVENT_HANDLER(_defEventHandler)
        self.c_callbacks.EventHandler = cfp

        if self.flags & ILCLIENT_ENABLE_INPUT_BUFFERS:
            cfp = CFP_EMPTY_BUFFER_DONE(_defEmptyBufferDone)
            self.c_callbacks.EmptyBufferDone = cfp
        else:
            cfp = CFP_EMPTY_BUFFER_DONE(_defEmptyBufferDoneError)
            self.c_callbacks.EmptyBufferDone = cfp

        if self.flags & ILCLIENT_ENABLE_OUTPUT_BUFFERS:
            cfp = CFP_FILL_BUFFER_DONE(_defFillBufferDone)
            self.c_callbacks.FillBufferDone = cfp
        else:
            cfp = CFP_FILL_BUFFER_DONE(_defFillBufferDoneError)
            self.c_callbacks.FillBufferDone = cfp

        # Open component.
        self.Open()

        # Ensure that component is opened.
        if not self.cv_handle:
            return

        # Get current state of component.
        e, state = self.GetState()

        # Find all input and output ports.
        self.num_ports = {}         # number of ports for all domains
        self.num_in_ports = {}      # numbers of input ports for all domains
        self.num_out_ports = {}     # numbers of output ports for all domains
        self.port_indices = {}      # port indices for each existed domain
        self.in_port_indices = {}   # input port indices for each existed domain
        self.out_port_indices = {}  # output port indices for each existed domain

        for port_domain in omx_component_domains:
            e, c_port_param = self.GetPorts(port_domain)
            if e != OMX_ErrorNone:
                continue

            domain_name = omx_component_domain_names[port_domain -
                                                     OMX_IndexParamAudioInit]

            # Save number of ports for this domain.
            self.num_ports[domain_name] = c_port_param.nPorts

            self.num_in_ports[domain_name] = 0
            self.num_out_ports[domain_name] = 0

            if c_port_param.nPorts <= 0:    # This domain has no ports.
                continue

            for n in xrange(c_port_param.nPorts):
                port_index = c_port_param.nStartPortNumber + n

                # Save port index.
                key = '%s%d' % (domain_name, n+1)
                self.port_indices[key] = port_index

                e, c_port_def = self.GetPortDefinition(port_index)
                if e != OMX_ErrorNone:
                    continue

                # Port is input. Update input port count and save index.
                if c_port_def.eDir == OMX_DirInput:
                    self.num_in_ports[domain_name] += 1
                    key = '%s%d' %(domain_name, self.num_in_ports[domain_name])
                    self.in_port_indices[key] = port_index

                # Port is output. Update output port count and save index.
                else:
                    self.num_out_ports[domain_name] += 1
                    key = '%s%d' %(domain_name, self.num_out_ports[domain_name])
                    self.out_port_indices[key] = port_index

        # Disable all ports if instructed.
        if self.flags & ILCLIENT_DISABLE_ALL_PORTS:
            self.DisableAllPorts(timeout)

        # Zero actual buffer count of all output ports if instructed.
        if self.flags & ILCLIENT_OUTPUT_ZERO_BUFFERS:
            self.ZeroAllOutBufferCounts()

        # Empty lists of port buffers.
        self.c_in_buf_list = []
        self.c_out_buf_list = []

        # Empty lists of private structures for port buffer headers.
        self.c_in_buf_hdr_prv_list = []
        self.c_out_buf_hdr_prv_list = []

    #---------------------------------------------------------------------------
    def Open(self):
        """
        Open the component.
        """

        self.c_app_data.method = 'Open'

#        cons_print('%s: Creating component...' % self.name)

        # Add required prefix to component name.
        c_component_name = ctypes.create_string_buffer('OMX.broadcom.' +
                                                       self.name)

        # Create instance of component specified by name given.
        cv_handle = OMX_HANDLETYPE()    # component handle
        cp_app_data = ctypes.pointer(self.c_app_data)
        e = OMX_GetHandle(ctypes.byref(cv_handle),
                c_component_name,
                ctypes.cast(cp_app_data, OMX_PTR),
                ctypes.byref(self.c_callbacks))

        if e != OMX_ErrorNone:
            print '%s: Component not created.' % self.name
            return

        cons_print('%s: Component created.' % self.name)

        # Save component handle.
        self.cv_handle = cv_handle
        self.c_handle = ctypes.cast(self.cv_handle, pOMX_COMPONENTTYPE)
        self.c_app_data.handle = self.cv_handle

    #---------------------------------------------------------------------------
    def Close(self):
        """
        Close the component.
        The IL client application is responsible for bringing the component
        back to state Loaded before calling this method.

        Return value:
            <int>       Error code.
        """

        e = OMX_FreeHandle(self.cv_handle)
        print_error(e, self.name, 'Close')

        if e == OMX_ErrorNone:
            self.cv_handle = OMX_HANDLETYPE()   # void pointer
            self.c_handle = ctypes.cast(self.cv_handle, pOMX_COMPONENTTYPE)
            self.c_app_data.handle = self.cv_handle

            self.c_app_data.current_state = OMX_StateInvalid
            cons_print('%s: Closed.' % self.name)

        return e

    #---------------------------------------------------------------------------
    def DisableAllPorts(self, timeout=0):
        """
        Disable all ports in all domains (audio, video, image, and other) for
        the component.

        Parameters:
            timeout     <int>       Time-out in ms (optional). If > 0, this
                                    method will wait until a port is disabled
                                    or the time-out is reached before disabling
                                    another port.
        """

        for domain_name in omx_component_domain_names:
            for n in xrange(self.num_ports[domain_name]):
                key = '%s%d' % (domain_name, n+1)
                self.DisablePort(self.port_indices[key], timeout)

    #---------------------------------------------------------------------------
    def WaitForState(self, state):
        """
        Wait until the component is in a specific state.

        Parameters:
            state           <int>       State to wait for.
        """

        timer = 0
        while ((self.c_app_data.current_state != state) and
                (timer < self.timeout)):
            time.sleep(0.001)
            timer += 1

        if self.c_app_data.current_state != state:
            cons_print('%s: State %s not reached after %d ms.' %
                (self.name, omx_state_names[state], self.timeout))

    #---------------------------------------------------------------------------
    def WaitForPortFlushed(self, port_index, timeout):
        """
        Wait until a port is flushed.

        Parameters:
            port_index      <int>       Index of port to wait.
            timeout         <int>       Time-out in ms.
        """

        timer = 0
        while ((self.c_app_data.port_flushed != port_index) and
                (timer < timeout)):
            time.sleep(0.001)
            timer += 1

        if self.c_app_data.port_flushed != port_index:
            cons_print('%s: Port %d not flushed after %d ms.' %
                (self.name, port_index, timeout))

    #---------------------------------------------------------------------------
    def WaitForPortDisabled(self, port_index, timeout):
        """
        Wait until a port is disabled.

        Parameters:
            port_index      <int>       Index of port to wait.
            timeout         <int>       Time-out in ms.
        """

#        timer = 0
#        while ((self.c_app_data.port_disabled != port_index) and
#                (timer < timeout)):
#            time.sleep(0.001)
#            timer += 1
#        if self.c_app_data.port_disabled != port_index:
#            cons_print('%s: Port %d not disabled after %d ms.' %
#                (self.name, port_index, timeout))

        timer = 0
        e, c_port_def = self.GetPortDefinition(port_index)
        while (c_port_def.bEnabled and (timer < timeout)):
            time.sleep(0.001)
            timer += 1
            e, c_port_def = self.GetPortDefinition(port_index)

        if c_port_def.bEnabled:
            cons_print('%s: Port %d not disabled after %d ms.' %
                (self.name, port_index, timeout))

    #---------------------------------------------------------------------------
    def WaitForPortEnabled(self, port_index, timeout):
        """
        Wait until a port is enabled.

        Parameters:
            port_index      <int>       Index of port to wait.
            timeout         <int>       Time-out in ms.
        """

#        timer = 0
#        while ((self.c_app_data.port_enabled != port_index) and
#                (timer < timeout)):
#            time.sleep(0.001)
#            timer += 1
#        if self.c_app_data.port_enabled != port_index:
#            cons_print('%s: Port %d not enabled after %d ms.' %
#                (self.name, port_index, timeout))

        timer = 0
        e, c_port_def = self.GetPortDefinition(port_index)
        while (not c_port_def.bEnabled and (timer < timeout)):
            time.sleep(0.001)
            timer += 1
            e, c_port_def = self.GetPortDefinition(port_index)

        if not c_port_def.bEnabled:
            cons_print('%s: Port %d not enabled after %d ms.' %
                (self.name, port_index, timeout))

    #---------------------------------------------------------------------------
    def WaitForPortSettingsChanged(self, port_index):
        """
        Wait for a settings changed event for a port.

        Parameters:
            port_index      <int>       Index of port to wait for event.

        Return value:
            <int>       Error code.
        """

        timer = 0
        while ((self.c_app_data.port_changed != port_index) and
                (timer < self.timeout)):
            # Quit waiting on StreamCorrupt error event.
            e = self.c_app_data.event_error
            if e != OMX_ErrorNone:
                self.c_app_data.event_error = OMX_ErrorNone
                if e == OMX_ErrorStreamCorrupt:
                    return e
            time.sleep(0.001)
            timer += 1

        if self.c_app_data.port_changed == port_index:
            return 0

        cons_print('%s: No settings changed event for port %d after %d ms.'
            % (self.name, port_index, self.timeout))
        return 1

    #---------------------------------------------------------------------------
    def WaitForBufferEmpty(self, port_index, timeout):
        """
        Wait until a port buffer is empty.

        Parameters:
            port_index      <int>       Index of port to wait.
            timeout         <int>       Time-out in ms.

        Return value:
            <int>       Error code.
        """

        timer = 0
        while ((self.c_app_data.port_emptied != port_index) and
                (timer < timeout)):
            time.sleep(0.001)
            timer += 1

        if self.c_app_data.port_emptied == port_index:
            return 0

        cons_print('%s: Port %d buffer not empty after %d ms.' %
            (self.name, port_index, timeout))
        return 1

    #---------------------------------------------------------------------------
    def WaitForBufferFilled(self, port_index, timeout):
        """
        Wait until a port buffer is filled.

        Parameters:
            port_index      <int>       Index of port to wait.
            timeout         <int>       Time-out in ms.

        Return value:
            <int>       Error code.
        """

        timer = 0
        while ((self.c_app_data.port_filled != port_index) and
                (timer < timeout)):
            time.sleep(0.001)
            timer += 1

        if self.c_app_data.port_filled == port_index:
            return 0

        cons_print('%s: Port %d buffer not filled after %d ms.' %
            (self.name, port_index, timeout))
        return 1

    #---------------------------------------------------------------------------
    def ResetCallbackPortFlags(self):
        """
        Reset all port flags in the component structure returned by callbacks.
        """

        self.c_app_data.port_flushed = 0
        self.c_app_data.port_disabled = 0
        self.c_app_data.port_enabled = 0
        self.c_app_data.port_buf_marked = 0
        self.c_app_data.port_changed = 0
        self.c_app_data.port_eos = 0
        self.c_app_data.port_emptied = 0
        self.c_app_data.port_filled = 0
        self.c_app_data.event_error = OMX_ErrorNone

    #---------------------------------------------------------------------------
    def PlaceOutTunnel(self, out_port, sink_component, sink_port):
        """
        Set up an output tunnel to a sink component.

        Parameters:
            out_port        <int>       Output port index.
            sink_component  <object>    Sink component.
            sink_port       <int>       Input port index of sink component.

        Return value:
            <int>       Error code.
        """

        # Set up output tunnel.
        e = OMX_SetupTunnel(self.cv_handle, out_port,
                sink_component.cv_handle, sink_port)
        print_error(e, self.name, 'OMX_SetupTunnel')

        if e == OMX_ErrorNone:
            self.c_app_data.out_tunnel_port = out_port
            self.c_app_data.sink = ctypes.pointer(sink_component.c_app_data)
            sink_component.c_app_data.in_tunnel_port = sink_port
            sink_component.c_app_data.source = ctypes.pointer(self.c_app_data)
            cons_print('%s: Tunnel placed from port %d to port %d of %s.' %
                (self.name, out_port, sink_port, sink_component.name))

        return e

    #---------------------------------------------------------------------------
    def RemoveOutTunnel(self):
        """
        Remove the output tunnel to a sink component.

        Return value:
            <int>       Error code.
        """

        if not self.c_app_data.sink:
            return OMX_ErrorNone

        sink = self.c_app_data.sink[0]

        e = OMX_SetupTunnel(self.cv_handle, self.c_app_data.out_tunnel_port,
                OMX_HANDLETYPE(), sink.in_tunnel_port)
        e |= OMX_SetupTunnel(OMX_HANDLETYPE(), self.c_app_data.out_tunnel_port,
                sink.handle, sink.in_tunnel_port)
        print_error(e, self.name, 'OMX_SetupTunnel')
        if e == OMX_ErrorNone:
            cons_print('%s: Tunnel from port %d to port %d of %s removed.' %
                (self.name, self.c_app_data.out_tunnel_port,
                 sink.in_tunnel_port, sink.name))

        return e

    #---------------------------------------------------------------------------
    def SupplyAllBuffers(self, port_index, buffer_size):
        """
        This method is called by an IL client to allocate and supply all
        required buffers to a port of the component.

        Parameters:
            port_index      <int>       Index of port to use buffers.
            buffer_size     <int>       Size of a buffer in bytes.

        Return values:
            <int>       Error code.
            <c_pointer> Array of pointers to ctypes.c_char buffers.
        """

        self.c_app_data.method = 'SupplyAllBuffers'

        CP = ctypes.c_char*buffer_size
        CPP = ctypes.POINTER(CP)

        e, c_port_def = self.GetPortDefinition(port_index)
        if (e != OMX_ErrorNone) or (c_port_def.nBufferCountActual <= 0):
            return e, (CPP*0)()

        dir_names = ('input', 'output')
        cons_print('%s: Client supplying %d buffer(s) to %s port %d...' %
            (self.name, c_port_def.nBufferCountActual,
            dir_names[c_port_def.eDir], port_index))

        if buffer_size < c_port_def.nBufferSize:
            buffer_size = c_port_def.nBufferSize
            cons_print('%s: Port %d buffer size increased to %d.' %
                (self.name, port_index, buffer_size))
            CP = ctypes.c_char*buffer_size
            CPP = ctypes.POINTER(CP)

        cpp_buf = (CPP*c_port_def.nBufferCountActual)()
        cpp_buf_hdr = (pOMX_BUFFERHEADERTYPE*c_port_def.nBufferCountActual)()

        # Delete existing lists of port buffers and private structures for port
        # buffer headers.
        if c_port_def.eDir == OMX_DirInput:
            if len(self.c_in_buf_list) > 0:
                del self.c_in_buf_list
                self.c_in_buf_list = []
            if len(self.c_in_buf_hdr_prv_list) > 0:
                del self.c_in_buf_hdr_prv_list
                self.c_in_buf_hdr_prv_list = []
        else:
            if len(self.c_out_buf_list) > 0:
                del self.c_out_buf_list
                self.c_out_buf_list = []
            if len(self.c_out_buf_hdr_prv_list) > 0:
                del self.c_out_buf_hdr_prv_list
                self.c_out_buf_hdr_prv_list = []

        for n in xrange(c_port_def.nBufferCountActual):
            if c_port_def.eDir == OMX_DirInput:
                # Allocate a port buffer.
                self.c_in_buf_list.append(CP())

                # Allocate a private structure for port buffer header.
                self.c_in_buf_hdr_prv_list.append(BUFHDR_APPT())
                self.c_in_buf_hdr_prv_list[n].buffer_index = n
                self.c_in_buf_hdr_prv_list[n].port_index = port_index
                self.c_in_buf_hdr_prv_list[n].buffer_free = 1

                e, cp_buf_hdr = self.UseBuffer(
                        port_index,
                        ctypes.pointer(self.c_in_buf_hdr_prv_list[n]),
                        buffer_size,
                        ctypes.cast(self.c_in_buf_list[n], OMX_BYTE))
            else:
                # Allocate a port buffer.
                self.c_out_buf_list.append(CP())

                # Allocate a private structure for port buffer header.
                self.c_out_buf_hdr_prv_list.append(BUFHDR_APPT())
                self.c_out_buf_hdr_prv_list[n].buffer_index = n
                self.c_out_buf_hdr_prv_list[n].port_index = port_index
                self.c_out_buf_hdr_prv_list[n].buffer_free = 1

                e, cp_buf_hdr = self.UseBuffer(
                        port_index,
                        ctypes.pointer(self.c_out_buf_hdr_prv_list[n]),
                        buffer_size,
                        ctypes.cast(self.c_out_buf_list[n], OMX_BYTE))
            if e != OMX_ErrorNone:
                return e, (CPP*0)()
            cpp_buf[n] = ctypes.cast(cp_buf_hdr[0].pBuffer, CPP)
            cpp_buf_hdr[n] = cp_buf_hdr

        # Save number of buffers and array of pointers to buffer headers
        # in component data structure for callbacks.
        if c_port_def.eDir == OMX_DirInput:
            self.c_app_data.num_in_buf_hdr = c_port_def.nBufferCountActual
            self.c_app_data.pp_in_buf_hdr = ctypes.cast(cpp_buf_hdr,
                                                        ppOMX_BUFFERHEADERTYPE)
        else:
            self.c_app_data.num_out_buf_hdr = c_port_def.nBufferCountActual
            self.c_app_data.pp_out_buf_hdr = ctypes.cast(cpp_buf_hdr,
                                                         ppOMX_BUFFERHEADERTYPE)

#        dir_names = ('input', 'output')
#        cons_print('%s: %d buffer(s) supplied by client to %s port %d.' %
#            (self.name, c_port_def.nBufferCountActual,
#            dir_names[c_port_def.eDir], port_index))

        return (e,
                cpp_buf)

    #---------------------------------------------------------------------------
    def AllocateAllBuffers(self, port_index, buffer_size):
        """
        Request the component to allocate all required buffers for a port.

        Parameters:
            port_index      <int>       Index of port to use buffers.
            buffer_size     <int>       Size of a buffer in bytes.

        Return values:
            <int>       Error code.
            <c_pointer> Array of pointers to c_char buffers.
        """

        self.c_app_data.method = 'AllocateAllBuffers'

        CPP = ctypes.POINTER(ctypes.c_char*buffer_size)

        e, c_port_def = self.GetPortDefinition(port_index)
        if (e != OMX_ErrorNone) or (c_port_def.nBufferCountActual <= 0):
            return e, (CPP*0)()

        dir_names = ('input', 'output')
        cons_print('%s: Self allocating %d buffer(s) to %s port %d...' %
            (self.name, c_port_def.nBufferCountActual,
            dir_names[c_port_def.eDir], port_index))

        if buffer_size < c_port_def.nBufferSize:
            buffer_size = c_port_def.nBufferSize
            cons_print('%s: Port %d buffer size increased to %d.' %
                (self.name, port_index, buffer_size))
            CPP = ctypes.POINTER(ctypes.c_char*buffer_size)

        cpp_buf = (CPP*c_port_def.nBufferCountActual)()
        cpp_buf_hdr = (pOMX_BUFFERHEADERTYPE*c_port_def.nBufferCountActual)()

        # Delete existing lists of port buffers and private structures for port
        # buffer headers.
        if c_port_def.eDir == OMX_DirInput:
            if len(self.c_in_buf_list) > 0:
                del self.c_in_buf_list
                self.c_in_buf_list = []
            if len(self.c_in_buf_hdr_prv_list) > 0:
                del self.c_in_buf_hdr_prv_list
                self.c_in_buf_hdr_prv_list = []
        else:
            if len(self.c_out_buf_list) > 0:
                del self.c_out_buf_list
                self.c_out_buf_list = []
            if len(self.c_out_buf_hdr_prv_list) > 0:
                del self.c_out_buf_hdr_prv_list
                self.c_out_buf_hdr_prv_list = []

        for n in xrange(c_port_def.nBufferCountActual):
            if c_port_def.eDir == OMX_DirInput:
                # Allocate a private structure for port buffer header.
                self.c_in_buf_hdr_prv_list.append(BUFHDR_APPT())
                self.c_in_buf_hdr_prv_list[n].buffer_index = n
                self.c_in_buf_hdr_prv_list[n].port_index = port_index
                self.c_in_buf_hdr_prv_list[n].buffer_free = 1

                e, cp_buf_hdr = self.AllocateBuffer(
                    port_index,
                    ctypes.pointer(self.c_in_buf_hdr_prv_list[n]),
                    buffer_size)
            else:
                # Allocate a private structure for port buffer header.
                self.c_out_buf_hdr_prv_list.append(BUFHDR_APPT())
                self.c_out_buf_hdr_prv_list[n].buffer_index = n
                self.c_out_buf_hdr_prv_list[n].port_index = port_index
                self.c_out_buf_hdr_prv_list[n].buffer_free = 1

                e, cp_buf_hdr = self.AllocateBuffer(
                    port_index,
                    ctypes.pointer(self.c_out_buf_hdr_prv_list[n]),
                    buffer_size)
            if e != OMX_ErrorNone:
                return e, (CPP*0)()
            cpp_buf[n] = ctypes.cast(cp_buf_hdr[0].pBuffer, CPP)            
            cpp_buf_hdr[n] = cp_buf_hdr

        # Save number of buffers and array of pointers to buffer headers
        # in component data structure for callbacks.
        if c_port_def.eDir == OMX_DirInput:
            self.c_app_data.num_in_buf_hdr = c_port_def.nBufferCountActual
            self.c_app_data.pp_in_buf_hdr = ctypes.cast(cpp_buf_hdr,
                                                        ppOMX_BUFFERHEADERTYPE)
        else:
            self.c_app_data.num_out_buf_hdr = c_port_def.nBufferCountActual
            self.c_app_data.pp_out_buf_hdr = ctypes.cast(cpp_buf_hdr,
                                                         ppOMX_BUFFERHEADERTYPE)

#        dir_names = ('input', 'output')
#        cons_print('%s: %d buffer(s) allocated to %s port %d.' %
#            (self.name, c_port_def.nBufferCountActual,
#            dir_names[c_port_def.eDir], port_index))

        return (e,
                cpp_buf)

    #---------------------------------------------------------------------------
    # Component Level Methods
    # These methods have macros defined in OMX_Core.h.
    #---------------------------------------------------------------------------

    def GetComponentVersion(self):
        """
        Get the information about the component.

        Parameters:
            None

        Return values:
            <int>       Error code.
            <str>       Name of component.
            <int>       Version of component.
            <int>       Version of OpenMAX IL specification against which the
                        component was built.
            <str>       UUID of component (128 bytes).
        """

        c_comp_name = (ctypes.c_char*128)()
        c_comp_version = OMX_VERSIONTYPE()
        c_spec_version = OMX_VERSIONTYPE()
        c_comp_uuid = OMX_UUIDTYPE()
        e = self.c_handle[0].GetComponentVersion(self.cv_handle,
                c_comp_name,
                ctypes.byref(c_comp_version),
                ctypes.byref(c_spec_version),
                c_comp_uuid)
        print_error(e, self.name, 'GetComponentVersion')

        return (e,
                c_comp_name.value,
                c_comp_version.nVersion,
                c_spec_version.nVersion,
                ctypes.cast(c_comp_uuid, OMX_STRING)[:len(c_comp_uuid)])

    #---------------------------------------------------------------------------
    def SendCommand(self, cmd, param,
                    p_cmd_data=ctypes.POINTER(OMX_MARKTYPE)(), timeout=0):
        """
        Send a command to the component.

        Parameters:
            cmd         <int>       Command for the component to execute.
            param       <int>       Parameter for the command.
                                    When cmd is OMX_CommandStateSet,
                                    param is a member of OMX_STATETYPE.
                                    When cmd is OMX_CommandFlush,
                                    param indicates which port(s) to flush.
                                    -1 is used to flush all ports. A single port
                                    index will only flush that port.
                                    When Cmd is OMX_CommandPortDisable or
                                    OMX_CommandPortEnable, param specifies
                                    the component's port.
                                    When Cmd is OMX_CommandMarkBuffer,
                                    param specifies the component's port.
            p_cmd_data  <c_pointer> Pointer to OMX_MARKTYPE structure when cmd
                                    has the value OMX_CommandMarkBuffer
                                    (optional).
            timeout     <int>       Time-out in ms (optional). If > 0, this
                                    method will wait until the command completes
                                    or the time-out is reached.

        Return value:
            <int>       Error code.
        """

        self.c_app_data.cmd_complete = 0
        
        e = self.c_handle[0].SendCommand(self.cv_handle,
                cmd,
                param,
                ctypes.cast(p_cmd_data, OMX_PTR))
        print_error(e, self.name, 'SendCommand')

        if (e == OMX_ErrorNone) and (timeout > 0):
            timer = 0
            while ((self.c_app_data.cmd_complete == 0) and
                   (timer < timeout)):
                time.sleep(0.001)
                timer += 1

            if self.c_app_data.cmd_complete == 0:
                cons_print('%s: %s not complete within %d ms.' %
                    (self.name, omx_cmd_names[cmd], timeout))
#            else:
#                cons_print('%s: %s complete in %d ms.' %
#                    (self.name, omx_cmd_names[cmd], timer))

        return e

    #---------------------------------------------------------------------------
    def GetParameter(self, param_index, cp_param_struct):
        """
        Query the component for a parameter structure specified by an index.
        Before the query, the method will fill the structure with its size and
        version information. The remaining fields in the structure will be
        filled by the component.

        Parameters:
            param_index     <int>       Index of structure to be filled.
            cp_param_struct <c_pointer> Pointer to structure to be filled.

        Return value:
            <int>       Error code.
        """

        cp_param_struct[0].nSize = ctypes.sizeof(cp_param_struct[0])
        cp_param_struct[0].nVersion = OMX_VERSIONTYPE(nVersion=OMX_VERSION)

        e = self.c_handle[0].GetParameter(self.cv_handle,
                param_index,
                ctypes.cast(cp_param_struct, OMX_PTR))
        print_error(e, self.name, 'GetParameter')

        return e

    #---------------------------------------------------------------------------
    def SetParameter(self, param_index, cp_param_struct):
        """
        Send a parameter structure specified by an index to the component.
        Before sending the structure, the method will fill the structure with
        its size and version information. The remaining fields in the structure
        must be filled by the caller.
   
        Parameters:
            param_index     <int>       Index of structure to be sent.
            cp_param_struct <c_pointer> Pointer to structure to be sent.

        Return value:
            <int>       Error code.
        """

        cp_param_struct[0].nSize = ctypes.sizeof(cp_param_struct[0])
        cp_param_struct[0].nVersion = OMX_VERSIONTYPE(nVersion=OMX_VERSION)

        e = self.c_handle[0].SetParameter(self.cv_handle,
                param_index,
                ctypes.cast(cp_param_struct, OMX_PTR))
        print_error(e, self.name, 'SetParameter')

        return e

    #---------------------------------------------------------------------------
    def GetConfig(self, cfg_index, cp_cfg_struct):
        """
        Query the component for a configuration structure specified by an index.
        Before the query, the method will fill the structure with its size and
        version information. The remaining fields in the structure will be
        filled by the component.

        Parameters:
            cfg_index       <int>       Index of structure to be filled.
            cp_cfg_struct   <c_pointer> Pointer to structure to be filled.

        Return value:
            <int>       Error code.
        """

        cp_cfg_struct[0].nSize = ctypes.sizeof(cp_cfg_struct[0])
        cp_cfg_struct[0].nVersion = OMX_VERSION

        e = self.c_handle[0].GetConfig(self.cv_handle,
                cfg_index,
                ctypes.cast(cp_cfg_struct, OMX_PTR))
        print_error(e, self.name, 'GetConfig')

        return e

    #---------------------------------------------------------------------------
    def SetConfig(self, cfg_index, cp_cfg_struct):
        """
        Send a configuration structure specified by an index to the component.
        Before sending the structure, the method will fill the structure with
        its size and version information. The remaining fields in the structure
        must be filled by the caller.

        Parameters:
            cfg_index       <int>       Index of structure to be sent.
            cp_cfg_struct   <c_pointer> Pointer to structure to be sent.

        Return value:
            <int>       Error code.
        """

        cp_cfg_struct[0].nSize = ctypes.sizeof(cp_cfg_struct[0])
        cp_cfg_struct[0].nVersion = OMX_VERSION

        e = self.c_handle[0].SetConfig(self.cv_handle,
                cfg_index,
                ctypes.cast(cp_cfg_struct, OMX_PTR))
        print_error(e, self.name, 'SetConfig')

        return e

    #---------------------------------------------------------------------------
    def GetExtensionIndex(self, param_name):
        """
        Translate a vendor specific configuration or parameter string into an
        OMX structure index.
   
        Parameters:
            param_name      <str>       config./parameter string (<= 127 bytes)

        Return values:
            <int>       Error code.
            <int>       OMX structure index.
        """

        c_param_name = ctypes.create_string_buffer(param_name, 128)
        c_param_name[-1] = '\x00'

        c_index = OMX_INDEXTYPE()
        e = self.c_handle[0].GetExtensionIndex(self.cv_handle,
                c_param_name,
                ctypes.byref(c_index))
        print_error(e, self.name, 'GetExtensionIndex')

        return (e,
                c_index.value)

    #---------------------------------------------------------------------------
    def GetState(self):
        """
        Get the current state of the component.

        Parameters:
            None

        Return values:
            <int>       Error code.
            <int>       State value from OMX_STATETYPE enumeration.
        """

        c_state = OMX_STATETYPE()
        e = self.c_handle[0].GetState(self.cv_handle,
                ctypes.byref(c_state))
        print_error(e, self.name, 'GetState')

        if e == OMX_ErrorNone:
            self.c_app_data.current_state = c_state.value
#            cons_print('%s: Currently in %s.' %
#                       (self.name, omx_state_names[c_state.value]))

        return (e,
                c_state.value)

    #---------------------------------------------------------------------------
    def UseBuffer(self, port_index, cp_app_private, buffer_size, cp_buffer):
        """
        Request the component to use a buffer already allocated by the IL
        client, or by another component, for a port. The component will allocate
        its own buffer header, fill it with the input parameters and return a
        pointer to the buffer header structure.

        Parameters:
            port_index      <int>       Index of port that will use the buffer.
            cp_app_private  <c_pointer> Pointer to implementation-specific
                                        memory area that is under responsibility
                                        of buffer supplier.
            buffer_size     <int>       Buffer size in bytes.
            cp_buffer       <c_pointer> Pointer to OMX_U8 buffer to be used.

        Return values:
            <int>       Error code.
            <c_pointer> Pointer to buffer header structure.
        """

        cp_buffer_hdr = pOMX_BUFFERHEADERTYPE()
        e = self.c_handle[0].UseBuffer(self.cv_handle,
                ctypes.byref(cp_buffer_hdr),
                port_index,
                ctypes.cast(cp_app_private, OMX_PTR),
                buffer_size,
                cp_buffer)
        print_error(e, self.name, 'UseBuffer')

        return (e,
                cp_buffer_hdr)

    #---------------------------------------------------------------------------
    def AllocateBuffer(self, port_index, cp_app_private, buffer_size):
        """
        Request the component to allocate a buffer and a buffer header for
        a port. The component will return a pointer to the buffer header
        structure.

        Parameters:
            port_index      <int>       Index of port with which buffer will be
                                        used.
            cp_app_private  <c_pointer> Pointer to implementation-specific
                                        memory area to fill buffer header.
            buffer_size     <int>       Size in bytes of buffer to allocate.

        Return values:
            <int>       Error code.
            <c_pointer> Pointer to buffer header structure.
        """

        cp_buffer_hdr = pOMX_BUFFERHEADERTYPE()
        e = self.c_handle[0].AllocateBuffer(self.cv_handle,
                ctypes.byref(cp_buffer_hdr),
                port_index,
                ctypes.cast(cp_app_private, OMX_PTR),
                buffer_size)
        print_error(e, self.name, 'AllocateBuffer')

        return (e,
                cp_buffer_hdr)

    #---------------------------------------------------------------------------
    def FreeBuffer(self, port_index, cp_buffer_hdr):
        """
        Release a buffer header from the component which was allocated using
        either AllocateBuffer or UseBuffer. If the component allocated the
        buffer, the component shall free the buffer and buffer header.

        Parameters:
            port_index      <int>       Index of port with which buffer is used.
            cp_buffer_hdr   <c_pointer> Pointer to buffer header structure.

        Return value:
            <int>       Error code.
        """

        e = self.c_handle[0].FreeBuffer(self.cv_handle,
                port_index,
                cp_buffer_hdr)
        print_error(e, self.name, 'FreeBuffer')

        return e

    #---------------------------------------------------------------------------
    def EmptyThisBuffer(self, cp_buffer_hdr):
        """
        Send a buffer full of data to an input port of the component.
        The component will empty the buffer and return it to the application
        via the EmptyBufferDone callback.

        Parameters:
            cp_buffer_hdr   <c_pointer> Pointer to buffer header structure.

        Return value:
            <int>       Error code.
        """

        self.c_app_data.method = 'EmptyThisBuffer'

        e = self.c_handle[0].EmptyThisBuffer(self.cv_handle,
                cp_buffer_hdr)
        print_error(e, self.name, 'EmptyThisBuffer')

        return e

    #---------------------------------------------------------------------------
    def FillThisBuffer(self, cp_buffer_hdr):
        """
        Send an empty buffer to an output port of the component.
        The component will fill the buffer and return it to the application
        via the FillBufferDone callback.

        Parameters:
            cp_buffer_hdr   <c_pointer> Pointer to buffer header structure.

        Return value:
            <int>       Error code.
        """

        self.c_app_data.method = 'FillThisBuffer'

        e = self.c_handle[0].FillThisBuffer(self.cv_handle,
                cp_buffer_hdr)
        print_error(e, self.name, 'FillThisBuffer')

        return e

    #---------------------------------------------------------------------------
    def UseEGLImage(self, port_index, cp_app_private, cp_egl_image):
        """
        Request the component to use an EGLImage provided by EGL, in place of
        using the UseBuffer method. The component will allocate its own buffer
        header, fill it with the input parameters and return a pointer to the
        buffer header structure.

        Parameters:
            port_index      <int>       Index of port with which buffer will be
                                        used.
            cp_app_private  <c_pointer> Pointer to implementation-specific
                                        memory area to fill buffer header.
            cp_egl_image    <c_pointer> Handle of EGL image to be used as
                                        buffer.

        Return values:
            <int>       Error code.
            <c_pointer> Pointer to buffer header structure.
        """

        cp_buffer_hdr = pOMX_BUFFERHEADERTYPE()
        e = self.c_handle[0].UseEGLImage(self.cv_handle,
                ctypes.byref(cp_buffer_hdr),
                port_index,
                ctypes.cast(cp_app_private, OMX_PTR),
                ctypes.cast(cp_egl_image, ctypes.c_void_p))
        print_error(e, self.name, 'UseEGLImage')

        return (e,
                cp_buffer_hdr)

    #---------------------------------------------------------------------------
    # Other Component Level Methods
    # These methods are mostly called by the component itself.
    #---------------------------------------------------------------------------

    def ComponentTunnelRequest(self, port,
                               c_other_handle, other_port, cp_tunnel_setup):
        """
        Interact with another OMX component to determine if tunneling is
        possible and to setup the tunneling. The return codes can be used to
        determine if tunneling is not possible or not supported.

        Parameters:
            port            <int>       Index of port that will participate in
                                        tunnel.
            c_other_handle  <c_pointer> Handle of other component that will
                                        participate in tunnel. When this handle
                                        is null, the specified port will be set
                                        up for non-tunneled communication with
                                        the IL client.
            other_port      <int>       Index of port of other component that
                                        will participate in tunnel.
            cp_tunnel_setup <c_pointer> Pointer to structure used for tunnelling
                                        negotiation between components.

        Return value:
            <int>       Error code.
        """

        e = self.c_handle[0].ComponentTunnelRequest(self.cv_handle,
                port,
                c_other_handle,
                other_port,
                cp_tunnel_setup)
        print_error(e, self.name, 'ComponentTunnelRequest')

        return e

    #---------------------------------------------------------------------------
    def SetCallbacks(self, cp_callbacks, cp_app_data):
        """
        Transfer a callback structure from the IL client to the component.

        Parameters:
            cp_callbacks    <c_pointer> Pointer to a OMX_CALLBACKTYPE structure.
            cp_app_data     <c_pointer> Pointer to application defined data that
                                        will be returned by callbacks for
                                        identifying source

        Return value:
            <int>       Error code.
        """

        e = self.c_handle[0].SetCallbacks(self.cv_handle,
                cp_callbacks,
                ctypes.cast(cp_app_data, OMX_PTR))
        print_error(e, self.name, 'SetCallbacks')

        return e

    #---------------------------------------------------------------------------
    def ComponentDeInit(self):
        """
        Deinitialize the component. This will free any resources allocated at
        component initialization. After this call, the component handle is no
        longer valid for further use.

        Parameters:
            None

        Return value:
            <int>       Error code.
        """

        e = self.c_handle[0].ComponentDeInit(self.cv_handle)
        print_error(e, self.name, 'ComponentDeInit')

        return e

    #---------------------------------------------------------------------------
    def ComponentRoleEnum(self, role_index):
        """
        Query the component for all supported roles.

        Parameters:
            role_index      <int>       Index of role being queried

        Return values:
            <int>       Error code.
            <str>       name of specified role(127 bytes max.).
        """

        c_role_name = (ctypes.c_char*128)()
        e = self.c_handle[0].ComponentRoleEnum(self.cv_handle,
            ctypes.cast(c_role_name, POINTER(OMX_U8)),
            role_index)
        print_error(e, self.name, 'ComponentRoleEnum')

        return (e,
                c_role_name.value)

    #---------------------------------------------------------------------------
    # Send Commands
    #---------------------------------------------------------------------------

    def ChangeState(self, state):
        """
        Request the component to transition into a new state.

        Parameters:
            state           <int>       new state for component

        Return value:
            <int>       Error code.
        """

        self.c_app_data.method = 'ChangeState'

        cons_print('%s: Going to %s...' %
                   (self.name, omx_state_names[state]))
        e = self.SendCommand(OMX_CommandStateSet, state)

        return e

    #---------------------------------------------------------------------------
    def FlushPort(self, port_index):
        """
        Flush a specific port or all ports.

        Parameters:
            port_index      <int>       Index of port to flush. If this is
                                        OMX_ALL, all ports will be flushed.

        Return value:
            <int>       Error code.
        """

        self.c_app_data.method = 'FlushPort'
        self.c_app_data.port_flushed = 0

#        cons_print('%s: Flushing port %d...' % (self.name, port_index))
        e = self.SendCommand(OMX_CommandFlush, port_index)

        return e

    #---------------------------------------------------------------------------
    def DisablePort(self, port_index, timeout=0):
        """
        Disable a specific port or all ports.

        Parameters:
            port_index      <int>       Index of port to disable. If this is
                                        OMX_ALL, all ports will be disabled.
            timeout         <int>       Time-out in ms (optional). If > 0, this
                                        method will wait until the port is
                                        disabled or the time-out is reached.

        Return value:
            <int>       Error code.
        """
        
        self.c_app_data.method = 'DisablePort'
        self.c_app_data.port_disabled = 0

#        cons_print('%s: Disabling port %d...' % (self.name, port_index))
        e = self.SendCommand(OMX_CommandPortDisable, port_index)
        if (e == OMX_ErrorNone) and (timeout > 0):
            self.WaitForPortDisabled(port_index, timeout)

        return e
  
    #---------------------------------------------------------------------------
    def EnablePort(self, port_index, timeout=0):
        """
        Enable a specific port or all ports.

        Parameters:
            port_index      <int>       Index of port to enable. If this is
                                        OMX_ALL, all ports will be enabled.
            timeout         <int>       Time-out in ms (optional). If > 0, this
                                        method will wait until the port is
                                        enabled or the time-out is reached.

        Return value:
            <int>       Error code.
        """

        self.c_app_data.method = 'EnablePort'
        self.c_app_data.port_enabled = 0

#        cons_print('%s: Enabling port %d...' % (self.name, port_index))
        e = self.SendCommand(OMX_CommandPortEnable, port_index)
        if (e == OMX_ErrorNone) and (timeout > 0):
            self.WaitForPortEnabled(port_index, timeout)

        return e
  
    #---------------------------------------------------------------------------
    def MarkBuffer(self, port_index, cp_mark):
        """
        Instruct a port to mark a buffer.

        Parameters:
            port_index      <int>       Index of port performing the mark.
            cp_mark         <c_pointer> Pointer to an OMX_MARKTYPE structure.

        Return value:
            <int>       Error code.
        """

        self.c_app_data.method = 'MarkBuffer'
        self.c_app_data.port_buf_marked = 0

        cons_print('%s: Port %d marking buffer...' % (self.name, port_index))
        e = self.SendCommand(OMX_CommandMarkBuffer, port_index, cp_mark)

        return e

    #---------------------------------------------------------------------------
    # Get Parameters
    #---------------------------------------------------------------------------

    def GetPorts(self, port_domain):
        """
        Get the number and starting index of ports of a domain (audio, image,
        video, or other) for the component.

        Parameters:
            port_domain     <int>       OMX_IndexParamAudioInit,
                                        OMX_IndexParamImageInit,
                                        OMX_IndexParamVideoInit, or
                                        OMX_IndexParamOtherInit.

        Return values:
            <int>       Error code.
            <c_struct>  OMX_PORT_PARAM_TYPE structure
        """

        self.c_app_data.method = 'GetPorts'

        c_port_param = OMX_PORT_PARAM_TYPE()
        e = self.GetParameter(port_domain, ctypes.pointer(c_port_param))

        assert (c_port_param.nSize == ctypes.sizeof(OMX_PORT_PARAM_TYPE))

#        if ((e == OMX_ErrorNone) and (c_port_param.nPorts > 0)):
#            domain_name = omx_component_domain_names[port_domain -
#                                                     OMX_IndexParamAudioInit]
#            cons_print('%s: Found %d %s ports starting at %d.' %
#                       (self.name, c_port_param.nPorts, domain_name,
#                        c_port_param.nStartPortNumber))

        return (e,
                c_port_param)
  
    #---------------------------------------------------------------------------
    def GetPortDefinition(self, port_index):
        """
        Get the definition of a port.

        Parameters:
            port_index      <int>       Index of port to get definition.

        Return values:
            <int>       Error code.
            <c_struct>  OMX_PARAM_PORTDEFINITIONTYPE structure
        """

        self.c_app_data.method = 'GetPortDefinition'

#        cons_print('%s: Getting port %d definition...' %
#                   (self.name, port_index))
        c_port_def = OMX_PARAM_PORTDEFINITIONTYPE()
        c_port_def.nPortIndex = port_index
        e = self.GetParameter(OMX_IndexParamPortDefinition,
                              ctypes.pointer(c_port_def))

        assert (c_port_def.nSize == ctypes.sizeof(OMX_PARAM_PORTDEFINITIONTYPE))

        return (e,
                c_port_def)
  
    #---------------------------------------------------------------------------
    def GetNumberStreams(self, port_index):
        """
        Get the number of available streams of a port.

        Parameters:
            port_index      <int>       Index of port to get definition.

        Return values:
            <int>       Error code.
            <int>       Number of available streams.
        """

        self.c_app_data.method = 'GetNumberStreams'

        c_param = OMX_PARAM_U32TYPE()
        c_param.nPortIndex = port_index
        e = self.GetParameter(OMX_IndexParamNumAvailableStreams,
                              ctypes.pointer(c_param))

        assert (c_param.nSize == ctypes.sizeof(OMX_PARAM_U32TYPE))

        return (e,
                c_param.nU32)
  
    #---------------------------------------------------------------------------
    def GetActiveStream(self, port_index):
        """
        Get the active stream index of a port.

        Parameters:
            port_index      <int>       Index of port to get definition.

        Return values:
            <int>       Error code.
            <int>       Active stream index.
        """

        self.c_app_data.method = 'GetActiveStream'

        c_param = OMX_PARAM_U32TYPE()
        c_param.nPortIndex = port_index
        e = self.GetParameter(OMX_IndexParamActiveStream,
                              ctypes.pointer(c_param))

        assert (c_param.nSize == ctypes.sizeof(OMX_PARAM_U32TYPE))

        return (e,
                c_param.nU32)
  
    #---------------------------------------------------------------------------
    def GetBufferSupplier(self, port_index):
        """
        Get the buffer supplier of a port.

        Parameters:
            port_index      <int>       Index of port to get definition.

        Return values:
            <int>       Error code.
            <int>       Buffer supplier code (0=unspecified, 1=input, 2=output).
        """

        self.c_app_data.method = 'GetBufferSupplier'

        c_param = OMX_PARAM_BUFFERSUPPLIERTYPE()
        c_param.nPortIndex = port_index
        e = self.GetParameter(OMX_IndexParamCompBufferSupplier,
                ctypes.pointer(c_param))

        assert (c_param.nSize == ctypes.sizeof(OMX_PARAM_BUFFERSUPPLIERTYPE))

        return (e,
                c_param.eBufferSupplier)
  
    #---------------------------------------------------------------------------
    # Set Parameters
    #---------------------------------------------------------------------------

    def SetPortDefinition(self, port_index, cp_port_def):
        """
        Set the definition of a port.

        Parameters:
            port_index      <int>       Index of port to get definition.
            cp_port_def     <c_pointer> Pointer to OMX_PARAM_PORTDEFINITIONTYPE
                                        structure.

        Return value:
            <int>       Error code.
        """

        self.c_app_data.method = 'SetPortDefinition'

#        type_names = ('audio', 'video', 'image', 'other')
#        cons_print('%s: Setting %s port %d definition...' %
#            (self.name, type_names[cp_port_def[0].eDomain], port_index))
        cp_port_def[0].nPortIndex = port_index
        e = self.SetParameter(OMX_IndexParamPortDefinition, cp_port_def)
        if e == OMX_ErrorNone:
            type_names = ('Audio', 'Video', 'Image', 'Other-type')
            cons_print('%s: %s port %d definition set.' %
                (self.name, type_names[cp_port_def[0].eDomain], port_index))

        return e

    #---------------------------------------------------------------------------
    def SetBufferCount(self, port_index, buffer_count):
        """
        Set the actual buffer count of a port.

        Parameters:
            port_index      <int>       Index of port to set buffer count.
            buffer_count    <int>       Desired buffer count.

        Return value:
            <int>       Error code.
        """

        self.c_app_data.method = 'SetBufferCount'

        e, c_port_def = self.GetPortDefinition(port_index)
        if e != OMX_ErrorNone:
            return e

        if buffer_count < c_port_def.nBufferCountMin:
            cons_print('%s.%s: Buffer count must be >= %d.' %
                (self.name, self.c_app_data.method, c_port_def.nBufferCountMin))
            return e
        
        c_port_def.nBufferCountActual = buffer_count
        e = self.SetPortDefinition(port_index, ctypes.pointer(c_port_def))

        return e
        
    #---------------------------------------------------------------------------
    def ZeroOutBufferCount(self, port_index):
        """
        Zero the actual buffer count of an output port.

        Parameters:
            port_index      <int>       Index of port to zero buffer count.
        """

        self.c_app_data.method = 'ZeroOutBufferCount'

        e, c_port_def = self.GetPortDefinition(port_index)
        if e != OMX_ErrorNone:
            return

        if ((c_port_def.eDir == OMX_DirInput) or
                (c_port_def.nBufferCountActual <= 0)):
            return

        c_port_def.nBufferCountActual = 0
        self.SetPortDefinition(port_index, ctypes.pointer(c_port_def))

    #---------------------------------------------------------------------------
    def ZeroAllOutBufferCounts(self):
        """
        Zero the actual buffer count of all output ports.
        """

        self.c_app_data.method = 'ZeroAllOutBufferCounts'

        for domain_name in omx_component_domain_names:
            for n in xrange(self.num_out_ports[domain_name]):
                key = '%s%d' % (domain_name, n+1)
                self.ZeroOutBufferCount(self.out_port_indices[key])

    #---------------------------------------------------------------------------
    def SetAudioPortFormat(self, port_index, coding):
        """
        Set the format of an audio port.

        Parameters:
            port_index      <int>       Index of port to set format.
            coding          <int>       Audio coding format.

        Return value:
            <int>       Error code.
        """

        self.c_app_data.method = 'SetAudioPortFormat'

        if self.num_ports['Audio'] <= 0:
            print '%s: Component has no audio port.' % self.name
            return OMX_ErrorNone

        for n in xrange(self.num_ports['Audio']):
            key = 'Audio%d' % (n+1)
            if port_index != self.port_indices[key]:
                continue

#            cons_print('%s: Setting audio port %d format...' %
#                (self.name, port_index))
            c_apf = OMX_AUDIO_PARAM_PORTFORMATTYPE()
            c_apf.nPortIndex = port_index
            c_apf.eEncoding = coding
            e = self.SetParameter(OMX_IndexParamAudioPortFormat,
                    ctypes.pointer(c_apf))
            if e == OMX_ErrorNone:
                cons_print('%s: Audio port %d format set.' %
                    (self.name, port_index))

            return e

        print '%s: Port %d is not an audio port.' % (self.name, port_index)
        return OMX_ErrorBadPortIndex

    #---------------------------------------------------------------------------
    def SetImagePortFormat(self, port_index, coding, color):
        """
        Set the format of an image port.

        Parameters:
            port_index      <int>       Index of port to set format.
            coding          <int>       Image coding format.
            color           <int>       Color format.

        Return value:
            <int>       Error code.
        """

        self.c_app_data.method = 'SetImagePortFormat'

        if self.num_ports['Image'] <= 0:
            print '%s: Component has no image port.' % self.name
            return OMX_ErrorNone

        for n in xrange(self.num_ports['Image']):
            key = 'Image%d' % (n+1)
            if port_index != self.port_indices[key]:
                continue

#            cons_print('%s: Setting image port %d format...' %
#                (self.name, port_index))
            c_ipf = OMX_IMAGE_PARAM_PORTFORMATTYPE()
            c_ipf.nPortIndex = port_index
            c_ipf.eCompressionFormat = coding
            c_ipf.eColorFormat = color
            e = self.SetParameter(OMX_IndexParamImagePortFormat,
                    ctypes.pointer(c_ipf))
            if e == OMX_ErrorNone:
                cons_print('%s: Image port %d format set.' %
                    (self.name, port_index))

            return e

        print '%s: Port %d is not an image port.' % (self.name, port_index)
        return OMX_ErrorBadPortIndex

    #---------------------------------------------------------------------------
    def SetVideoPortFormat(self, port_index, coding, color, frame_rate):
        """
        Set the format of a video port.

        Parameters:
            port_index      <int>       Index of port to set format.
            coding          <int>       Video coding format.
            color           <int>       Color format.
            frame_rate      <int>       Video frame rate in Q16 format.

        Return value:
            <int>       Error code.
        """

        self.c_app_data.method = 'SetVideoPortFormat'

        if self.num_ports['Video'] <= 0:
            print '%s: Component has no video port.' % self.name
            return OMX_ErrorNone

        for n in xrange(self.num_ports['Video']):
            key = 'Video%d' % (n+1)
            if port_index != self.port_indices[key]:
                continue

#            cons_print('%s: Setting video port %d format...' %
#                (self.name, port_index))
            c_vpf = OMX_VIDEO_PARAM_PORTFORMATTYPE()
            c_vpf.nPortIndex = port_index
            c_vpf.eCompressionFormat = coding
            c_vpf.eColorFormat = color
            c_vpf.xFramerate = frame_rate
            e = self.SetParameter(OMX_IndexParamVideoPortFormat,
                    ctypes.pointer(c_vpf))
            if e == OMX_ErrorNone:
                cons_print('%s: Video port %d format set.' %
                    (self.name, port_index))

            return e

        print '%s: Port %d is not a video port.' % (self.name, port_index)
        return OMX_ErrorBadPortIndex

    #---------------------------------------------------------------------------
    def SetOtherPortFormat(self, port_index, data_type):
        """
        Set the format of an other-type port.

        Parameters:
            port_index      <int>       Index of port to set format.
            data_type       <int>       Type of data expected for this port.

        Return value:
            <int>       Error code.
        """

        self.c_app_data.method = 'SetOtherPortFormat'

        if self.num_ports['Other'] <= 0:
            print '%s: Component has no other-type port.' % self.name
            return OMX_ErrorNone

        for n in xrange(self.num_ports['Other']):
            key = 'Other%d' % (n+1)
            if port_index != self.port_indices[key]:
                continue

#            cons_print('%s: Setting other-type port %d format...' %
#                (self.name, port_index))
            c_opf = OMX_OTHER_PARAM_PORTFORMATTYPE()
            c_opf.nPortIndex = port_index
            c_opf.eFormat = data_type
            e = self.SetParameter(OMX_IndexParamOtherPortFormat,
                    ctypes.pointer(c_opf))
            if e == OMX_ErrorNone:
                cons_print('%s: Other-type port %d format set.' %
                    (self.name, port_index))

            return e

        print '%s: Port %d is not an other-type port.' % (self.name, port_index)
        return OMX_ErrorBadPortIndex

    #---------------------------------------------------------------------------
    def SetBufferSupplier(self, port_index, buf_sup):
        """
        Set the buffer supplier of a port.

        Parameters:
            port_index      <int>       Index of port to set buffer supplier.
            buf_sup         <int>       Buffer supplier code:
                                            OMX_BufferSupplyUnspecified,
                                            OMX_BufferSupplyInput or
                                            OMX_BufferSupplyOutput.

        Return value:
            <int>       Error code.
        """

        self.c_app_data.method = 'SetBufferSupplier'

        c_param = OMX_PARAM_BUFFERSUPPLIERTYPE()
        c_param.nPortIndex = port_index
        c_param.eBufferSupplier = buf_sup
        e = self.SetParameter(OMX_IndexParamCompBufferSupplier,
                ctypes.pointer(c_param))
        if e == OMX_ErrorNone:
            cons_print('%s: Port %d buffer supplier set.' %
                (self.name, port_index))

        return e

    #---------------------------------------------------------------------------
    # Miscellaneous Methods
    #---------------------------------------------------------------------------

    def printPortDefinition(self, c_port_def):
        """
        Print the definition parameters of a port.

        Parameters:
            c_port_def      <c_struct>  OMX_PARAM_PORTDEFINITIONTYPE structure.
        """

        print('%s: Port %d Definition' %
                (self.name, c_port_def.nPortIndex))
        dir_names = ('input', 'output')
        print('    eDir = %s' % dir_names[c_port_def.eDir])
        print('    nBufferCountActual = %d' % c_port_def.nBufferCountActual)
        print('    nBufferCountMin = %d' % c_port_def.nBufferCountMin)
        print('    nBufferSize = %d' % c_port_def.nBufferSize)
        no_yes = ('no', 'yes')
        print('    bEnabled = %s' % no_yes[c_port_def.bEnabled])
        print('    bPopulated = %s' % no_yes[c_port_def.bPopulated])
        type_names = ('audio', 'video', 'image', 'other')
        print('    eDomain = %s' % type_names[c_port_def.eDomain])
        print('    bBuffersContiguous = %s' % no_yes[c_port_def.bBuffersContiguous])
        print('    nBufferAlignment = %d' % c_port_def.nBufferAlignment)

        if c_port_def.eDomain == 0: # audio port domain
            printAudioPortDefinition(c_port_def.format.audio)

        elif c_port_def.eDomain == 1: # video port domain
            printVideoPortDefinition(c_port_def.format.video)

        elif c_port_def.eDomain == 2: # image port domain
            self.printImagePortDefinition(c_port_def.format.image)

        if c_port_def.eDomain == 3: # other port domain
            printOtherPortDefinition(c_port_def.format.other)

    #---------------------------------------------------------------------------
    def printAudioPortDefinition(self, c_audioportdef,
                                 name=' '*4, indent=' '*4):
        """
        Print the format of an audio port.

        Parameters:
            c_audioportdef  <c_struct>  OMX_AUDIO_PORTDEFINITIONTYPE structure.
        """

        print('%sAudio Port Format:' % name)
#        print('%s    cMIMEType = %s' %
#            (indent, ctypes.string_at(c_audioportdef.cMIMEType)))
        print('%s    bFlagErrorConcealment = %d' %
            (indent, c_audioportdef.bFlagErrorConcealment))
        print('%s    eEncoding = %s' %
            (indent, omx_audio_coding_names[c_audioportdef.eEncoding]))

    #---------------------------------------------------------------------------
    def printVideoPortDefinition(self, c_videoportdef,
                                 name=' '*4, indent=' '*4):
        """
        Print the format of a video port.

        Parameters:
            c_videoportdef  <c_struct>  OMX_VIDEO_PORTDEFINITIONTYPE structure.
        """

        print('%sVideo Port Format:' % name)
#        print('%s    cMIMEType = %s' %
#            (indent, ctypes.string_at(c_videoportdef.cMIMEType)))
        print('%s    nFrameWidth = %d' %
            (indent, c_videoportdef.nFrameWidth))
        print('%s    nFrameHeight = %d' %
            (indent, c_videoportdef.nFrameHeight))
        print('%s    nStride = %d' % (indent, c_videoportdef.nStride))
        print('%s    nSliceHeight = %d' %
            (indent, c_videoportdef.nSliceHeight))
        print('%s    nBitrate = %d' % (indent, c_videoportdef.nBitrate))
        print('%s    xFramerate = %d' % (indent, c_videoportdef.xFramerate))
        print('%s    bFlagErrorConcealment = %d' %
            (indent, c_videoportdef.bFlagErrorConcealment))
        print(indent, '    eCompressionFormat = %s' %
            (indent, omx_video_coding_names[c_videoportdef.eCompressionFormat]))
        print(indent, '    eColorFormat = %s' %
            (indent, omx_color_format_names[c_videoportdef.eColorFormat]))

    #---------------------------------------------------------------------------
    def printImagePortDefinition(self, c_imgportdef,
                                 name=' '*4, indent=' '*4):
        """
        Print the format of an image port.

        Parameters:
            c_imgportdef    <c_struct>  OMX_IMAGE_PORTDEFINITIONTYPE structure.
        """

        print('%sImage Port Format:' % name)
#        print('%s    cMIMEType = %s' %
#            (indent, ctypes.string_at(c_imgportdef.cMIMEType)))
        print('%s    nFrameWidth = %d' %
            (indent, c_imgportdef.nFrameWidth))
        print('%s    nFrameHeight = %d' %
            (indent, c_imgportdef.nFrameHeight))
        print('%s    nStride = %d' % (indent, c_imgportdef.nStride))
        print('%s    nSliceHeight = %d' %
            (indent, c_imgportdef.nSliceHeight))
        print('%s    bFlagErrorConcealment = %d' %
            (indent, c_imgportdef.bFlagErrorConcealment))
        print('%s    eCompressionFormat = %s' %
            (indent, omx_image_coding_names[c_imgportdef.eCompressionFormat]))
        print('%s    eColorFormat = %s' %
            (indent, omx_color_format_names[c_imgportdef.eColorFormat]))
        
    #---------------------------------------------------------------------------
    def printOtherPortDefinition(self, c_otherportdef,
                                 name=' '*4, indent=' '*4):
        """
        Print the format of an other-type port.

        Parameters:
            c_otherportdef  <c_struct>  OMX_OTHER_PORTDEFINITIONTYPE structure.
        """

        print('%sOther-Type Port Format:' % name)
        print('%s    eFormat = %s' %
            (indent, omx_other_data_type_names[c_otherportdef.eFormat]))

    #---------------------------------------------------------------------------
    def printBufferHeader(self, c_buf_hdr):
        """
        Print the members of a buffer header.

        Parameters:
            c_buf_hdr       <c_struct>  OMX_BUFFERHEADERTYPE structure.

        Notes:
            nTimeStamp is splitted into two 4-byte words for ctypes.
            Otherwise, the size of the buffer header structure reported by
            ctypes.sizeof() will have 8 extra bytes due to 8-byte alignment.
        """

        print('Buffer Header:')
        print('    nSize =', c_buf_hdr.nSize)
        print('    nVersion =', hex(c_buf_hdr.nVersion.nVersion))
        print('    pBuffer =', c_buf_hdr.pBuffer)
        print('    nAllocLen =', c_buf_hdr.nAllocLen)
        print('    nFilledLen =', c_buf_hdr.nFilledLen)
        print('    nOffet =', c_buf_hdr.nOffset)
        print('    pAppPrivate =', c_buf_hdr.pAppPrivate)
        print('    pPlatformPrivate =', c_buf_hdr.pPlatformPrivate)
        print('    pInputPortPrivate =', c_buf_hdr.pInputPortPrivate)
        print('    nOutputPortPrivate =', c_buf_hdr.pOutputPortPrivate)
        print('    hMarkTargetComponent =', c_buf_hdr.hMarkTargetComponent)
        print('    pMarkData =', c_buf_hdr.pMarkData)
        print('    nTickCount =', c_buf_hdr.nTickCount)
        print('    nTimeStamp0 =', hex(c_buf_hdr.nTimeStamp0))
        print('    nTimeStamp1 =', hex(c_buf_hdr.nTimeStamp1))
        print('    nFlags =', hex(c_buf_hdr.nFlags))
        print('    nOutputPortIndex =', c_buf_hdr.nOutputPortIndex)
        print('    nInputPortIndex =', c_buf_hdr.nInputPortIndex)

    #---------------------------------------------------------------------------
    def Info(self):
        """
        Get and print the current parameters and state of the component.
        """

        for domain_name in omx_component_domain_names:
            num_ports = self.num_ports[domain_name]
            if num_ports <= 0:
                continue
            print('%s has %d %s-type ports starting at %d.' %
               (self.name, num_ports, domain_name,
                self.port_indices[domain_name+'1']))

            for n in xrange(num_ports):
                key = '%s%d' % (domain_name, n+1)
                port_index = self.port_indices[key]
                e, c_port_def = self.GetPortDefinition(port_index)
                if e == OMX_ErrorNone:
                    self.printPortDefinition(c_port_def)

                e, num_streams = self.GetNumberStreams(port_index)
                e1, stream_num = self.GetActiveStream(port_index)
                if e != OMX_ErrorNone or e1 != OMX_ErrorNone:
                    continue
                print('%s: Port %d has %d streams. Active stream = %d.' %
                    (self.name, port_index, num_streams, stream_num))

        e, state = self.GetState()
        print('%s: Currently in %s.' %
           (self.name, omx_state_names[self.c_app_data.current_state]))

#===============================================================================

# Load library bcm_host.
_libbcm = ctypes.CDLL('libbcm_host.so')

bcm_host_init = _libbcm.bcm_host_init
bcm_host_init.argtypes = []
bcm_host_init.restype = None

bcm_host_deinit = _libbcm.bcm_host_deinit
bcm_host_deinit.argtypes = []
bcm_host_deinit.restype = None

bcm_host_init()

# Initialize the OMX core.
e = OMX_Init()
assert (e == OMX_ErrorNone)

