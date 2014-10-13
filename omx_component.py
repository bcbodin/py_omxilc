"""
   omx_component.py
   Python Conversion of OMX_Component.h - OpenMax IL version 1.1.2
   by Binh Bui - 2014-09-25

/*
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

/** OMX_Component.h - OpenMax IL version 1.1.2
 *  The OMX_Component header file contains the definitions used to define
 *  the public interface of a component.  This header file is intended to
 *  be used by both the application and the component.
 */
"""


#** Each OMX header must include all required header files to allow the
#*  header to compile without errors.  The includes below are required
#*  for this header file to compile successfully 
#*/

#include "OMX_Audio.h"
#include "OMX_Video.h"
#include "OMX_Image.h"
#include "OMX_Other.h"

from omx_audio import *
from omx_video import *
from omx_image import *
from omx_other import *


#** @ingroup comp */
OMX_PORTDOMAINTYPE = OMX_U32

(   OMX_PortDomainAudio, 
    OMX_PortDomainVideo, 
    OMX_PortDomainImage, 
    OMX_PortDomainOther 
    ) = range(4)

OMX_PortDomainKhronosExtensions = 0x6F000000  #**< Reserved region for introducing Khronos Standard Extensions */ 
OMX_PortDomainVendorStartUnused = 0x7F000000  #**< Reserved region for introducing Vendor Extensions */
OMX_PortDomainMax = 0x7ffffff

#} OMX_PORTDOMAINTYPE;

#** @ingroup comp */
class OMX_PORTDEFINITIONTYPE_U(ctypes.Union):
    _fields_ = [('audio', OMX_AUDIO_PORTDEFINITIONTYPE),
                ('video', OMX_VIDEO_PORTDEFINITIONTYPE),
                ('image', OMX_IMAGE_PORTDEFINITIONTYPE),
                ('other', OMX_OTHER_PORTDEFINITIONTYPE)]

class OMX_PARAM_PORTDEFINITIONTYPE(ctypes.Structure):
    _fields_ = [('nSize', OMX_U32),                 #**< Size of the structure in bytes */
                ('nVersion', OMX_VERSIONTYPE),      #**< OMX specification version information */
                ('nPortIndex', OMX_U32),            #**< Port number the structure applies to */
                ('eDir', OMX_DIRTYPE),              #**< Direction (input or output) of this port */
                ('nBufferCountActual', OMX_U32),    #**< The actual number of buffers allocated on this port */
                ('nBufferCountMin', OMX_U32),       #**< The minimum number of buffers this port requires */
                ('nBufferSize', OMX_U32),           #**< Size, in bytes, for buffers to be used for this channel */
                ('bEnabled', OMX_BOOL),             #**< Ports default to enabled and are enabled/disabled by
                                                    #  OMX_CommandPortEnable/OMX_CommandPortDisable.
                                                    #  When disabled a port is unpopulated. A disabled port
                                                    #  is not populated with buffers on a transition to IDLE. */
                ('bPopulated', OMX_BOOL),           #**< Port is populated with all of its buffers as indicated by
                                                    #  nBufferCountActual. A disabled port is always unpopulated. 
                                                    #  An enabled port is populated on a transition to OMX_StateIdle
                                                    #  and unpopulated on a transition to loaded. */
                ('eDomain', OMX_PORTDOMAINTYPE),    #**< Domain of the port. Determines the contents of metadata below. */
                ('format', OMX_PORTDEFINITIONTYPE_U),
                ('bBuffersContiguous', OMX_BOOL),
                ('nBufferAlignment', OMX_U32)]

#} OMX_PARAM_PORTDEFINITIONTYPE;

#** @ingroup comp */
class OMX_PARAM_U32TYPE(ctypes.Structure):
    _fields_ = [('nSize', OMX_U32),             #**< Size of this structure, in Bytes */ 
                ('nVersion', OMX_VERSIONTYPE),  #**< OMX specification version information */ 
                ('nPortIndex', OMX_U32),        #**< port that this structure applies to */ 
                ('nU32', OMX_U32)]              #**< U32 value */

#} OMX_PARAM_U32TYPE;

