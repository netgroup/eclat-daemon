# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: eclat.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='eclat.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0b\x65\x63lat.proto\"3\n\x10\x45\x63latLoadRequest\x12\x0e\n\x06script\x18\x01 \x01(\t\x12\x0f\n\x07package\x18\x02 \x01(\t\"4\n\x11\x45\x63latLoadResponse\x12\x0e\n\x06status\x18\x01 \x01(\t\x12\x0f\n\x07message\x18\x02 \x01(\t\"&\n\x13\x45\x63latDumpMapRequest\x12\x0f\n\x07mapname\x18\x01 \x01(\t\"7\n\x14\x45\x63latDumpMapResponse\x12\x0e\n\x06status\x18\x01 \x01(\t\x12\x0f\n\x07message\x18\x02 \x01(\t\"7\n\x17\x45\x63latGetMapValueRequest\x12\x0f\n\x07mapname\x18\x01 \x01(\t\x12\x0b\n\x03key\x18\x02 \x01(\t\";\n\x18\x45\x63latGetMapValueResponse\x12\x0e\n\x06status\x18\x01 \x01(\t\x12\x0f\n\x07message\x18\x02 \x01(\t2\xc5\x01\n\x05\x45\x63lat\x12<\n\x11LoadConfiguration\x12\x11.EclatLoadRequest\x1a\x12.EclatLoadResponse\"\x00\x12\x38\n\x07\x44umpMap\x12\x14.EclatDumpMapRequest\x1a\x15.EclatDumpMapResponse\"\x00\x12\x44\n\x0bGetMapValue\x12\x18.EclatGetMapValueRequest\x1a\x19.EclatGetMapValueResponse\"\x00\x62\x06proto3'
)




_ECLATLOADREQUEST = _descriptor.Descriptor(
  name='EclatLoadRequest',
  full_name='EclatLoadRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='script', full_name='EclatLoadRequest.script', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='package', full_name='EclatLoadRequest.package', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=15,
  serialized_end=66,
)


_ECLATLOADRESPONSE = _descriptor.Descriptor(
  name='EclatLoadResponse',
  full_name='EclatLoadResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='EclatLoadResponse.status', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='message', full_name='EclatLoadResponse.message', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=68,
  serialized_end=120,
)


_ECLATDUMPMAPREQUEST = _descriptor.Descriptor(
  name='EclatDumpMapRequest',
  full_name='EclatDumpMapRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='mapname', full_name='EclatDumpMapRequest.mapname', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=122,
  serialized_end=160,
)


_ECLATDUMPMAPRESPONSE = _descriptor.Descriptor(
  name='EclatDumpMapResponse',
  full_name='EclatDumpMapResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='EclatDumpMapResponse.status', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='message', full_name='EclatDumpMapResponse.message', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=162,
  serialized_end=217,
)


_ECLATGETMAPVALUEREQUEST = _descriptor.Descriptor(
  name='EclatGetMapValueRequest',
  full_name='EclatGetMapValueRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='mapname', full_name='EclatGetMapValueRequest.mapname', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='key', full_name='EclatGetMapValueRequest.key', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=219,
  serialized_end=274,
)


_ECLATGETMAPVALUERESPONSE = _descriptor.Descriptor(
  name='EclatGetMapValueResponse',
  full_name='EclatGetMapValueResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='EclatGetMapValueResponse.status', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='message', full_name='EclatGetMapValueResponse.message', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=276,
  serialized_end=335,
)

DESCRIPTOR.message_types_by_name['EclatLoadRequest'] = _ECLATLOADREQUEST
DESCRIPTOR.message_types_by_name['EclatLoadResponse'] = _ECLATLOADRESPONSE
DESCRIPTOR.message_types_by_name['EclatDumpMapRequest'] = _ECLATDUMPMAPREQUEST
DESCRIPTOR.message_types_by_name['EclatDumpMapResponse'] = _ECLATDUMPMAPRESPONSE
DESCRIPTOR.message_types_by_name['EclatGetMapValueRequest'] = _ECLATGETMAPVALUEREQUEST
DESCRIPTOR.message_types_by_name['EclatGetMapValueResponse'] = _ECLATGETMAPVALUERESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

EclatLoadRequest = _reflection.GeneratedProtocolMessageType('EclatLoadRequest', (_message.Message,), {
  'DESCRIPTOR' : _ECLATLOADREQUEST,
  '__module__' : 'eclat_pb2'
  # @@protoc_insertion_point(class_scope:EclatLoadRequest)
  })
_sym_db.RegisterMessage(EclatLoadRequest)

EclatLoadResponse = _reflection.GeneratedProtocolMessageType('EclatLoadResponse', (_message.Message,), {
  'DESCRIPTOR' : _ECLATLOADRESPONSE,
  '__module__' : 'eclat_pb2'
  # @@protoc_insertion_point(class_scope:EclatLoadResponse)
  })
_sym_db.RegisterMessage(EclatLoadResponse)

EclatDumpMapRequest = _reflection.GeneratedProtocolMessageType('EclatDumpMapRequest', (_message.Message,), {
  'DESCRIPTOR' : _ECLATDUMPMAPREQUEST,
  '__module__' : 'eclat_pb2'
  # @@protoc_insertion_point(class_scope:EclatDumpMapRequest)
  })
_sym_db.RegisterMessage(EclatDumpMapRequest)

EclatDumpMapResponse = _reflection.GeneratedProtocolMessageType('EclatDumpMapResponse', (_message.Message,), {
  'DESCRIPTOR' : _ECLATDUMPMAPRESPONSE,
  '__module__' : 'eclat_pb2'
  # @@protoc_insertion_point(class_scope:EclatDumpMapResponse)
  })
_sym_db.RegisterMessage(EclatDumpMapResponse)

EclatGetMapValueRequest = _reflection.GeneratedProtocolMessageType('EclatGetMapValueRequest', (_message.Message,), {
  'DESCRIPTOR' : _ECLATGETMAPVALUEREQUEST,
  '__module__' : 'eclat_pb2'
  # @@protoc_insertion_point(class_scope:EclatGetMapValueRequest)
  })
_sym_db.RegisterMessage(EclatGetMapValueRequest)

EclatGetMapValueResponse = _reflection.GeneratedProtocolMessageType('EclatGetMapValueResponse', (_message.Message,), {
  'DESCRIPTOR' : _ECLATGETMAPVALUERESPONSE,
  '__module__' : 'eclat_pb2'
  # @@protoc_insertion_point(class_scope:EclatGetMapValueResponse)
  })
_sym_db.RegisterMessage(EclatGetMapValueResponse)



_ECLAT = _descriptor.ServiceDescriptor(
  name='Eclat',
  full_name='Eclat',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=338,
  serialized_end=535,
  methods=[
  _descriptor.MethodDescriptor(
    name='LoadConfiguration',
    full_name='Eclat.LoadConfiguration',
    index=0,
    containing_service=None,
    input_type=_ECLATLOADREQUEST,
    output_type=_ECLATLOADRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='DumpMap',
    full_name='Eclat.DumpMap',
    index=1,
    containing_service=None,
    input_type=_ECLATDUMPMAPREQUEST,
    output_type=_ECLATDUMPMAPRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetMapValue',
    full_name='Eclat.GetMapValue',
    index=2,
    containing_service=None,
    input_type=_ECLATGETMAPVALUEREQUEST,
    output_type=_ECLATGETMAPVALUERESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_ECLAT)

DESCRIPTOR.services_by_name['Eclat'] = _ECLAT

# @@protoc_insertion_point(module_scope)
