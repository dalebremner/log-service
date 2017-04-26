# Copyright 2017 Dell Inc. or its subsidiaries.  All Rights Reserved.

from concurrent import futures
import time
import math
import subprocess

import grpc

import log_service_pb2
import log_service_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class LogServicer(log_service_pb2_grpc.LogServiceServicer):
    def GetSelEntries(self, request, context):
        print('Server received: ' + request.ipAddress + ' ' + request.userName)
        ipmiCommand = [
            "ipmitool",
            "-I",
            "lanplus",
            "-U",
            request.userName,
            "-P", request.password,
            "-H",
            request.ipAddress,
            "sel",
            "list"
        ]
        selOutput = subprocess.check_output(ipmiCommand)
        return log_service_pb2.SelReply(message=selOutput)

def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  log_service_pb2_grpc.add_LogServiceServicer_to_server(LogServicer(), server)
  server.add_insecure_port('[::]:50051')
  server.start()
  try:
    while True:
      time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop(0)

if __name__ == '__main__':
  serve()