#** @ingroup rpm */
OMX_SUSPENSIONPOLICYTYPE = OMX_U32

(   OMX_SuspensionDisabled, #**< No suspension; v1.0 behavior */
    OMX_SuspensionEnabled   #**< Suspension allowed */   
    ) = range(2)

OMX_SuspensionPolicyKhronosExtensions = 0x6F000000  #**< Reserved region for introducing Khronos Standard Extensions */ 
OMX_SuspensionPolicyStartUnused = 0x7F000000  #**< Reserved region for introducing Vendor Extensions */

OMX_SuspensionPolicyMax = 0x7fffffff

#} OMX_SUSPENSIONPOLICYTYPE;

#** @ingroup rpm */
class OMX_PARAM_SUSPENSIONPOLICYTYPE(ctypes.Structure):
    _fields_ = [('nSize', OMX_U32),
                ('nVersion', OMX_VERSIONTYPE),
                ('ePolicy', OMX_SUSPENSIONPOLICYTYPE)]

#} OMX_PARAM_SUSPENSIONPOLICYTYPE;

#** @ingroup rpm */
OMX_SUSPENSIONTYPE = OMX_U32

(   OMX_NotSuspended, #**< component is not suspended */
    OMX_Suspended     #**< component is suspended */
    ) = range(2)

OMX_SuspensionKhronosExtensions = 0x6F000000  #**< Reserved region for introducing Khronos Standard Extensions */ 
OMX_SuspensionVendorStartUnused = 0x7F000000  #**< Reserved region for introducing Vendor Extensions */

OMX_SuspendMax = 0x7FFFFFFF

#} OMX_SUSPENSIONTYPE;

#** @ingroup rpm */
class OMX_PARAM_SUSPENSIONTYPE(ctypes.Structure):
    _fields_ = [('nSize', OMX_U32),
                ('nVersion', OMX_VERSIONTYPE),
                ('eType', OMX_SUSPENSIONTYPE)]

#} OMX_PARAM_SUSPENSIONTYPE ;

class OMX_CONFIG_BOOLEANTYPE(ctypes.Structure):
    _fields_ = [('nSize', OMX_U32),
                ('nVersion', OMX_VERSIONTYPE),
                ('bEnabled', OMX_BOOL)]

#} OMX_CONFIG_BOOLEANTYPE;

#* Parameter specifying the content uri to use. */
#** @ingroup cp */
class OMX_PARAM_CONTENTURITYPE(ctypes.Structure):
    _fields_ = [('nSize', OMX_U32),             #**< size of the structure in bytes, including
                                                #  actual URI name */
                ('nVersion', OMX_VERSIONTYPE),  #**< OMX specification version information */
                ('contentURI', OMX_U8 * 1)]     #**< The URI name */

#} OMX_PARAM_CONTENTURITYPE;

#* Parameter specifying the pipe to use. */
#** @ingroup cp */
class OMX_PARAM_CONTENTPIPETYPE(ctypes.Structure):
    _fields_ = [('nSize', OMX_U32),             #**< size of the structure in bytes */
                ('nVersion', OMX_VERSIONTYPE),  #**< OMX specification version information */
                ('hPipe', OMX_HANDLETYPE )]     #**< The pipe handle*/

#} OMX_PARAM_CONTENTPIPETYPE;

#** @ingroup rpm */
class OMX_RESOURCECONCEALMENTTYPE(ctypes.Structure):
    _fields_ = [('nSize', OMX_U32),             #**< size of the structure in bytes */
                ('nVersion', OMX_VERSIONTYPE),  #**< OMX specification version information */
                ('bResourceConcealmentForbidden', OMX_BOOL )] #**< disallow the use of resource concealment 
                                                # methods (like degrading algorithm quality to 
                                                # lower resource consumption or functional bypass) 
                                                # on a component as a resolution to resource conflicts. */

#} OMX_RESOURCECONCEALMENTTYPE;

#** @ingroup metadata */
OMX_METADATACHARSETTYPE = OMX_U32

