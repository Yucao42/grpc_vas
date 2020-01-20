# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import Database_pb2 as Database__pb2


class QueryHandlerStub(object):
  """The query-and-insert service definition.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Query = channel.unary_unary(
        '/Database.QueryHandler/Query',
        request_serializer=Database__pb2.QueryRequest.SerializeToString,
        response_deserializer=Database__pb2.QueryReply.FromString,
        )
    self.QueryInsert = channel.unary_unary(
        '/Database.QueryHandler/QueryInsert',
        request_serializer=Database__pb2.QueryRequest.SerializeToString,
        response_deserializer=Database__pb2.QueryReply.FromString,
        )


class QueryHandlerServicer(object):
  """The query-and-insert service definition.
  """

  def Query(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def QueryInsert(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_QueryHandlerServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Query': grpc.unary_unary_rpc_method_handler(
          servicer.Query,
          request_deserializer=Database__pb2.QueryRequest.FromString,
          response_serializer=Database__pb2.QueryReply.SerializeToString,
      ),
      'QueryInsert': grpc.unary_unary_rpc_method_handler(
          servicer.QueryInsert,
          request_deserializer=Database__pb2.QueryRequest.FromString,
          response_serializer=Database__pb2.QueryReply.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'Database.QueryHandler', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
