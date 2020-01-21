/*
 *
 * Copyright 2015 gRPC authors.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 */

#include <iostream>
#include <memory>
#include <string>

#include <grpcpp/grpcpp.h>

#ifdef BAZEL_BUILD
#include "examples/protos/Database.grpc.pb.h"
#else
#include "Database.grpc.pb.h"
#endif

using grpc::Server;
using grpc::ServerBuilder;
using grpc::ServerContext;
using grpc::Status;
using Database::QueryRequest;
using Database::QueryReply;
using Database::QueryHandler;

// Logic and data behind the server's behavior.
class QueryHandlerServiceImpl final : public QueryHandler::Service {
  Status QueryInsert(ServerContext* context, const QueryRequest* request,
                  QueryReply* reply) override {
    std::string prefix("Hello ");
	int d = 512;
	int num_query = request -> num_query();

	for(long i = 0; i < num_query; i++) {
		for(long j = 0; j < d; j++)
	    	std::cout<< "Received "  << request -> query(d * i + j) << std::endl;
	}

	for(long i = 0; i < num_query; i++) {
		for(long j = 0; j < 2; j++)
	    	std::cout<< "Received "  << request -> center(2 * i + j) << std::endl;
	}
    reply->set_status("OK");

	auto indexes = reply -> mutable_indexes();
	indexes -> Reserve(num_query);
	for(long i = 0; i < num_query; i++) {
		reply -> add_indexes(i);
	}
    return Status::OK;
  }
};

void RunServer() {
  std::string server_address("0.0.0.0:50051");
  QueryHandlerServiceImpl service;

  ServerBuilder builder;
  // Listen on the given address without any authentication mechanism.
  builder.AddListeningPort(server_address, grpc::InsecureServerCredentials());
  // Register "service" as the instance through which we'll communicate with
  // clients. In this case it corresponds to an *synchronous* service.
  builder.RegisterService(&service);
  // Finally assemble the server.
  std::unique_ptr<Server> server(builder.BuildAndStart());
  std::cout << "Server listening on " << server_address << std::endl;

  // Wait for the server to shutdown. Note that some other thread must be
  // responsible for shutting down the server for this call to ever return.
  server->Wait();
}

int main(int argc, char** argv) {
  RunServer();

  return 0;
}