(   OMX_MetadataCharsetUnknown, # = 0,
    OMX_MetadataCharsetASCII,
    OMX_MetadataCharsetBinary,
    OMX_MetadataCharsetCodePage1252,
    OMX_MetadataCharsetUTF8,
    OMX_MetadataCharsetJavaConformantUTF8,
    OMX_MetadataCharsetUTF7,
    OMX_MetadataCharsetImapUTF7,
    OMX_MetadataCharsetUTF16LE, 
    OMX_MetadataCharsetUTF16BE,
    OMX_MetadataCharsetGB12345,
    OMX_MetadataCharsetHZGB2312,
    OMX_MetadataCharsetGB2312,
    OMX_MetadataCharsetGB18030,
    OMX_MetadataCharsetGBK,
    OMX_MetadataCharsetBig5,
    OMX_MetadataCharsetISO88591,
    OMX_MetadataCharsetISO88592,
    OMX_MetadataCharsetISO88593,
    OMX_MetadataCharsetISO88594,
    OMX_MetadataCharsetISO88595,
    OMX_MetadataCharsetISO88596,
    OMX_MetadataCharsetISO88597,
    OMX_MetadataCharsetISO88598,
    OMX_MetadataCharsetISO88599,
    OMX_MetadataCharsetISO885910,
    OMX_MetadataCharsetISO885913,
    OMX_MetadataCharsetISO885914,
    OMX_MetadataCharsetISO885915,
    OMX_MetadataCharsetShiftJIS,
    OMX_MetadataCharsetISO2022JP,
    OMX_MetadataCharsetISO2022JP1,
    OMX_MetadataCharsetISOEUCJP,
    OMX_MetadataCharsetSMS7Bit 
    ) = range(34)

OMX_MetadataCharsetKhronosExtensions = 0x6F000000  #**< Reserved region for introducing Khronos Standard Extensions */ 
OMX_MetadataCharsetVendorStartUnused = 0x7F000000  #**< Reserved region for introducing Vendor Extensions */

OMX_MetadataCharsetTypeMax= 0x7FFFFFFF

#} OMX_METADATACHARSETTYPE;

#** @ingroup metadata */
OMX_METADATASCOPETYPE = OMX_U32

(   OMX_MetadataScopeAllLevels,
    OMX_MetadataScopeTopLevel,
    OMX_MetadataScopePortLevel,
    OMX_MetadataScopeNodeLevel 
    ) = range(4)

OMX_MetadataScopeKhronosExtensions = 0x6F000000  #**< Reserved region for introducing Khronos Standard Extensions */ 
OMX_MetadataScopeVendorStartUnused = 0x7F000000  #**< Reserved region for introducing Vendor Extensions */

OMX_MetadataScopeTypeMax = 0x7fffffff

#} OMX_METADATASCOPETYPE;

#** @ingroup metadata */
OMX_METADATASEARCHMODETYPE = OMX_U32

(   OMX_MetadataSearchValueSizeByIndex,
    OMX_MetadataSearchItemByIndex,
    OMX_MetadataSearchNextItemByKey 
    ) = range(3)

OMX_MetadataSearchKhronosExtensions = 0x6F000000  #**< Reserved region for introducing Khronos Standard Extensions */ 
OMX_MetadataSearchVendorStartUnused = 0x7F000000  #**< Reserved region for introducing Vendor Extensions */

OMX_MetadataSearchTypeMax = 0x7fffffff

#} OMX_METADATASEARCHMODETYPE;

#** @ingroup metadata */
class OMX_CONFIG_METADATAITEMCOUNTTYPE(ctypes.Structure):
    _fields_ = [('nSize', OMX_U32),
                ('nVersion', OMX_VERSIONTYPE),
                ('eScopeMode', OMX_METADATASCOPETYPE),
                ('nScopeSpecifier', OMX_U32),
                ('nMetadataItemCount', OMX_U32)]

#} OMX_CONFIG_METADATAITEMCOUNTTYPE;

