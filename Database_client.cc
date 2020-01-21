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
#include <stdlib.h>

#include <grpcpp/grpcpp.h>

#ifdef BAZEL_BUILD
#include "examples/protos/Database.grpc.pb.h"
#else
#include "Database.grpc.pb.h"
#endif

using grpc::Channel;
using grpc::ClientContext;
using grpc::Status;
using Database::QueryRequest;
using Database::QueryReply;
using Database::QueryHandler;

class QueryHandlerClient {
 public:
  QueryHandlerClient(std::shared_ptr<Channel> channel)
      : stub_(QueryHandler::NewStub(channel)) {}

  // Assembles the client's payload, sends it and presents the response back
  // from the server.
  std::string QueryInsert(const std::string& user) {
    // Data we are sending to the server.
    QueryRequest request;
    request.set_frame_id(1);
    request.set_cls_id(0);

	// Yu: RANDOM intialize some data
	int d = 512, nq = 2;
    request.set_num_query(nq);
	float *xq = new float[d * nq];

	auto query = request.mutable_query();
	auto center = request.mutable_center();
	query -> Reserve(d * nq);
	center -> Reserve(2 * nq);

	for(long i = 0; i < nq; i++) {
		for(long j = 0; j < d; j++)
	    	xq[d * i + j] = drand48();
	}

	for(long i = 0; i < nq; i++) {
		for(long j = 0; j < d; j++)
		{
	    	request.add_query(xq[d * i + j]);
	    	std::cout<< "Prepared "  << request.query(d * i + j) << std::endl;
			if (j < 2)
	    		request.add_center(xq[2 * i + j]);
		}
	    	// query -> AddAllocated(xq + d * i + j); // AddAllocated
	}

    // Container for the data we expect from the server.
    QueryReply reply;

    // Context for the client. It could be used to convey extra information to
    // the server and/or tweak certain RPC behaviors.
    ClientContext context;

    // The actual RPC.
    Status status = stub_->QueryInsert(&context, request, &reply);

    // Act upon its status.
    if (status.ok()) {
      return reply.status();
    } else {
      std::cout << status.error_code() << ": " << status.error_message()
                << std::endl;
      return "RPC failed";
    }
  }

 private:
  std::unique_ptr<QueryHandler::Stub> stub_;
};

int main(int argc, char** argv) {
  // Instantiate the client. It requires a channel, out of which the actual RPCs
  // are created. This channel models a connection to an endpoint (in this case,
  // localhost at port 50051). We indicate that the channel isn't authenticated
  // (use of InsecureChannelCredentials()).
  QueryHandlerClient querier(grpc::CreateChannel(
      "localhost:50051", grpc::InsecureChannelCredentials()));
  std::string user("world");
  std::string reply = querier.QueryInsert(user);
  std::cout << "Greeter received: " << reply << std::endl;

  return 0;
}