#** @ingroup metadata */
class OMX_CONFIG_METADATAITEMTYPE(ctypes.Structure):
    _fields_ = [('nSize', OMX_U32),
                ('nVersion', OMX_VERSIONTYPE),
                ('eScopeMode', OMX_METADATASCOPETYPE),
                ('nScopeSpecifier', OMX_U32),
                ('nMetadataItemIndex', OMX_U32),  
                ('eSearchMode', OMX_METADATASEARCHMODETYPE),
                ('eKeyCharset', OMX_METADATACHARSETTYPE),
                ('nKeySizeUsed', OMX_U8),
                ('nKey', OMX_U8 * 128),
                ('eValueCharset', OMX_METADATACHARSETTYPE),
                ('sLanguageCountry', OMX_STRING),
                ('nValueMaxSize', OMX_U32),
                ('nValueSizeUsed', OMX_U32),
                ('nValue', OMX_U8 * 1)]

#} OMX_CONFIG_METADATAITEMTYPE;

#* @ingroup metadata */
class OMX_CONFIG_CONTAINERNODECOUNTTYPE(ctypes.Structure):
    _fields_ = [('nSize', OMX_U32),
                ('nVersion', OMX_VERSIONTYPE),
                ('bAllKeys', OMX_BOOL),
                ('nParentNodeID', OMX_U32),
                ('nNumNodes', OMX_U32)]

#} OMX_CONFIG_CONTAINERNODECOUNTTYPE;

#** @ingroup metadata */
class OMX_CONFIG_CONTAINERNODEIDTYPE(ctypes.Structure):
    _fields_ = [('nSize', OMX_U32),
                ('nVersion', OMX_VERSIONTYPE),
                ('bAllKeys', OMX_BOOL),
                ('nParentNodeID', OMX_U32),
                ('nNodeIndex', OMX_U32), 
                ('nNodeID', OMX_U32), 
                ('cNodeName', OMX_STRING),
                ('bIsLeafType', OMX_BOOL)]

#} OMX_CONFIG_CONTAINERNODEIDTYPE;

#** @ingroup metadata */
class OMX_PARAM_METADATAFILTERTYPE(ctypes.Structure):
    _fields_ = [('nSize', OMX_U32), 
                ('nVersion', OMX_VERSIONTYPE), 
                ('bAllKeys', OMX_BOOL),	        #* if true then this structure refers to all keys and 
                                                #* the three key fields below are ignored */
                ('eKeyCharset', OMX_METADATACHARSETTYPE),
                ('nKeySizeUsed', OMX_U32), 
                ('nKey', OMX_U8 * 128), 
                ('nLanguageCountrySizeUsed', OMX_U32),
                ('nLanguageCountry', OMX_U8 * 128),
                ('bEnabled', OMX_BOOL)]	        #* if true then key is part of filter (e.g. 
                                                #* retained for query later). If false then
                                                #* key is not part of filter */

#} OMX_PARAM_METADATAFILTERTYPE; 

#** The OMX_COMPONENTTYPE structure defines the component handle.  The component 
#*  handle is used to access all of the component's public methods and also
#*  contains pointers to the component's private data area.  The component
#*  handle is initialized by the OMX core (with help from the component)
#*  during the process of loading the component.  After the component is
#*  successfully loaded, the application can safely access any of the
#*  component's public functions (although some may return an error because
#*  the state is inappropriate for the access).
#* 
#*  @ingroup comp
#*/
class OMX_COMPONENTTYPE(ctypes.Structure):

    #** The size of this structure, in bytes.  It is the responsibility
    #   of the allocator of this structure to fill in this value.  Since
    #   this structure is allocated by the GetHandle function, this
    #   function will fill in this value. */
    _fields_ = [('nSize', OMX_U32),

    #** nVersion is the version of the OMX specification that the structure 
    #   is built against.  It is the responsibility of the creator of this 
    #   structure to initialize this value and every user of this structure 
    #   should verify that it knows how to use the exact version of 
    #   this structure found herein. */
                ('nVersion', OMX_VERSIONTYPE),

    #** pComponentPrivate is a pointer to the component private data area.  
    #   This member is allocated and initialized by the component when the 
    #   component is first loaded.  The application should not access this 
    #   data area. */
                ('pComponentPrivate', OMX_PTR),

    #** pApplicationPrivate is a pointer that is a parameter to the 
    #   OMX_GetHandle method, and contains an application private value 
    #   provided by the IL client.  This application private data is 
    #   returned to the IL Client by OMX in all callbacks */
                ('pApplicationPrivate', OMX_PTR),

    #** refer to OMX_GetComponentVersion in OMX_core.h or the OMX IL 
    #   specification for details on the GetComponentVersion method.
    #*/
    # OMX_ERRORTYPE (*GetComponentVersion)(
    #         OMX_IN  OMX_HANDLETYPE hComponent,
    #         OMX_OUT OMX_STRING pComponentName,
    #         OMX_OUT OMX_VERSIONTYPE* pComponentVersion,
    #         OMX_OUT OMX_VERSIONTYPE* pSpecVersion,
    #         OMX_OUT OMX_UUIDTYPE* pComponentUUID);
                ('GetComponentVersion', ctypes.CFUNCTYPE(OMX_ERRORTYPE,
                                                         OMX_HANDLETYPE,
                                                         OMX_STRING,
                                                         ctypes.POINTER(OMX_VERSIONTYPE),
                                                         ctypes.POINTER(OMX_VERSIONTYPE),
                                                         ctypes.POINTER(OMX_UUIDTYPE))),

    #** refer to OMX_SendCommand in OMX_core.h or the OMX IL 
    #   specification for details on the SendCommand method.
    #*/
    # OMX_ERRORTYPE (*SendCommand)(
    #         OMX_IN  OMX_HANDLETYPE hComponent,
    #         OMX_IN  OMX_COMMANDTYPE Cmd,
    #         OMX_IN  OMX_U32 nParam1,
    #         OMX_IN  OMX_PTR pCmdData);
                ('SendCommand', ctypes.CFUNCTYPE(OMX_ERRORTYPE,
                                                 OMX_HANDLETYPE,
                                                 OMX_COMMANDTYPE,
                                                 OMX_U32,
                                                 OMX_PTR)),

    #** refer to OMX_GetParameter in OMX_core.h or the OMX IL 
    #   specification for details on the GetParameter method.
    #*/
    # OMX_ERRORTYPE (*GetParameter)(
    #         OMX_IN  OMX_HANDLETYPE hComponent, 
    #         OMX_IN  OMX_INDEXTYPE nParamIndex,  
    #         OMX_INOUT OMX_PTR pComponentParameterStructure);
                ('GetParameter', ctypes.CFUNCTYPE(OMX_ERRORTYPE,
                                                  OMX_HANDLETYPE, 
                                                  OMX_INDEXTYPE,  
                                                  OMX_PTR)),

    #** refer to OMX_SetParameter in OMX_core.h or the OMX IL 
    #   specification for details on the SetParameter method.
    #*/
    # OMX_ERRORTYPE (*SetParameter)(
    #         OMX_IN  OMX_HANDLETYPE hComponent, 
    #         OMX_IN  OMX_INDEXTYPE nIndex,
    #         OMX_IN  OMX_PTR pComponentParameterStructure);
                ('SetParameter', ctypes.CFUNCTYPE(OMX_ERRORTYPE,
                                                  OMX_HANDLETYPE, 
                                                  OMX_INDEXTYPE,
                                                  OMX_PTR)),

    #** refer to OMX_GetConfig in OMX_core.h or the OMX IL 
    #   specification for details on the GetConfig method.
    #*/
    # OMX_ERRORTYPE (*GetConfig)(
    #         OMX_IN  OMX_HANDLETYPE hComponent,
    #         OMX_IN  OMX_INDEXTYPE nIndex, 
    #         OMX_INOUT OMX_PTR pComponentConfigStructure);
                ('GetConfig', ctypes.CFUNCTYPE(OMX_ERRORTYPE,
                                               OMX_HANDLETYPE,
                                               OMX_INDEXTYPE,
                                               OMX_PTR)),

    #** refer to OMX_SetConfig in OMX_core.h or the OMX IL 
    #   specification for details on the SetConfig method.
    #*/
    # OMX_ERRORTYPE (*SetConfig)(
    #         OMX_IN  OMX_HANDLETYPE hComponent,
    #         OMX_IN  OMX_INDEXTYPE nIndex, 
    #         OMX_IN  OMX_PTR pComponentConfigStructure);
                ('SetConfig', ctypes.CFUNCTYPE(OMX_ERRORTYPE,
                                               OMX_HANDLETYPE,
                                               OMX_INDEXTYPE,
                                               OMX_PTR)),

    #** refer to OMX_GetExtensionIndex in OMX_core.h or the OMX IL 
    #   specification for details on the GetExtensionIndex method.
    #*/
    # OMX_ERRORTYPE (*GetExtensionIndex)(
    #         OMX_IN  OMX_HANDLETYPE hComponent,
    #         OMX_IN  OMX_STRING cParameterName,
    #         OMX_OUT OMX_INDEXTYPE* pIndexType);
                ('GetExtensionIndex', ctypes.CFUNCTYPE(OMX_ERRORTYPE,
                                                       OMX_HANDLETYPE,
                                                       OMX_STRING,
                                                       ctypes.POINTER(OMX_INDEXTYPE))),

    #** refer to OMX_GetState in OMX_core.h or the OMX IL 
    #   specification for details on the GetState method.
    #*/
    # OMX_ERRORTYPE (*GetState)(
    #         OMX_IN  OMX_HANDLETYPE hComponent,
    #         OMX_OUT OMX_STATETYPE* pState);
                ('GetState', ctypes.CFUNCTYPE(OMX_ERRORTYPE,
                                              OMX_HANDLETYPE,
                                              ctypes.POINTER(OMX_STATETYPE))),
    
    #** The ComponentTunnelRequest method will interact with another OMX
    #   component to determine if tunneling is possible and to setup the
    #   tunneling.  The return codes for this method can be used to 
    #   determine if tunneling is not possible, or if tunneling is not
    #   supported.  
        
    #   Base profile components (i.e. non-interop) do not support this
    #   method and should return OMX_ErrorNotImplemented 

    #   The interop profile component MUST support tunneling to another 
    #   interop profile component with a compatible port parameters.  
    #   A component may also support proprietary communication.
        
    #   If proprietary communication is supported the negotiation of 
    #   proprietary communication is done outside of OMX in a vendor 
    #   specific way. It is only required that the proper result be 
    #   returned and the details of how the setup is done is left 
    #   to the component implementation.  
    
    #   When this method is invoked when nPort in an output port, the
    #   component will:
    #   1.  Populate the pTunnelSetup structure with the output port's 
    #       requirements and constraints for the tunnel.

    #   When this method is invoked when nPort in an input port, the
    #   component will:
    #   1.  Query the necessary parameters from the output port to 
    #       determine if the ports are compatible for tunneling
    #   2.  If the ports are compatible, the component should store
    #       the tunnel step provided by the output port
    #   3.  Determine which port (either input or output) is the buffer
    #       supplier, and call OMX_SetParameter on the output port to
    #       indicate this selection.
        
    #   The component will return from this call within 5 msec.
    
    #   @param [in] hComp
    #       Handle of the component to be accessed.  This is the component
    #       handle returned by the call to the OMX_GetHandle method.
    #   @param [in] nPort
    #       nPort is used to select the port on the component to be used
    #       for tunneling.
    #   @param [in] hTunneledComp
    #       Handle of the component to tunnel with.  This is the component 
    #       handle returned by the call to the OMX_GetHandle method.  When
    #       this parameter is 0x0 the component should setup the port for
    #       communication with the application / IL Client.
    #   @param [in] nPortOutput
    #       nPortOutput is used indicate the port the component should
    #       tunnel with.
    #   @param [in] pTunnelSetup
    #       Pointer to the tunnel setup structure.  When nPort is an output port
    #       the component should populate the fields of this structure.  When
    #       When nPort is an input port the component should review the setup
    #       provided by the component with the output port.
    #   @return OMX_ERRORTYPE
    #       If the command successfully executes, the return code will be
    #       OMX_ErrorNone.  Otherwise the appropriate OMX error will be returned.
    #   @ingroup tun
    #*/
    # OMX_ERRORTYPE (*ComponentTunnelRequest)(
    #     OMX_IN  OMX_HANDLETYPE hComp,
    #     OMX_IN  OMX_U32 nPort,
    #     OMX_IN  OMX_HANDLETYPE hTunneledComp,
    #     OMX_IN  OMX_U32 nTunneledPort,
    #     OMX_INOUT  OMX_TUNNELSETUPTYPE* pTunnelSetup); 
                ('ComponentTunnelRequest', ctypes.CFUNCTYPE(OMX_ERRORTYPE,
                                                            OMX_HANDLETYPE,
                                                            OMX_U32,
                                                            OMX_HANDLETYPE,
                                                            OMX_U32,
                                                            ctypes.POINTER(OMX_TUNNELSETUPTYPE))), 

    #** refer to OMX_UseBuffer in OMX_core.h or the OMX IL 
    #   specification for details on the UseBuffer method.
    #   @ingroup buf
    #*/
    # OMX_ERRORTYPE (*UseBuffer)(
    #         OMX_IN OMX_HANDLETYPE hComponent,
    #         OMX_INOUT OMX_BUFFERHEADERTYPE** ppBufferHdr,
    #         OMX_IN OMX_U32 nPortIndex,
    #         OMX_IN OMX_PTR pAppPrivate,
    #         OMX_IN OMX_U32 nSizeBytes,
    #         OMX_IN OMX_U8* pBuffer);
                ('UseBuffer', ctypes.CFUNCTYPE(OMX_ERRORTYPE,
                                               OMX_HANDLETYPE,
                                               ppOMX_BUFFERHEADERTYPE,
                                               OMX_U32,
                                               OMX_PTR,
                                               OMX_U32,
                                               ctypes.POINTER(OMX_U8))),

    #** refer to OMX_AllocateBuffer in OMX_core.h or the OMX IL 
    #   specification for details on the AllocateBuffer method.
    #   @ingroup buf
    #*/
    # OMX_ERRORTYPE (*AllocateBuffer)(
    #         OMX_IN OMX_HANDLETYPE hComponent,
    #         OMX_INOUT OMX_BUFFERHEADERTYPE** ppBuffer,
    #         OMX_IN OMX_U32 nPortIndex,
    #         OMX_IN OMX_PTR pAppPrivate,
    #         OMX_IN OMX_U32 nSizeBytes);
                ('AllocateBuffer', ctypes.CFUNCTYPE(OMX_ERRORTYPE,
                                                    OMX_HANDLETYPE,
                                                    ppOMX_BUFFERHEADERTYPE,
                                                    OMX_U32,
                                                    OMX_PTR,
                                                    OMX_U32)),

    #** refer to OMX_FreeBuffer in OMX_core.h or the OMX IL 
    #   specification for details on the FreeBuffer method.
    #   @ingroup buf
    #*/
    # OMX_ERRORTYPE (*FreeBuffer)(
    #         OMX_IN  OMX_HANDLETYPE hComponent,
    #         OMX_IN  OMX_U32 nPortIndex,
    #         OMX_IN  OMX_BUFFERHEADERTYPE* pBuffer);
                ('FreeBuffer', ctypes.CFUNCTYPE(OMX_ERRORTYPE,
                                                OMX_HANDLETYPE,
                                                OMX_U32,
                                                pOMX_BUFFERHEADERTYPE)),

    #** refer to OMX_EmptyThisBuffer in OMX_core.h or the OMX IL 
    #   specification for details on the EmptyThisBuffer method.
    #   @ingroup buf
    #*/
    # OMX_ERRORTYPE (*EmptyThisBuffer)(
    #         OMX_IN  OMX_HANDLETYPE hComponent,
    #         OMX_IN  OMX_BUFFERHEADERTYPE* pBuffer);
                ('EmptyThisBuffer', ctypes.CFUNCTYPE(OMX_ERRORTYPE,
                                                     OMX_HANDLETYPE,
                                                     pOMX_BUFFERHEADERTYPE)),

    #** refer to OMX_FillThisBuffer in OMX_core.h or the OMX IL 
    #   specification for details on the FillThisBuffer method.
    #   @ingroup buf
    #*/
    # OMX_ERRORTYPE (*FillThisBuffer)(
    #         OMX_IN  OMX_HANDLETYPE hComponent,
    #         OMX_IN  OMX_BUFFERHEADERTYPE* pBuffer);
                ('FillThisBuffer', ctypes.CFUNCTYPE(OMX_ERRORTYPE,
                                                    OMX_HANDLETYPE,
                                                    pOMX_BUFFERHEADERTYPE)),

    #** The SetCallbacks method is used by the core to specify the callback
    #   structure from the application to the component.  This is a blocking
    #   call.  The component will return from this call within 5 msec.
    #   @param [in] hComponent
    #       Handle of the component to be accessed.  This is the component
    #       handle returned by the call to the GetHandle function.
    #   @param [in] pCallbacks
    #       pointer to an OMX_CALLBACKTYPE structure used to provide the 
    #       callback information to the component
    #   @param [in] pAppData
    #       pointer to an application defined value.  It is anticipated that 
    #       the application will pass a pointer to a data structure or a "this
    #       pointer" in this area to allow the callback (in the application)
    #       to determine the context of the call
    #   @return OMX_ERRORTYPE
    #       If the command successfully executes, the return code will be
    #       OMX_ErrorNone.  Otherwise the appropriate OMX error will be returned.
    #*/
    # OMX_ERRORTYPE (*SetCallbacks)(
    #         OMX_IN  OMX_HANDLETYPE hComponent,
    #         OMX_IN  OMX_CALLBACKTYPE* pCallbacks, 
    #         OMX_IN  OMX_PTR pAppData);
                ('SetCallbacks', ctypes.CFUNCTYPE(OMX_ERRORTYPE,
                                                  OMX_HANDLETYPE,
                                                  ctypes.POINTER(OMX_CALLBACKTYPE), 
                                                  OMX_PTR)),

    #** ComponentDeInit method is used to deinitialize the component
    #   providing a means to free any resources allocated at component
    #   initialization.  NOTE:  After this call the component handle is
    #   not valid for further use.
    #   @param [in] hComponent
    #       Handle of the component to be accessed.  This is the component
    #       handle returned by the call to the GetHandle function.
    #   @return OMX_ERRORTYPE
    #       If the command successfully executes, the return code will be
    #       OMX_ErrorNone.  Otherwise the appropriate OMX error will be returned.
    #*/
    # OMX_ERRORTYPE (*ComponentDeInit)(
    #         OMX_IN  OMX_HANDLETYPE hComponent);
                ('ComponentDeInit', ctypes.CFUNCTYPE(OMX_ERRORTYPE,
                                                     OMX_HANDLETYPE)),

    #** @ingroup buf */
    # OMX_ERRORTYPE (*UseEGLImage)(
    #         OMX_IN OMX_HANDLETYPE hComponent,
    #         OMX_INOUT OMX_BUFFERHEADERTYPE** ppBufferHdr,
    #         OMX_IN OMX_U32 nPortIndex,
    #         OMX_IN OMX_PTR pAppPrivate,
    #         OMX_IN void* eglImage);
                ('UseEGLImage', ctypes.CFUNCTYPE(OMX_ERRORTYPE,
                                                 OMX_HANDLETYPE,
                                                 ppOMX_BUFFERHEADERTYPE,
                                                 OMX_U32,
                                                 OMX_PTR,
                                                 ctypes.c_void_p)),

    # OMX_ERRORTYPE (*ComponentRoleEnum)(
    #         OMX_IN OMX_HANDLETYPE hComponent,
    #         OMX_OUT OMX_U8 *cRole,
    #         OMX_IN OMX_U32 nIndex);
                ('ComponentRoleEnum', ctypes.CFUNCTYPE(OMX_ERRORTYPE,
                                                       OMX_HANDLETYPE,
                                                       ctypes.POINTER(OMX_U8),
                                                       OMX_U32))]

#} OMX_COMPONENTTYPE;

pOMX_COMPONENTTYPE = ctypes.POINTER(OMX_COMPONENTTYPE)


#/* File EOF */

